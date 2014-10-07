import json
from google.appengine.ext import db
from google.appengine.api import memcache

class Product(db.Model):
    docHeaderMap = ["Category",
                        "Sub-category",
                        "INCI",
                        "Photo",
                        "EAN",
                        "Brand name",
                        "Product name",
                        "Product description"]

    category = db.StringProperty(multiline=True)
    subcategory = db.StringProperty(multiline=True)
    inci = db.StringProperty(multiline=True)
    photo = db.BlobProperty()
    ean = db.StringProperty(multiline=True)
    brand = db.StringProperty(multiline=True)
    name = db.StringProperty(multiline=True)
    description = db.StringProperty(multiline=True)
    
    def setFieldData(self, fieldName, value):
        if not value:
            return False
        
        result = True
        if fieldName == "Category":
            self.category = value
        elif fieldName == "Sub-category":
            self.subcategory = value
        elif fieldName == "INCI":
            self.inci = value
        elif fieldName == "Photo":
            self.photo = value
        elif fieldName == "EAN":
            self.ean = value
        elif fieldName == "Brand name":
            self.brand = value
        elif fieldName == "Product name":
            self.name = value
        elif fieldName == "Product description":
            self.description = value
        else:
            result = False
        return result
            
        
