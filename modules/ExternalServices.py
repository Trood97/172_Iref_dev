import json
import requests
import xml.etree.ElementTree as ET
import re

class ExternalServs:
    def ExternalSearch(self,input):

        url = "https://irefservices.icodex.in/find/references"
        payload = json.dumps(input)

        files = [

        ]
        headers = {
            'iRefRefApiKey': 'APIKEYFORIREFPRODUCT',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.status_code)
        data = response.json()
        jsonData = json.loads(data["JsonData"])
        return jsonData

    def Restructuring(self,dict01):
        url = "https://irefservices.icodex.in/iref/reference/restructure"

        payload = json.dumps(dict01)
        headers = {
            'JID': 'ASAP',
            'eAssistantXApiKey': 'CUCCLI11UI#AB',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        restructredjson = response.json()
        res = (restructredjson["Reference"])
        return res


    def slicinginput(self,input:str):
        url = 'http://autostyling.icodex.in:8070/api/processCitation'

        new_string,final_string= '',''            #for removing . after page number first-lage
        for i in input.split(' '):
            new_string = re.sub(r'(\d+)(–)(\d+)\.', r'\1\2\3', str(i))
            new_string = re.sub(r'(\d+)(-)(\d+)\.', r'\1\2\3', new_string)
            final_string += new_string + ' '



        payload = {'citations':final_string}      #final_string with removed . after page first-last
        response = requests.request("POST", url, data=payload)
        data = response.text
        file1 = open('sliced.xml', "w")
        file1.write(data)
        file1.close()

        tree = ET.parse('sliced.xml', parser=ET.XMLParser(encoding='iso-8859-5'))
        root = tree.getroot()

        persName = tree.findall('monogr')
        dictfinal = {}
        list1 = []
        str1 = ''
        dictfinal["authors"] = []
        dictfinal["groups"] = []
        dictfinal["firstPage"] =""
        dictfinal["lastPage"]= ""
        dictfinal["issue"]= ""
        dictfinal["journalTitle"]= ""
        dictfinal["articleTitle"] = ""
        dictfinal["type"] = ""
        dictfinal["url"] = ""
        dictfinal["volume"] = ""
        dictfinal["elocator"] = ""
        dictfinal["year"] =  ""
        for i in persName:
            for j in i:
                # print(j)
                if j.tag == 'title':
                    if j.text is not None:
                        dictfinal['journalTitle'] = j.text
                    else:
                        pass
                if j.tag == 'author':

                    for a in j:
                        dict2 = {}

                        for auth in a:
                            if auth.attrib.get('type') == 'first' or auth.attrib.get('type') == 'middle':
                                firstname = str1 + str(auth.text)
                                str1 = str(auth.text)

                                dict2['firstname'] = firstname
                            if auth.tag == 'surname':
                                lastname = auth.text
                                dict2['lastname'] = lastname

                        list1.append(dict2)

                    dictfinal['authors'] = list1

                if j.tag == 'idno':
                    if j.text is not None:
                        dictfinal['url'] = j.text
                    else:
                        pass

                if j.tag == 'imprint':
                    for ab in j:
                        # print(ab)
                        if ab.tag == 'date':
                            x = ab.text
                            dictfinal['year'] = x

                        if ab.tag == 'biblScope':
                            if ab.attrib.get('unit') == 'volume':
                                y = ab.text
                                dictfinal['volume'] = y

                        if ab.attrib.get('from') is not None:
                            dictfinal['firstPage'] = ab.attrib.get('from')

                        if ab.attrib.get('to') is not None:
                            dictfinal['lastPage'] = ab.attrib.get('to')


        return dictfinal










