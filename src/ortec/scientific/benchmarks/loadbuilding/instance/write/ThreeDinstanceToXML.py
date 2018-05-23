
from .ThreeDinstanceToBase import ThreeDinstanceToBase
import xml.etree.ElementTree as ET

class ThreeDinstanceToXML(ThreeDinstanceToBase):
    @staticmethod
    #http://effbot.org/zone/element-lib.htm#prettyprint
    def indent(elem, level=0):
        i = '\n' + level*'\t'
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + '\t'
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                ThreeDinstanceToXML.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
                
    @staticmethod
    def newObject(container, new_obj):
        return ET.SubElement(container, new_obj)

    @staticmethod
    def newObjectList(container, new_obj):
        return ET.SubElement(container, new_obj)
    
    @staticmethod
    def addAttrib(container, attr, val, cast):
        container.attrib.update({attr: str(val)})
    
    @staticmethod
    def setText(container, tag, text, cast):
        ET.SubElement(container, tag).text = str(text)

    @staticmethod 
    def createBase():
        return ET.Element("instance")
                
    def WriteInstance(self,filename):
        self._createBase_()
        self.indent(self.base)
        lbXML = ET.ElementTree(self.base)
        lbXML.write(filename)
        
if __name__=="__main__":
    exit("Don't run this file")