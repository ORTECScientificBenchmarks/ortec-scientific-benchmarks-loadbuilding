from ..common.utils import Orientation, indent
from ..common.Requirements import BaseRequirement, ExistenceRequirement

class ThreeDitemkind(object):
    def __init__(self):
        self.id           = None
        self.boundingBox  = None
        self.quantity     = None
        self.orientations = None
        
        # Load all known optional fields
        itemRequirements = list()
        for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
            itemRequirements += requirements.itemkindRequirements
        for field, cast in set([(requirement.field, requirement.cast) for requirement in itemRequirements if isinstance(requirement, ExistenceRequirement)]):
            setattr(self, field, None)

    def GetOrientationString(self):
        return ','.join(sorted(self.orientations))
    
    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id, int):
            errors.append("Id should be integer")
        else:
            validid = True
            
        if self.boundingBox is None:
            errors.append("Bounding box undefined")
        elif not isinstance(self.boundingBox, list):
            errors.append("Bounding box should be a list")
        elif None in self.boundingBox or len(self.boundingBox) != 3:
            errors.append("Bounding box should have three dimensions")
        elif not all([isinstance(x, int) for x in self.boundingBox]):
            errors.append("Dimensions of bounding box should be integer")
        elif not all([x > 0 for x in self.boundingBox]):
            errors.append("Dimensions of bounding box should be positive")
            
        if self.quantity is None:
            errors.append("Quantity undefined")
        elif not isinstance(self.quantity, int):
            errors.append("Quantity should be integer")
        elif not self.quantity >= 0:
            errors.append("Quantity should be non-negative")
            
        if self.orientations is None:
            errors.append("Orientations undefined")
        elif not isinstance(self.orientations, set):
            errors.append("Orientations should be a set")
        elif not ({Orientation.GetFromAlias(alias) for alias in self.orientations}.issubset(Orientation.ALL)):
            errors.append("Orientations must be subset of {" + ", ".join(Orientation.ALL) + "}, where LHW, WLH, and HWL can be used as aliases for LhW, WlH, and HwL")
            
        if len(errors)>1:
            return False, "Invalid itemkind" + (" with id " + str(self.id) + "" if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "itemkind"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")