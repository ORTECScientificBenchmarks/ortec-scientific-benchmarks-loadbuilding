from .BaseToThreeDinstance import BaseToThreeDinstance
from ...common.utils import bool_cast
import yaml

class YAMLtoThreeDinstance(BaseToThreeDinstance):
    @staticmethod
    def safeFindRoot(filename="", text=""):
        if filename:
            with open(filename) as fd:
                return yaml.load(fd)
        if text:
            return yaml.load(text)
    
    @staticmethod
    def safeFindOne(yaml, tag):
        try:
            if tag is None:
                return yaml
            else:
                return yaml[tag]
        except:
            return None
    
    @staticmethod
    def safeFindAll(yaml, tag):
        if yaml is None:
            return []
        return yaml
    
    @staticmethod
    def safeGetAttr(yaml, tag, cast):
        try:
            if yaml[tag] is None:
                return None
            if cast == bool:
                return bool_cast(yaml[tag])
            return cast(yaml[tag])
        except:
            try:
                return yaml[tag]
            except:
                return None
    
    @staticmethod
    def safeGetText(yaml, tag, cast):
        return YAMLtoThreeDinstance.safeGetAttr(yaml, tag, cast)
    
    def __init__(self,filename="", text=""):
        super(YAMLtoThreeDinstance, self).__init__(filename,text)
        
if __name__=="__main__":
    exit("Don't run this file")