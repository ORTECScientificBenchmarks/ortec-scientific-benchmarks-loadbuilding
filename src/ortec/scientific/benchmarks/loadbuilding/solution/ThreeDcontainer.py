from .ThreeDloadingspace import ThreeDloadingspace
from ..common.utils import key, indent, checkDuplicateIds

class ThreeDcontainer:
    def __init__(self):
        self.id            = None
        self.kindid        = None
        self.loadingspaces = list()
        
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
            
        if self.loadingspaces is None:
            errors.append("Loadingspaces undefined")
        elif not isinstance(self.loadingspaces,list):
            errors.append("Loadingspaces should be a list")
        elif not self.loadingspaces:
            errors.append("No loadingspaces specified")
        elif not all([isinstance(x, ThreeDloadingspace) for x in self.loadingspaces]):
            errors.append("Expected loadingspace")
        else:
            for ls in self.loadingspaces:
                b,e = ls.IsValid()
                if not b:
                    errors.append(indent(e))
            b,e = checkDuplicateIds(self.loadingspaces)
            if not b:
                errors.append(e)
                    
        if len(errors)>1:
            return False, "Invalid container" + (" with id " + str(self.id) if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True,""
    
    def GetTotalWeight(self):
        final_weight = 0
        for loadingspace in self.loadingspaces:
            for placement in loadingspace.placements:
                final_weight += placement.GetTotalWeight()
        return final_weight
    
    def GetCOG(self):
        final_cog    = [0,0,0]
        final_weight = 0
        for loadingspace in self.loadingspaces:
            ls_pos = loadingspace.position
            for placement in loadingspace.placements:
                cog, weight = placement.GetCOG()
                final_weight += weight
                final_cog[0] += weight*(cog[0] + ls_pos[0])
                final_cog[1] += weight*(cog[1] + ls_pos[1])
                final_cog[2] += weight*(cog[2] + ls_pos[2])
        final_weight = self.GetTotalWeight()
        final_cog    = [coord/final_weight for coord in final_cog]
        return final_cog, final_weight
    
    def GetCOGbounds(self):
        W = self.GetTotalWeight()
        x_f, x_r       = self.axle1,          self.axle2
        W_fmin, W_fmax = self.minWeightAxle1, self.maxWeightAxle1
        W_rmin, W_rmax = self.minWeightAxle2, self.maxWeightAxle2
        C_min = max(x_f + W_rmin*(x_r - x_f)/W, x_r - W_fmax*(x_r - x_f)/W)
        C_max = min(x_f + W_rmax*(x_r - x_f)/W, x_r - W_fmin*(x_r - x_f)/W)
        return C_min, C_max
    
    @staticmethod
    def TypeString():
        return "container"

    def sort(self):
        if self.loadingspaces != None:
            self.loadingspaces.sort(key=key("id"))
            for loadingspace in self.loadingspaces:
                if loadingspace != None:
                    loadingspace.sort()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        self.sort()
        other.sort()
        return self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

    def addLoadingspace(self, loadingspace):
        if not isinstance(loadingspace, ThreeDloadingspace): raise Exception("Expected a loadingspace")
        self.loadingspaces.append(loadingspace)
        
if __name__=="__main__":
    exit("Don't run this file")