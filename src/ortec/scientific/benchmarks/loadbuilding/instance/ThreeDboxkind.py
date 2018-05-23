from .ThreeDloadingspace import ThreeDloadingspace
from ..common.utils import Orientation, indent
from ..common.Requirements import BaseRequirement, ExistenceRequirement

class ThreeDboxkind(object):
    def __init__(self):
        self.id                        = None
        self.boundingBox               = None
        self.position                  = None
        self.loadingspace              = None
        self.quantity                  = None
        self.orientations              = None
        
        # Load all known optional fields
        boxRequirements = list()
        for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
            boxRequirements += requirements.boxkindRequirements
        for field, cast in set([(requirement.field, requirement.cast) for requirement in boxRequirements if isinstance(requirement, ExistenceRequirement)]):
            setattr(self, field, None)

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
            
        if self.loadingspace is None:
            errors.append("Loadingspace undefined")
        elif not isinstance(self.loadingspace, ThreeDloadingspace):
            errors.append("Expected loadingspace")
        else:
            b,e = self.loadingspace.IsValid()
            if not b:
                errors.append(indent(e))
                
        if self.quantity is None:
            errors.append("Quantity is undefined")
        elif not isinstance(self.quantity, int):
            errors.append("Quantity should be integer")
        elif not self.quantity >= 0:
            errors.append("Quantity should be non-negative")
        
        if self.orientations is None:
            errors.append("Orientations undefined")
        elif not isinstance(self.orientations, set):
            errors.append("Orientations should be a set")
        elif not ({Orientation.GetFromAlias(alias) for alias in self.orientations}.issubset(Orientation.THIS_SIDE_UP)):
            errors.append("Orientations must be subset of {" + ", ".join(Orientation.THIS_SIDE_UP) + "}, where WLH can be used as alias for WlH")

        if len(errors)>1:
            return False, "Invalid boxkind" + (" with id " + str(self.id) + "" if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "boxkind"
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")