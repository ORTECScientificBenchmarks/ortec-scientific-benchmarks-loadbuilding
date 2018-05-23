from ..common.utils import indent

class ThreeDloadingspace(object):
    def __init__(self):
        self.id          = None
        self.boundingBox = None
        self.position    = None
        
    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id,int):
            errors.append("Id should be integer")
        else:
            validid = True
            
        if self.boundingBox is None:
            errors.append("Bounding box undefined")
        elif not isinstance(self.boundingBox,list):
            errors.append("Bounding box should be a list")
        elif None in self.boundingBox or len(self.boundingBox) != 3:
            errors.append("Bounding box should have three dimensions")
        elif not all([isinstance(x,int) for x in self.boundingBox]):
            errors.append("Dimensions of bounding box should be integer")
        elif not all([x > 0 for x in self.boundingBox]):
            errors.append("Dimensions of bounding box should be positive")

        if self.position is None:
            errors.append("Position undefined")
        elif not isinstance(self.position, list):
            errors.append("Position should be a list")
        elif None in self.position or len(self.position) != 3:
            errors.append("Position should have three dimensions")
        elif not all([isinstance(x, int) for x in self.position]):
            errors.append("Dimensions of position should be integer")
        elif not all([x >= 0 for x in self.position]):
            errors.append("Dimensions of position should be non-negative")
            
        if len(errors)>1:
            return False, "Invalid loadingspace" + (" with id " + str(self.id) + "" if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "loadingspace"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")