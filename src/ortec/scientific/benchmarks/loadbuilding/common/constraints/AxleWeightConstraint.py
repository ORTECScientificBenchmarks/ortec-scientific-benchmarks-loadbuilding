from ..Requirements import BaseConstraint, ExistenceRequirement, PropositionalRequirement

class AxleWeightConstraint(BaseConstraint):
    name = "axle_weight"
    containerkindRequirements = [ExistenceRequirement("axle1", None, float),
                                 ExistenceRequirement("axle2", None, float),
                                 ExistenceRequirement("minWeightAxle1", 0.0, float),
                                 ExistenceRequirement("minWeightAxle2", 0.0, float),
                                 ExistenceRequirement("maxWeightAxle1", float("inf"), float),
                                 ExistenceRequirement("maxWeightAxle2", float("inf"), float)]
    itemkindRequirements = [ExistenceRequirement("weight", 0., float),
                            PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    boxkindRequirements = [ExistenceRequirement("weight", 0., float),
                           PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    palletkindRequirements = [ExistenceRequirement("weight", 0., float),
                              PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    def Validate(threeDsolution):
        valid, errors = True, [""]
        for container in threeDsolution.containers:
            L_min, L_max =  float("inf"), -float("inf")
            for loadingspace in threeDsolution.threeDinstance.containerkinds[container.kindid].loadingspaces:
                L_min, L_max = min(L_min, loadingspace.position[0]), max(L_max, loadingspace.position[0] + loadingspace.boundingBox[0])
            C_min, C_max = container.GetCOGbounds()
            C_min, C_max = max(C_min, L_min), min(C_max, L_max)
            x            = container.GetCOG()
            if x[0] < C_min or x[0] > C_max:
                valid = False
                errors.append("Container with id " + str(container.id) + " and kind " + str(container.kindid) + " c.o.g.: " + str(x[0]) + " not in [" + str(C_min) + ", " + str(C_max) + "] <- VIOLATION")
            else:
                errors.append("Container with id " + str(container.id) + " and kind " + str(container.kindid) + " c.o.g.: " + str(x[0]) + " in [" + str(C_min) + ", " + str(C_max) + "]")
        return valid, ("All" if valid else "Not all") + " containers adhere to their axle weight constraints" + ("." if valid else ":" + "\n\t- ".join(errors))
        
        
if __name__=="__main__":
    exit("Don't run this file")