import zipfile
import io
import json
from xml.etree.ElementTree import iterparse
import datamodel
from _ast import Pass

def xlsx(fname):
    z = zipfile.ZipFile(fname)
    strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for e, el in iterparse(z.open('xl/worksheets/sheet1.xml')):
        if el.tag.endswith('}v'): # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                value = strings[int(value)]
            letter = el.attrib['r'] # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows

def saveToDb(data, filter):
    if len(data) < 2 :
        raise Exception("Invalid document format")
    headers = [(letter, column.strip()) for (letter, column) in data[0].items() if column.strip() in filter]
    result = []
    for dict in data[1:]:
        row = datamodel.Product()
        isNeedToSave = False
        for (letter, headerName) in headers:
            if dict.has_key(letter) and dict[letter]:
                isNeedToSave = row.setFieldData(headerName, dict[letter])
        if isNeedToSave:
            row.put()
        
#        row = []
#        for (letter, headerName) in headers:
#            if dict.has_key(letter) and dict[letter]:
#                row.append(dict[letter])
#            else:
#                row.append("")
#        result.append(row)
    return {"Status": "saved"}    

def importFromBuffer(buff):
    memfile = io.BytesIO(buff)
    raw = xlsx(memfile)
    result = saveToDb(raw, datamodel.Product.docHeaderMap)
    return json.dumps(result)
    
