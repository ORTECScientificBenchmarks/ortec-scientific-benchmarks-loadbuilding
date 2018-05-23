from .ThreeDloadingspace import ThreeDloadingspace
from ..common.utils import key, indent

class ThreeDpallet:
    def __init__(self):
        self.id           = None
        self.kindid       = None
        self.loadingspace = None

    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id, int):
            errors.append("Id should be integer")
        else:
            validid = True
            
        if self.kindid is None:
            errors.append("Kind id undefined")
        elif not isinstance(self.kindid, int):
            errors.append("Kind id should be integer")
            
        if self.loadingspace is None:
            errors.append("Loadingspace undefined")
        elif not isinstance(self.loadingspace, ThreeDloadingspace):
            errors.append("Expected loadingspace")
        else:
            b,e = self.loadingspace.IsValid()
            if not b:
                errors.append(indent(e))
                
        if len(errors)>1:
            return False, "Invalid pallet" + (" with id " + str(self.id) if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True,""

    @staticmethod
    def TypeString():
        return "pallet"

    def sort(self):
        if self.loadingspace != None:
            self.loadingspace.sort(key=key("id"))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        self.sort()
        other.sort()
        return self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")