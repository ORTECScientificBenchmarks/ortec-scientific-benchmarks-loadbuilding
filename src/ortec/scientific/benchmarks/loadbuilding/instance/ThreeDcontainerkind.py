from .ThreeDloadingspace import ThreeDloadingspace
from ..common.utils import key, checkDuplicateIds, indent
from ..common.Requirements import BaseRequirement, ExistenceRequirement

class ThreeDcontainerkind(object):
    def __init__(self):
        self.id            = None
        self.loadingspaces = list()
        self.quantity      = None
        
        # Load all known optional fields
        containerRequirements = list()
        for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
            containerRequirements += requirements.containerkindRequirements
        for field, cast in set([(requirement.field, requirement.cast) for requirement in containerRequirements if isinstance(requirement, ExistenceRequirement)]):
            setattr(self, field, None)

    def addLoadingspace(self, loadingspace):
        if not isinstance(loadingspace, ThreeDloadingspace): raise Exception("Expected a loadingspace")
        self.loadingspaces.append(loadingspace)
        
    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id, int):
            errors.append("Id should be integer")
        else:
            validid = True
            
        if not self.loadingspaces:
            errors.append("No loadingspaces specified")
        elif not all([isinstance(x, ThreeDloadingspace) for x in self.loadingspaces]):
            errors.append("Expected loadingspace")
        else:
            for loadingspace in self.loadingspaces:
                b,e = loadingspace.IsValid()
                if not b:
                    errors.append(e)
            b,e = checkDuplicateIds(self.loadingspaces)
            if not b:
                errors.append(e)
                
        if self.quantity is None:
            errors.append("Quantity is undefined")
        elif not isinstance(self.quantity, int):
            errors.append("Quantity should be integer")
        elif not self.quantity >= 0:
            errors.append("Quantity should be non-negative")

        if len(errors)>1:
            return False, "Invalid containerkind" + (" with id " + str(self.id) + "" if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True, ""

    @staticmethod
    def TypeString():
        return "containerkind"

    def sort(self):
        if self.loadingspaces != None:
            self.loadingspaces.sort(key=key("id"))
    
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
