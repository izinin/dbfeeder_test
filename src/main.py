import webapp2
import os
import jinja2
import parse_xlsx as parser
import datamodel
import json
from google.appengine.ext import db
from _ast import Pass

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
# not to conflicting with angular
jinja_environment.variable_start_string='{['
jinja_environment.variable_end_string=']}'

class MainPage(webapp2.RequestHandler):
    def __init__(self, request, response):
        super(MainPage, self).__init__(request, response)
        self.initialize(request, response)
        self.template = jinja_environment.get_template('index.html')
    
    def get(self):
        self.response.out.write(self.template.render())
    
    def post(self):
        buf = self.request.get('xlsinput')
        if len(buf) > 0:
            #try:
                self.response.headers['Content-Type'] = 'application/json'
                result = parser.importFromBuffer(buf)
                return webapp2.redirect("/")
                self.response.out.write(result)
            #except Exception: 
            #    self.response.out.write('{"Error" : "invalid file data"}')                         
        else:
            self.response.out.write(self.template.render())                         

class ServiceData(webapp2.RequestHandler):
    def get(self):
        filter = None
        try:
            filter = json.loads(self.request.get('filter'))
        except Exception:
            Pass
        if not filter:   
            self.response.out.write('{"Error" : "missing parameter \"filter\"}')
            return
    
        query = datamodel.Product.all()        
        data = [{"product":
                 {
                  "EAN": x.ean,
                    "Brand": x.brand,
                    "Name": x.name,
                    "Category": x.category,
                    "SubCategory": x.subcategory,
                    "INCI": x.inci,
                    "Photo": "*not supported*",
                    "Description": x.description
                  }
                 } for x in query.run() if filter["value"] == "ALL" or x.category.startswith(filter["value"])]
        result = {"store": data}
        self.response.out.write(json.dumps(result))

class WipeDbase(webapp2.RequestHandler):
    def get(self):
        db.delete(datamodel.Product.all().run(keys_only=True))
        return webapp2.redirect("/")

application = webapp2.WSGIApplication([
    ('/deletedata', WipeDbase),
    ('/readdb', ServiceData),
    ('/', MainPage)
], debug=True)