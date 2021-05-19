from mongoengine import connect
from mongoengine import *
import json
import numpy as np
import uuid


class Documents(Document):
    id_doc = StringField(required=True, unique=True)
    pattern_name = StringField(required=True, unique=True)
    keyword = StringField(required=True, unique=False)
    type = StringField(required=True, unique=False)
    image_sample = StringField(required=True, unique=False)
    attribute = ListField()



class Connector:
    def __init__(self,name):
        connect(name)

    #-------------add------------------
    def add_documents(self,data):
        try:
            id_doc=str(uuid.uuid4())
            Documents(
                id_doc = id_doc,
                pattern_name=data["pattern_name"],
                keyword=data["keyword"],
                type = data["type"],
                image_sample = data["image_sample"],
                attribute = data["attribute"]
            
            ).save()
            return id_doc
        except Exception as e:
            print(e)
            return "-1"
        
      
    #-----------------get--------------------------------
    def get_documents(self):
        documents=[]
        docs = Documents.objects()
        for x in docs:
            documents.append({"pattern_name":x.pattern_name,"keyword":x.keyword,"type":x.type,"image_sample":x.image_sample,"attribute":x.attribute})

        return documents
    def get_pattern_names(self):
        pattern_names=[]
        docs = Documents.objects()
        for x in docs:
            pattern_names.append(x.pattern_name)

        return pattern_names

    def get_document(self,pattern_name):
        documents=[]
        docs = Documents.objects(pattern_name=pattern_name)
        for x in docs:
            documents.append({"pattern_name":x.pattern_name,"keyword":x.keyword,"type":x.type,"image_sample":x.image_sample,"attribute":x.attribute})

        return documents

       

    

if __name__ == "__main__":
 pass  