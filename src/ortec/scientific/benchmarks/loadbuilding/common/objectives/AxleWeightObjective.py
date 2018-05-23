from ..Requirements import BaseObjective, ExistenceRequirement, PropositionalRequirement

# MINIMIZE
class AxleWeightObjective(BaseObjective):
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
    def Evaluate(threeDsolution):
        obj = 0
        for container in threeDsolution.containers:
            L_min, L_max =  float("inf"), -float("inf")
            for loadingspace in threeDsolution.threeDinstance.containerkinds[container.kindid].loadingspaces:
                L_min, L_max = min(L_min, loadingspace.position[0]), max(L_max, loadingspace.position[0] + loadingspace.boundingBox[0])
            C_min, C_max = container.GetCOGbounds()
            C_min, C_max = max(C_min, L_min), min(C_max, L_max)
            x            = container.GetCOG()
            obj += max(abs(x[0] - (C_min+C_max)/2) - (C_max-C_min)/2, 0)
        return obj
        
if __name__=="__main__":
    exit("Don't run this file")