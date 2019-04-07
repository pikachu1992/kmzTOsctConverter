import zipfile
from xml.dom import minidom

def kmz_to_kml(fname):
    zf = zipfile.ZipFile(fname,'r')
    for fn in zf.namelist():
        if fn.endswith('.kml'):
            content = zf.read(fn)
            xmldoc = minidom.parseString(content)
            out_name = (fname.replace(".kmz",".kml")).replace("\\","/")
            out = open('uploads/' + out_name,'w')
            out.writelines(xmldoc.toxml())
            out.close()
        else:
            print("no kml file")
