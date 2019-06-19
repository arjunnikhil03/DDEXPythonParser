# DDEX Python Parser
DDEX Python Parser Can be use for Parsing DDEX XML FILE.Output is in JSON Format.

it is been tested on:-
* Sony Music DDEX XML
* Universal Music DDEX XML
* EMI Music DDEX XML
* WARNER Music DDEX XML
* Fox Star DDEX XML
* WB DDEX XML

```python
#Just Pass DDEX Xml Path 
args = {"xmlpath":"A10301A00041017971.xml","debug":"DEBUG"}
ddex = DDEXParser(args)
ddex.parse_xml()
```

Comment json dump line inorder to return output in dictonary format

```python
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
        # Comment json dump line inorder to retun output in dictonary format
        print(json.dumps(process_xml,indent=4, sort_keys=True))
```
