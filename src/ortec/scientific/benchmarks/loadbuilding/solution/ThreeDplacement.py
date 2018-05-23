from ..common.utils import indent

class ThreeDplacement(object):
    UNPLACED = "UNPLACED"
    
    def __init__(self):
        self.id          = None
        self.itemid      = None # only for items
        self.boxid       = None # only for boxes
        self.palletid    = None # only for pallets
        self.position    = None
        self.orientation = None
        self.color       = None
        
    def IsValid(self):
        errors = [""]
        
        validid = False
        if self.id is None:
            errors.append("Id undefined")
        elif not isinstance(self.id, int):
            errors.append("Id should be integer")
        else:
            validid = True
        
        if sum([1 for i in [self.itemid, self.boxid, self.palletid] if i is not None]) != 1:
            errors.append("Exactly one of itemid, boxid, and palletid must be defined")
        else:
            if self.itemid is not None:
                if not isinstance(self.itemid, int):
                    errors.append("Item id should be integer")
            elif self.boxid is not None:
                if not isinstance(self.boxid, int):
                    errors.append("Box id should be integer")
            elif self.palletid is not None:
                if not isinstance(self.palletid, int):
                    errors.append("Pallet id should be integer")
        if self.position is None:
            errors.append("Position undefined")
        elif self.position is not self.UNPLACED:
            if not isinstance(self.position, list):
                errors.append("Position should be a list")
            elif any([x is None for x in self.position]) or len(self.position) != 3:
                errors.append("Position should have three dimensions")
            elif not all([isinstance(x, int) for x in self.position]):
                errors.append("Dimensions of position should be integer")
                
        if len(errors)>1:
            return False, "Invalid placement" + (" with id " + str(self.id) if validid else "") + ":" + "\n\t- ".join(map(indent, errors))
        return True,""

    def GetTotalWeight(self):
        if self.itemid is not None:
            return self.weight
        else:
            final_weight = self.weight
            for placement in self.loadingspace.placements:
                final_weight += placement.GetTotalWeight()
            return final_weight
        
    def GetCOG(self):
        if self.type == "item":
            return list(map(lambda x: x[0] + x[1]/2, zip(self.position, self.boundingBox)))
        else:
            final_cog    = list(map(lambda x: self.weight*(x[0] + x[1]/2), zip(self.position, self.boundingBox)))
            final_weight = self.weight
            ls_pos = self.loadingspace.position
            for placement in self.loadingspace.placements:
                cog, weight = placement.GetCOG()
                final_weight += weight
                final_cog[0] += weight*(cog[0] + ls_pos[0])
                final_cog[1] += weight*(cog[1] + ls_pos[1])
                final_cog[2] += weight*(cog[2] + ls_pos[2])
            final_weight = self.GetTotalWeight()
            final_cog    = [coord/final_weight for coord in final_cog]
            return final_cog, final_weight
        
    @staticmethod
    def TypeString():
        return "placement"

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__
    
    def __ne__(self,other):
        return not self.__eq__(other)

if __name__=="__main__":
    exit("Don't run this file")