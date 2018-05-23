
from .BaseToThreeDsolution import BaseToThreeDsolution
import json

class JSONtoThreeDsolution(BaseToThreeDsolution):
    @staticmethod
    def safeFindRoot(filename="", text=""):
        if filename:
            with open(filename) as fd:
                return json.load(fd)
        if text:
            return json.loads(text)

    @staticmethod
    def safeFindOne(json, tag):
        try:
            return json[tag]
        except:
            return None
    
    @staticmethod
    def safeFindAll(json, tag):
        if json is None:
            return []
        return json

    @staticmethod
    def safeGetAttr(json, tag, cast):
        try:
            if json[tag] is None:
                return None
            return cast(json[tag])
        except:
            try:
                return json[tag]
            except:
                return None
    
    @staticmethod
    def safeGetText(json, tag, cast):
        try:
            if json[tag] is None:
                return None
            return cast(json[tag])
        except:
            try:
                return json[tag]
            except:
                return None
        
    def __init__(self, filename="", text=""):
        super(JSONtoThreeDsolution, self).__init__(filename, text)
        
if __name__=="__main__":
    exit("Don't run this file")