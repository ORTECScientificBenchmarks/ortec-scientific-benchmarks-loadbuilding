from ..Requirements import BaseConstraint, ExistenceRequirement, PropositionalRequirement

class MaximumWeightConstraint(BaseConstraint):
    name = "maximum_weight"
    containerkindRequirements = [ExistenceRequirement("maxWeight", float("inf"), float),
                                 PropositionalRequirement("maxWeight", lambda x: x>=0, "maxWeight must be non-negative")]
    itemkindRequirements = [ExistenceRequirement("weight", 0., float),
                            PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    boxkindRequirements = [ExistenceRequirement("weight", 0., float),
                           PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    palletkindRequirements = [ExistenceRequirement("weight", 0., float),
                              PropositionalRequirement("weight", lambda x: x>=0, "weight must be non-negative")]
    def Validate(threeDsolution):
        valid, errors = True, [""]
        for container in threeDsolution.containers:
            total_weight = container.GetTotalWeight()
            rep = "Container with id " + str(container.id) + " and kind " + str(container.kindid) + ": " + str(total_weight) + "/" + str(container.maxWeight)
            if total_weight > container.maxWeight:
                valid = False
                rep += " <- VIOLATION"
            errors.append(rep)
        return valid, ("All" if valid else "Not all") + " containers adhere to their maximum weight constraints" + ("." if valid else ":" + "\n\t- ".join(errors))
        
if __name__=="__main__":
    exit("Don't run this file")