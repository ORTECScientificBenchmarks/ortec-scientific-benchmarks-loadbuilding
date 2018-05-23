from .BaseToThreeDinstance import BaseToThreeDinstance
from ...common.utils import bool_cast
import xml.etree.ElementTree as ET

class XMLtoThreeDinstance(BaseToThreeDinstance):
    @staticmethod
    def safeFindRoot(filename="", text=""):
        if filename:
            return ET.parse(filename).getroot()
        if text:
            return ET.fromstring(text)
    
    @staticmethod
    def safeFindOne(xml, tag):
        try:
            return xml.find(tag)
        except:
            return None
    
    @staticmethod
    def safeFindAll(xml, tag):
        try:
            return xml.findall(tag)
        except:
            return []
    
    @staticmethod
    def safeGetAttr(xml, tag, cast):
        try:
            if xml.get(tag) is None:
                return None
            if cast == bool:
                return bool_cast(xml.get(tag))
            return cast(xml.get(tag))
        except:
            try:
                return xml.get(tag)
            except:
                return None
    
    @staticmethod
    def safeGetText(xml, tag, cast):
        try:
            if xml.find(tag).text is None:
                return None
            if cast == bool:
                return bool_cast(xml.find(tag).text)
            return cast(xml.find(tag).text)
        except:
            try:
                return xml.find(tag).text
            except:
                return None
    
    def __init__(self,filename="",text=""):
        super(XMLtoThreeDinstance, self).__init__(filename,text)
        
if __name__=="__main__":
    exit("Don't run this file")