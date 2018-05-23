from ..Requirements import BaseConstraint, ExistenceRequirement

class MustPlaceConstraint(BaseConstraint):
    name = "must_place"
    palletkindRequirements = [ExistenceRequirement("place", True, bool)]
    boxkindRequirements    = [ExistenceRequirement("place", True, bool)]
    itemkindRequirements   = [ExistenceRequirement("place", True, bool)]
    def Validate(threeDsolution):
        valid, errors = True, [""]
        if threeDsolution.unplaced != []:
            for placement in threeDsolution.unplaced:
                if placement.place:
                    valid = False
                    errors.append(placement.type.capitalize() + " with id " + str(placement.id) + " should be placed <- VIOLATION")
        return valid, ("All" if valid else "Not all") + " necessary placements were placed" + ("." if valid else ":" + "\n\t- ".join(errors))
        
if __name__=="__main__":
    exit("Don't run this file")