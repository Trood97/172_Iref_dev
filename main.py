from pydantic import BaseModel
import fastapi
from modules.ExternalServices import ExternalServs
from modules.similarityscore import similaritycheck
from fastapi.middleware.cors import CORSMiddleware

import logging


#Trood97 from local says hi!!!

#dev2 has made some changes


logging.basicConfig(filename='logs.txt', filemode='a', level=10,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logging.info('\n')

app = fastapi.FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)
class Reference(BaseModel):
    reference: list = [{"id": "", "refstring": ""}]
    referenceStyle: str = ""

@app.post('/ref')
async def post_Reference(reference:Reference):
    try:
        logging.info('Entered post reference module')
        ref = reference.reference
        a = ExternalServs()
        final_output = []
        interval = 20
        flist = []
        for i in range(0, len(ref), interval):
            sub_list = ref[i:i + interval]
            flist.append((sub_list))
        for v in flist:
            print(v)
            print('####')
        bibid = ''
        logging.info('reflist is ready for web scraping(External Search)')
        for i in flist:
            logging.info(f'input references no.:{len(i)}')
            js = a.ExternalSearch(i)
            for pq in js:
                logging.info(f'bibid entered : {bibid}')
                if pq.get('InternalBibId') == bibid:
                    continue
                if pq.get('CompleteReference') == 'true' and pq.get('SearchSystem') == 'PubMed':
                    if pq.get("InternalBibId") is not None:
                        Id = pq['InternalBibId']
                    else:
                        Id = ""

                    if pq.get("ComparedReferenceString") is not None:
                        td = pq.get("ComparedReferenceString")
                    else:
                        td = ""
                    if pq.get("CompleteReference") == 'true':
                        status = 'Complete'
                    else:
                        status = 'Incomplete'

                    dict01 = {}
                    if pq.get("type".lower()) == 'journal':
                        mongoninsertlist = []  # just a list to insert to mongodb

                        if pq.get("authors") is not None:
                            author1 = []
                            sm = pq.get("authors")
                            for sa in sm:
                                dict_2 = {}
                                if sa.get("lastname") is not None:
                                    dict_2["lastname"] = sa.get("lastname")
                                else:
                                    dict_2["lastname"] = ""
                                if sa.get("firstname") is not None:
                                    dict_2["firstname"] = sa.get("firstname")
                                else:
                                    dict_2["firstname"] = ""
                                author1.append(dict_2)
                                dict01["authors"] = author1
                        else:
                            dict01["authors"] = []

                        if pq.get("groups") is not None:
                            groups1 = []
                            nm = pq.get("groups")
                            dict_3 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_3["lastname"] = np.get("lastname")
                                else:
                                    dict_3["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_3["firstname"] = np.get("firstname")
                                else:
                                    dict_3["firstname"] = ""
                                groups1.append(dict_3)
                                dict01["groups"] = groups1

                        else:
                            dict01["groups"] = []

                        if pq.get("firstPage") is not None:
                            dict01["firstPage"] = pq.get("firstPage")
                        else:
                            dict01["firstPage"] = ""
                        if pq.get("lastPage") is not None:
                            dict01["lastPage"] = pq.get("lastPage")
                        else:
                            dict01["lastPage"] = ""
                        if pq.get("issue") is not None:
                            dict01["issue"] = pq.get("issue")
                        else:
                            dict01["issue"] = ""

                        if pq.get("CompleteReference") == 'true':
                            status = 'Complete'
                        else:
                            status = 'Incomplete'

                        if pq.get("PubMedId") is not None:
                            PubMedId = pq.get("PubMedId")
                        else:
                            PubMedId = ""

                        if pq.get("journalTitle") is not None:
                            dict01["journalTitle"] = pq.get("journalTitle")
                        else:
                            dict01["journalTitle"] = ""
                        if pq.get("articleTitle") is not None:
                            dict01["articleTitle"] = pq.get("articleTitle")
                        else:
                            dict01["articleTitle"] = ""
                        dict01["type"] = pq.get("type")

                        if pq.get("Doi".lower()) is not None:
                            dict01["url"] = pq.get("Doi".lower())[5::]
                        else:
                            dict01["url"] = ""
                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("elocator") is not None:
                            dict01["elocator"] = pq.get("elocator")
                        else:
                            dict01["elocator"] = ""
                        if pq.get("year") is not None:
                            dict01["year"] = pq.get("year")
                        dict01["referencestyle"] = reference.referenceStyle

                        res = a.Restructuring(dict01)

                        print(dict01)
                        final_output.append(
                            {"id": Id, 'Status': status, 'PubMedId': PubMedId, "Sliced_Reference": dict01,
                             "Structured_Reference": res, "Track_Changes_Reference": td})
                        bibid = Id
                        continue

                    elif pq.get('type'.lower()) == 'book':
                        mongodbinsertbook = []

                        if pq.get("authors") is not None:
                            author1 = []
                            sm = pq.get("authors")
                            for sa in sm:
                                dict_2 = {}
                                if sa.get("lastname") is not None:
                                    dict_2["lastname"] = sa.get("lastname")
                                else:
                                    dict_2["lastname"] = ""
                                if sa.get("firstname") is not None:
                                    dict_2["firstname"] = sa.get("firstname")
                                else:
                                    dict_2["firstname"] = ""
                                author1.append(dict_2)
                                dict01["authors"] = author1
                        else:
                            dict01["authors"] = []

                        if pq.get("editors") is not None:
                            editors1 = []
                            nm = pq.get("editors")
                            dict_4 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_4["lastname"] = np.get("lastname")
                                else:
                                    dict_4["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_4["firstname"] = np.get("firstname")
                                else:
                                    dict_4["firstname"] = ""
                                editors1.append(dict_4)
                                dict01["groups"] = editors1
                        else:
                            dict01["editors"] = []
                        if pq.get("groups") is not None:
                            groups1 = []
                            nm = pq.get("groups")
                            dict_3 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_3["lastname"] = np.get("lastname")
                                else:
                                    dict_3["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_3["firstname"] = np.get("firstname")
                                else:
                                    dict_3["firstname"] = ""
                                groups1.append(dict_3)
                                dict01["groups"] = groups1
                        else:
                            dict01["groups"] = []
                        # if pq.get("groups") is not None:
                        #     dict["groups"] = pq.get("groups")
                        # else:
                        #     dict["groups"] = []
                        if pq.get("firstPage") is not None:
                            dict01["firstPage"] = pq.get("firstPage")
                        else:
                            dict01["firstPage"] = ""
                        if pq.get("lastPage") is not None:
                            dict01["lastPage"] = pq.get("lastPage")
                        else:
                            dict01["lastPage"] = ""

                        if pq.get("CompleteReference") == 'true':
                            status = 'Complete'
                        else:
                            status = 'Incomplete'

                        if pq.get("PubMedId") is not None:
                            PubMedId = pq.get("PubMedId")
                        else:
                            PubMedId = ""

                        if pq.get("bookTitle") is not None:
                            dict01["bookTitle"] = pq.get("bookTitle")
                        else:
                            dict01["bookTitle"] = ""
                        if pq.get("chapterTitle") is not None:
                            dict01["chapterTitle"] = pq.get("chapterTitle")
                        else:
                            dict01["chapterTitle"] = ""
                        if pq.get("type") is not None:
                            dict01["type"] = pq.get("type")
                        else:
                            dict01["type"] = ""

                        # dict01["referencestyle"] = reference.referenceStyle

                        if pq.get("doi") is not None:
                            dict01["url"] = pq.get("doi")
                        else:
                            dict01["url"] = ""

                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("year") is not None:
                            dict01["year"] = pq.get("year")
                        else:
                            dict01["year"] = ""

                        if pq.get("edition") is not None:
                            dict01["edition"] = pq.get("edition")
                        else:
                            dict01["edition"] = ""
                        if pq.get("publisherLocation") is not None:
                            dict01["publisherLocation"] = pq.get("publisherLocation")
                        else:
                            dict01["publisherLocation"] = ""
                        if pq.get("publisherName") is not None:
                            dict01["publisherName"] = pq.get("publisherName")
                        else:
                            dict01["publisherName"] = ""
                        dict01["referencestyle"] = reference.referenceStyle
                        res = a.Restructuring(dict01)

                        print(dict01)
                        final_output.append(
                            {"id": Id, 'Status': status, 'PubMedId': PubMedId, "Sliced_Reference": dict01,
                             "Structured_Reference": res, "Track_Changes_Reference": td})
                        bibid = Id
                        continue





                if pq.get('CompleteReference') == 'true' and pq.get('SearchSystem') == 'CrossRef':
                    if pq.get("InternalBibId") is not None:
                        Id = pq['InternalBibId']
                    else:
                        Id = ""

                    if pq.get("ComparedReferenceString") is not None:
                        td = pq.get("ComparedReferenceString")
                    else:
                        td = ""
                    if pq.get("CompleteReference") == 'true':
                        status = 'Complete'
                    else:
                        status = 'Incomplete'

                    dict01 = {}
                    if pq.get("type".lower()) == 'journal':
                        mongoninsertlist = []  # just a list to insert to mongodb

                        if pq.get("authors") is not None:
                            author1 = []
                            sm = pq.get("authors")
                            for sa in sm:
                                dict_2 = {}
                                if sa.get("lastname") is not None:
                                    dict_2["lastname"] = sa.get("lastname")
                                else:
                                    dict_2["lastname"] = ""
                                if sa.get("firstname") is not None:
                                    dict_2["firstname"] = sa.get("firstname")
                                else:
                                    dict_2["firstname"] = ""
                                author1.append(dict_2)
                                dict01["authors"] = author1
                        else:
                            dict01["authors"] = []

                        if pq.get("groups") is not None:
                            groups1 = []
                            nm = pq.get("groups")
                            dict_3 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_3["lastname"] = np.get("lastname")
                                else:
                                    dict_3["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_3["firstname"] = np.get("firstname")
                                else:
                                    dict_3["firstname"] = ""
                                groups1.append(dict_3)
                                dict01["groups"] = groups1

                        else:
                            dict01["groups"] = []

                        if pq.get("firstPage") is not None:
                            dict01["firstPage"] = pq.get("firstPage")
                        else:
                            dict01["firstPage"] = ""
                        if pq.get("lastPage") is not None:
                            dict01["lastPage"] = pq.get("lastPage")
                        else:
                            dict01["lastPage"] = ""
                        if pq.get("issue") is not None:
                            dict01["issue"] = pq.get("issue")
                        else:
                            dict01["issue"] = ""

                        if pq.get("CompleteReference") == 'true':
                            status = 'Complete'
                        else:
                            status = 'Incomplete'

                        if pq.get("PubMedId") is not None:
                            PubMedId = pq.get("PubMedId")
                        else:
                            PubMedId = ""

                        if pq.get("journalTitle") is not None:
                            dict01["journalTitle"] = pq.get("journalTitle")
                        else:
                            dict01["journalTitle"] = ""
                        if pq.get("articleTitle") is not None:
                            dict01["articleTitle"] = pq.get("articleTitle")
                        else:
                            dict01["articleTitle"] = ""
                        dict01["type"] = pq.get("type")

                        if pq.get("Doi".lower()) is not None:
                            dict01["url"] = pq.get("Doi".lower())[5::]
                        else:
                            dict01["url"] = ""
                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("elocator") is not None:
                            dict01["elocator"] = pq.get("elocator")
                        else:
                            dict01["elocator"] = ""
                        if pq.get("year") is not None:
                            dict01["year"] = pq.get("year")
                        dict01["referencestyle"] = reference.referenceStyle

                        res = a.Restructuring(dict01)

                        print(dict01)
                        final_output.append(
                            {"id": Id, 'Status': status, 'PubMedId': PubMedId, "Sliced_Reference": dict01,
                             "Structured_Reference": res, "Track_Changes_Reference": td})
                        bibid = Id
                        continue

                    elif pq.get('type'.lower()) == 'book':
                        mongodbinsertbook = []

                        if pq.get("authors") is not None:
                            author1 = []
                            sm = pq.get("authors")
                            for sa in sm:
                                dict_2 = {}
                                if sa.get("lastname") is not None:
                                    dict_2["lastname"] = sa.get("lastname")
                                else:
                                    dict_2["lastname"] = ""
                                if sa.get("firstname") is not None:
                                    dict_2["firstname"] = sa.get("firstname")
                                else:
                                    dict_2["firstname"] = ""
                                author1.append(dict_2)
                                dict01["authors"] = author1
                        else:
                            dict01["authors"] = []

                        if pq.get("editors") is not None:
                            editors1 = []
                            nm = pq.get("editors")
                            dict_4 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_4["lastname"] = np.get("lastname")
                                else:
                                    dict_4["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_4["firstname"] = np.get("firstname")
                                else:
                                    dict_4["firstname"] = ""
                                editors1.append(dict_4)
                                dict01["groups"] = editors1
                        else:
                            dict01["editors"] = []
                        if pq.get("groups") is not None:
                            groups1 = []
                            nm = pq.get("groups")
                            dict_3 = {}
                            for np in nm:
                                if np.get("lastname") is not None:
                                    dict_3["lastname"] = np.get("lastname")
                                else:
                                    dict_3["lastname"] = ""
                                if np.get("firstname") is not None:
                                    dict_3["firstname"] = np.get("firstname")
                                else:
                                    dict_3["firstname"] = ""
                                groups1.append(dict_3)
                                dict01["groups"] = groups1
                        else:
                            dict01["groups"] = []
                        # if pq.get("groups") is not None:
                        #     dict["groups"] = pq.get("groups")
                        # else:
                        #     dict["groups"] = []
                        if pq.get("firstPage") is not None:
                            dict01["firstPage"] = pq.get("firstPage")
                        else:
                            dict01["firstPage"] = ""
                        if pq.get("lastPage") is not None:
                            dict01["lastPage"] = pq.get("lastPage")
                        else:
                            dict01["lastPage"] = ""

                        if pq.get("CompleteReference") == 'true':
                            status = 'Complete'
                        else:
                            status = 'Incomplete'

                        if pq.get("PubMedId") is not None:
                            PubMedId = pq.get("PubMedId")
                        else:
                            PubMedId = ""

                        if pq.get("bookTitle") is not None:
                            dict01["bookTitle"] = pq.get("bookTitle")
                        else:
                            dict01["bookTitle"] = ""
                        if pq.get("chapterTitle") is not None:
                            dict01["chapterTitle"] = pq.get("chapterTitle")
                        else:
                            dict01["chapterTitle"] = ""
                        if pq.get("type") is not None:
                            dict01["type"] = pq.get("type")
                        else:
                            dict01["type"] = ""

                        # dict01["referencestyle"] = reference.referenceStyle

                        if pq.get("doi") is not None:
                            dict01["url"] = pq.get("doi")
                        else:
                            dict01["url"] = ""

                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("volume") is not None:
                            dict01["volume"] = pq.get("volume")
                        else:
                            dict01["volume"] = ""
                        if pq.get("year") is not None:
                            dict01["year"] = pq.get("year")
                        else:
                            dict01["year"] = ""

                        if pq.get("edition") is not None:
                            dict01["edition"] = pq.get("edition")
                        else:
                            dict01["edition"] = ""
                        if pq.get("publisherLocation") is not None:
                            dict01["publisherLocation"] = pq.get("publisherLocation")
                        else:
                            dict01["publisherLocation"] = ""
                        if pq.get("publisherName") is not None:
                            dict01["publisherName"] = pq.get("publisherName")
                        else:
                            dict01["publisherName"] = ""
                        dict01["referencestyle"] = reference.referenceStyle
                        res = a.Restructuring(dict01)

                        print(dict01)
                        final_output.append(
                            {"id": Id, 'Status': status, 'PubMedId': PubMedId, "Sliced_Reference": dict01,
                             "Structured_Reference": res, "Track_Changes_Reference": td})
                        bibid = Id
                        continue
                print('*******')

            print('#####################################')
            logging.info('json pack processed')
        logging.info('exiting program execution')
        return {"Success": "true", "output": final_output}  # dispalying final output

    except Exception as e:
        logging.info(f'Exception: {e}')
        return 'some error occured, please try again'

