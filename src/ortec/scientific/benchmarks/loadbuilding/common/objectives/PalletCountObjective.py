from ..Requirements import BaseObjective

# MINIMIZE
class PalletCountObjective(BaseObjective):
    name = "pallet_count"
    def Evaluate(threeDsolution):
        return len(threeDsolution.pallets)
        
if __name__=="__main__":
    exit("Don't run this file")