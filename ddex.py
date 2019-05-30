import xml.etree.ElementTree as ET,json
from base import *


class DDEXParser(Base):

    def __init__(self, args):
        Base.__init__(self, args)
        self.__root = ET.parse(args["xmlpath"]).getroot()

    def process_message_header(self, root):
        self.logInfo("PROCESSING MESSAGE HEADER")
        message = {}
        message_thread_id_tag = root.find('MessageThreadId')
        message["message_thread_id"]= ""

        if self.check_for_none(message_thread_id_tag):
            message["message_thread_id"] = message_thread_id_tag.text

        message_id_tag = root.find('MessageId')
        message["message_id"] = ""
        if self.check_for_none(message_id_tag):
            message["message_id"] = message_id_tag.text

        message_sender_partid_tag = root.find('MessageSender/PartyId')
        message["message_sender_partid"] = ""

        if self.check_for_none(message_sender_partid_tag):
            message["message_sender_partid"] = message_sender_partid_tag.text

        message_sender_partname_tag = root.find('MessageSender/PartyName/FullName')
        message["message_sender_partname"] = ""

        if self.check_for_none(message_sender_partname_tag):
            message["message_sender_partname"] = message_sender_partname_tag.text

        message_recipient_partid_tag = root.find('MessageRecipient/PartyId')
        message["message_recipient_partid"] = ""

        if self.check_for_none(message_recipient_partid_tag):
            message["message_recipient_partid"] = message_recipient_partid_tag.text

        message_recipient_partname_tag = root.find('MessageRecipient/PartyName/FullName')
        message["message_rec_partname"] = ""

        if self.check_for_none(message_recipient_partname_tag):
            message["message_rec_partname"] = message_recipient_partname_tag.text

        return message

    def process_resource_list(self, root):
        self.logInfo("PROCESSING RESOURCE LIST")
        image_tag = root.find('Image')
        image_type = ""
        image_file_url = ""
        image_file_hash_sum = ""
        image = {}

        if self.check_for_none(image_tag):
            image_type_tag = image_tag.find("ImageType")
            if self.check_for_none(image_type_tag):
                image_type = image_type_tag.text

            image_file_url_tag = image_tag.find("ImageDetailsByTerritory/TechnicalImageDetails/File/URL")
            if self.check_for_none(image_file_url_tag):
                image_file_url = image_file_url_tag.text

            image_file_hashsum_tag = image_tag.find(
                "ImageDetailsByTerritory/TechnicalImageDetails/File/HashSum/HashSum")
            if self.check_for_none(image_file_hashsum_tag):
                image_file_hash_sum = image_file_hashsum_tag.text
            image['image_type'] = image_type
            image['image_file_url'] = image_file_url
            image['image_file_hashsum'] = image_file_hash_sum
        #print(image)

        song = {}
        for child in root:
            isrc = ""
            artist_list = []
            resource_contr_list=[]
            if child.tag == "SoundRecording":
                isrc_tag = child.find("SoundRecordingId/ISRC")
                if self.check_for_none(isrc_tag):
                    isrc = isrc_tag.text

                song[isrc] = {}

                resource_ref_tag = child.find("ResourceReference")
                if self.check_for_none(resource_ref_tag):
                    song[isrc]["resource_ref"] = resource_ref_tag.text

                resource_ref_title_tag = child.find("ReferenceTitle/TitleText")
                if self.check_for_none(resource_ref_title_tag):
                    song[isrc]["resource_ref_title"] = resource_ref_title_tag.text

                lang_of_perf_tag = child.find("LanguageOfPerformance")
                if self.check_for_none(lang_of_perf_tag):
                    song[isrc]["lang_of_perf"] = lang_of_perf_tag.text

                duration_tag = child.find("Duration")
                if self.check_for_none(duration_tag):
                    song[isrc]["duration"] = duration_tag.text

                sound_rec_det_terr_tag = child.find("SoundRecordingDetailsByTerritory")

                territory_code_tag = child.find("SoundRecordingDetailsByTerritory/TerritoryCode")
                if self.check_for_none(territory_code_tag):
                    song[isrc]["territory_code"] = territory_code_tag.text
                # print("====================")

                tech_sound_rec_det = {}
                for soud_rec in sound_rec_det_terr_tag:
                    artist = {}
                    artist["artist_name"] = ""
                    resource_contr = {}
                    resource_contr['artist_name'] = ""
                    title_tag = soud_rec.find("TitleText")
                    if self.check_for_none(title_tag):
                        song[isrc]["title"] = title_tag.text

                    if soud_rec.tag == "DisplayArtist":
                        partyname_tag = soud_rec.find("PartyName/FullName")

                        if self.check_for_none(partyname_tag):
                            artist["artist_name"] = partyname_tag.text
                            artist["sequence_number"] = soud_rec.attrib['SequenceNumber']
                        artist["artist_role_list"] = []
                        artistrole_tag = soud_rec.findall("ArtistRole")
                        for artistr in artistrole_tag:
                           artist["artist_role_list"].append(artistr.text)
                        artist_list.append(artist)
                    if soud_rec.tag == "ResourceContributor":
                        partyname_tag = soud_rec.find("PartyName/FullName")

                        if self.check_for_none(partyname_tag):
                            resource_contr['artist_name'] = partyname_tag.text

                        resource_contr["artist_role_list"] = []
                        resource_contr_role_tag = soud_rec.findall("ResourceContributorRole")

                        for contr in resource_contr_role_tag:
                            if contr.text=="UserDefined":
                                resource_contr["artist_role_list"].append(contr.attrib['UserDefinedValue'])
                            else:
                                resource_contr["artist_role_list"].append(contr.text)
                        resource_contr_list.append(resource_contr)
                    if soud_rec.tag == "DisplayArtistName":
                        song[isrc]["display_artist_name"] = soud_rec.text
                    if soud_rec.tag == "LabelName":
                        song[isrc]["label_name"] = soud_rec.text
                    if soud_rec.tag == "Genre":
                        genre_tag = soud_rec.find("GenreText")
                        song[isrc]["genre_name"] = genre_tag.text
                    if soud_rec.tag == "PLine":
                        pline_text_tag = soud_rec.find("PLineText")
                        song[isrc]["pline_text"] = pline_text_tag.text
                        year_tag = soud_rec.find("Year")
                        song[isrc]["year"] = year_tag.text
                    if soud_rec.tag == "ParentalWarningType":
                        song[isrc]["parental_warning_type"] = soud_rec.text

                    if soud_rec.tag == "TechnicalSoundRecordingDetails":
                        is_preview = soud_rec.find("IsPreview")
                        if is_preview.text == "false":
                            audio_codec_type = soud_rec.find("AudioCodecType")
                            tech_sound_rec_det["audio_codec_type"] = audio_codec_type.text
                            tech_resource_det_ref = soud_rec.find("TechnicalResourceDetailsReference")
                            tech_sound_rec_det["tech_resource_details_reference"] = tech_resource_det_ref.text
                            num_of_channels = soud_rec.find("NumberOfChannels")
                            tech_sound_rec_det["num_of_channels"] = num_of_channels.text
                            sampling_rates = soud_rec.find("SamplingRate")
                            tech_sound_rec_det["sampling_rates"] = sampling_rates.text+ sampling_rates.attrib["UnitOfMeasure"]
                            bits_per_sample = soud_rec.find("BitsPerSample")
                            tech_sound_rec_det["bits_per_sample"] = bits_per_sample.text
                            url = soud_rec.find("File/URL")
                            tech_sound_rec_det["url"] = url.text
                            hashsum = soud_rec.find("File/HashSum/HashSum")
                            tech_sound_rec_det["hashsum"] = hashsum.text
                            hash_alog_type = soud_rec.find("File/HashSum/HashSumAlgorithmType")
                            tech_sound_rec_det["hash_alog_type"] = hash_alog_type.text

                song[isrc]["artist"] = artist_list
                song[isrc]["resource_contr"] = resource_contr_list
                song[isrc]["tech_sound_rec_det"] = tech_sound_rec_det



        data = {}
        data['song'] = song
        data['image'] = image
        return data

    def process_release_list(self, root):
        self.logInfo("PROCESSING REALEASE LIST")
        for child in root:
            grid_id_tag = child.find('ReleaseId/GRid')
            grid_id = ""
            if self.check_for_none(grid_id_tag):
                grid_id = grid_id_tag.text

            icpn_tag = child.find('ReleaseId/ICPN')
            icpn = ""

            if self.check_for_none(icpn_tag):
                icpn = icpn_tag.text

            catalog_number_tag = child.find("ReleaseId/CatalogNumber")
            catalog_number = ""

            if self.check_for_none(catalog_number_tag):
                catalog_number = catalog_number_tag.text

            release_reference_tag = child.find("ReleaseReference")
            release_reference = ""

            if self.check_for_none(release_reference_tag):
                release_reference = release_reference_tag.text

            reference_title_tag = child.find("ReferenceTitle")
            language_and_script_code = ""
            title_text = ""
            sub_title_text = ""

            if self.check_for_none(release_reference_tag):
                language_and_script_code = reference_title_tag.attrib['LanguageAndScriptCode']
                title_text_tag = reference_title_tag.find('TitleText')

                if self.check_for_none(title_text_tag):
                    title_text = title_text_tag.text

                sub_title_text_tag = reference_title_tag.find('SubTitle')

                if self.check_for_none(sub_title_text_tag):
                    sub_title_text = sub_title_text_tag.text
                    # print(sub_title_text)

            release_resource_ref_tag = child.find("ReleaseResourceReferenceList")
            release_resource_ref_list = []
            for release_resource_ref_child in release_resource_ref_tag:
                release_resource_type = release_resource_ref_child.attrib['ReleaseResourceType']
                release_resource_ref_dic = {}
                release_resource_ref_dic['value'] = release_resource_ref_child.text
                release_resource_ref_dic['release_resource_type'] = release_resource_type
                release_resource_ref_list.append(release_resource_ref_dic)

            release_type_tag = child.find("ReleaseType")
            release_type = ""

            if self.check_for_none(release_type_tag):
                release_type = release_type_tag.text
                # print(release_type)

            release_details_by_territory_tag = child.find("ReleaseDetailsByTerritory")
            territory_code = ""
            display_artist_name = ""
            parent_warning = ""
            label_name = ""
            display_title = ""
            genre = ""
            if self.check_for_none(release_details_by_territory_tag):
                territory_code_tag = release_details_by_territory_tag.find("TerritoryCode")
                if self.check_for_none(territory_code_tag):
                    territory_code = territory_code_tag.text

                display_artist_name_tag = release_details_by_territory_tag.find("DisplayArtistName")
                if self.check_for_none(display_artist_name_tag):
                    display_artist_name = display_artist_name_tag.text

                label_name_tag = release_details_by_territory_tag.find("LabelName")
                if self.check_for_none(label_name_tag):
                    label_name = label_name_tag.text

                display_title_tag = release_details_by_territory_tag.find("Title/TitleText")
                if self.check_for_none(display_title_tag):
                    display_title = display_title_tag.text

                parent_warning_tag = release_details_by_territory_tag.find('ParentalWarningType')
                if self.check_for_none(parent_warning_tag):
                    parent_warning = parent_warning_tag.text

                genre_tag = release_details_by_territory_tag.find("Genre/GenreText")
                if self.check_for_none(genre_tag):
                    genre = genre_tag.text

            duration_tag = child.find("Duration")
            duration = ""
            if self.check_for_none(duration_tag):
                duration = duration_tag.text

            pline_year_tag = child.find("PLine/Year")
            year = ""
            if self.check_for_none(pline_year_tag):
                year = pline_year_tag.text

            pline_text_tag = child.find("PLine/PLineText")
            pline_text = ""
            if self.check_for_none(pline_text_tag):
                pline_text = pline_text_tag.text

            global_original_date_tag = child.find("GlobalOriginalReleaseDate")
            global_original_date = ""
            if self.check_for_none(global_original_date_tag):
                global_original_date = global_original_date_tag.text

            album = {}
            if release_type == "Album":
                album[release_reference] = {}
                album[release_reference]['grid'] = grid_id
                album[release_reference]['icpn'] = icpn
                album[release_reference]['catalog_number'] = catalog_number
                album[release_reference]['title_text'] = title_text
                album[release_reference]['global_original_release_date'] = global_original_date
                album[release_reference]['release_resource_reference'] = release_resource_ref_list
                album[release_reference]['year'] = year
                album[release_reference]['label'] = pline_text
                album[release_reference]['genre'] = genre
                album[release_reference]['release_type'] = release_type
                album[release_reference]['territory_code'] = territory_code
                album[release_reference]['display_artist_name'] = display_artist_name
                album[release_reference]['label_name'] = label_name
                album[release_reference]['parent_warning'] = parent_warning
                album[release_reference]['duration'] = duration
                album[release_reference]['display_title'] = display_title
                album[release_reference]['language_and_script_code'] = language_and_script_code
                album[release_reference]['sub_title'] = sub_title_text
            return album

    def process_deal_list(self, root):
        self.logInfo("PROCESSING DEAL LIST")
        deal_dict = {}
        for child in root:
            deal_release_ref = child.find('DealReleaseReference')
            deal_dict[deal_release_ref.text] = []
            deals = child.findall('Deal/DealTerms')
            for d in deals:
                dict = {}
                commercial_model_type_tag = d.find('CommercialModelType')
                dict["commercial_model_type"] = ""
                if self.check_for_none(commercial_model_type_tag):
                    dict["commercial_model_type"] = commercial_model_type_tag.text
                dict["usage"] = []
                usetype_tag = d.findall('Usage/UseType')
                for u in usetype_tag:
                    dict["usage"].append(u.text)
                territory_code_tag = d.find('TerritoryCode')
                if self.check_for_none(territory_code_tag):
                    dict["territory_code"] = territory_code_tag.text
                validity_tag = d.find('ValidityPeriod/StartDate')
                if self.check_for_none(validity_tag):
                    dict["validity_period"] = validity_tag.text
                takedown_tag = d.find('TakenDown')
                dict["validity_end_period"] =""
                if self.check_for_none(takedown_tag):
                    dict["validity_end_period"] =validity_tag.text
                deal_dict[deal_release_ref.text].append(dict)
        return deal_dict

    def parse_xml(self):
        process_xml = {}

        for child in self.__root:
            if child.tag == "MessageHeader":
                process_xml['messge'] = self.process_message_header(child)

            if child.tag == "ReleaseList":
                process_xml["release_list"] = self.process_release_list(child)

            if child.tag == "ResourceList":
                process_xml["resource_lis"] = self.process_resource_list(child)

            if child.tag == "DealList":
                process_xml['deal'] = self.process_deal_list(child)
            if child.tag == "UpdateIndicator":
                process_xml['UpdateIndicator'] =child.text
        print(json.dumps(process_xml,indent=4, sort_keys=True))

args = {"xmlpath":"A10301A00041017971.xml","debug":"DEBUG"}
ddex = DDEXParser(args)
ddex.parse_xml()