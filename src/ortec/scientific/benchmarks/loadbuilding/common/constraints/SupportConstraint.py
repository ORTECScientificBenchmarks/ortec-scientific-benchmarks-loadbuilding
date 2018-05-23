from ..Requirements import BaseConstraint, ExistenceRequirement, PropositionalRequirement

# Support constraint validate uses stored values of Ngoi matrix obtained from the DecorateSolution(..)-method
class SupportConstraint(BaseConstraint):
    name = "support"
    itemkindRequirements = [ExistenceRequirement("support", 1.0, float),
                            PropositionalRequirement("support", lambda x: x>=0 and x<=1.0, "support must be in the interval [0, 1]")]
    boxkindRequirements = [ExistenceRequirement("support", 1.0, float),
                           PropositionalRequirement("support", lambda x: x>=0 and x<=1.0, "support must be in the interval [0, 1]")]
    palletkindRequirements = [ExistenceRequirement("support", 1.0, float),
                              PropositionalRequirement("support", lambda x: x>=0 and x<=1.0, "support must be in the interval [0, 1]")]
    def Validate(threeDsolution):
        valid, errors = True, [""]
        for container in threeDsolution.containers:
            for loadingspace in container.loadingspaces:
                valid = valid and loadingspace.ngoi.support_valid
                errors += loadingspace.ngoi.support_report
        for pallet in threeDsolution.pallets:
            valid = valid and pallet.loadingspace.ngoi.support_valid
            errors += pallet.loadingspace.ngoi.support_report
        return valid, ("All" if valid else "Not all") + " placements are properly supported:" + "\n\t- ".join(errors)
        
if __name__=="__main__":
    exit("Don't run this file")