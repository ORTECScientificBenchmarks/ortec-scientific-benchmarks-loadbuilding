
from .BaseToThreeDsolution import BaseToThreeDsolution
import yaml

class YAMLtoThreeDsolution(BaseToThreeDsolution):
    @staticmethod
    def safeFindRoot(filename="", text=""):
        if filename:
            with open(filename) as fd:
                return yaml.full_load(fd)
        if text:
            return yaml.full_load(text)
    
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
            return cast(yaml[tag])
        except:
            try:
                return yaml[tag]
            except:
                return None
    
    @staticmethod
    def safeGetText(yaml, tag, cast):
        return YAMLtoThreeDsolution.safeGetAttr(yaml, tag, cast)
    
    def __init__(self, filename="", text=""):
        super(YAMLtoThreeDsolution, self).__init__(filename, text)
        
if __name__=="__main__":
    exit("Don't run this file")