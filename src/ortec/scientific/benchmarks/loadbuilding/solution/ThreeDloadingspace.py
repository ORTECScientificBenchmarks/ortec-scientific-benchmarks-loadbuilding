from ..solution.ThreeDplacement import ThreeDplacement
from ..common.utils import indent, key

class ThreeDloadingspace:
    def __init__(self):
        self.id          = None
        self.placements  = list()
        
    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id, int):
            errors.append("Id should be integer")
        else:
            validid = True
            
        if self.placements is None:
            errors.append("Placements undefined")
        elif not isinstance(self.placements,list):
            errors.append("Placements should be a list")
        elif not all([isinstance(p, ThreeDplacement) for p in self.placements]):
            errors.append("Placements should be placement objects")
        else:
            for p in self.placements:
                b,e = p.IsValid()
                if not b:
                    errors.append(indent(e))
                    
        if len(errors)>1:
            return False, "Invalid loadingspace" + (" with id " + str(self.id) if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True,""

    @staticmethod
    def TypeString():
        return "loadingspace"

    def sort(self):
        if self.placements != None:
            self.placements.sort(key=key("id"))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        self.sort()
        other.sort()
        return self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

    def addPlacement(self, placement):
        if not isinstance(placement, ThreeDplacement): raise Exception("Expected a placement")
        self.placements.append(placement)

if __name__=="__main__":
    exit("Don't run this file")        