
import json
from collections import OrderedDict
from .ThreeDinstanceToBase import ThreeDinstanceToBase

class ThreeDinstanceToJSON(ThreeDinstanceToBase):
    @staticmethod
    def newObject(container, new_obj):
        if isinstance(container, list):
            obj = OrderedDict()
            container.append(obj)
            return obj
        else:
            container[new_obj] = OrderedDict()
            return container[new_obj]
    
    @staticmethod
    def newObjectList(container, new_obj):
        container[new_obj] = list()
        return container[new_obj]
    
    @staticmethod
    def addAttrib(container, attr, val, cast):
        container[attr] = cast(val)
    
    @staticmethod
    def setText(container, tag, text, cast):
        container[tag] = cast(text)
        
    @staticmethod 
    def createBase():
        return OrderedDict()
                
    def WriteInstance(self,filename):
        self._createBase_()
        with open(filename, 'w') as f:
            json.dump(self.base, f)


if __name__=="__main__":
    exit("Don't run this file")