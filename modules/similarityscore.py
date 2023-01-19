from thefuzz import fuzz
import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017/")
ddddbbbb = client['ICODEX-DB01']
collection = ddddbbbb['Journal02']







DICT = {


                "type": "Journal",

                "authors": [

                    {

                        "lastname": "Becker",

                        "firstname": "KD"

                    },

                    {

                        "lastname": "Bradshaw",

                        "firstname": "CP"

                    },

                    {

                        "lastname": "Domitrovich",

                        "firstname": "C"

                    },

                    {

                        "lastname": "Ialongo",

                        "firstname": "NS"

                    }

                ],

                "groups": [{

            "groupname": "Research Group"

        },

        {

            "groupname": "The Metropolitan Area Child Study Research Group"

        }],

                "firstPage": "482",

                "lastPage": "493",

                "issue": "6",

                "journalTitle": "Administration and policy in mental health",

                "articleTitle": "Coaching teachers to improve implementation of the good behavior game.",

                "doi": "10.1007/s10488-013-0482-8",

                "volume": "40",

                "year": "2013"

            }


class similaritycheck:   # to compare sliced input reference and the existing documents in the goldendatabase
    def __init__(self,dict1):    #doi1 = first we compare doi , if doi = "" ,then we compare the whole values
        self.dict1 = (dict1)


    def doiquest(self):
        doi = self.dict1.get('url')
        if doi != 'None':
            query = collection.find({'url':str(doi)})
            for i in query:
                del i['_id']
                return i

        elif doi == 'None':
            for i in collection.find():
                del i['_id']
                sample1 = str(self.dict1)
                sample2 = str(i)
                comparision = int(fuzz.ratio(sample1, sample2))
                if (comparision) > 90:
                    print(comparision)
                    return i
        else:
            return 'not found'

