class ThreeDsolutionToBase(object):
    @staticmethod
    def newObject(container, new_obj):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the newObject-method")
    
    @staticmethod
    def newObjectList(container, new_obj):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the newObjectList-method")
    
    @staticmethod
    def addAttrib(container, attr, val, cast):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the addAttrib-method")
    
    @staticmethod
    def setText(container, tag, text, cast):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the setText-method")

    @staticmethod 
    def createBase(filename):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the createBase-method")
                
    def WriteSolution(self,filename):
        raise Exception("Derived classes of ThreeDsolutionToBase need to override the writeSolution-method")

    def __init__(self,solution):
        self.solution = solution
    
    def _createFrame_(self):
        self.base        = self.createBase()
        self.description = self.newObject(self.base, "description")
        self.layout      = self.newObject(self.base, "layout")
        self.containers  = self.newObjectList(self.layout, "containers")
        self.pallets     = self.newObjectList(self.layout, "pallets")
        self.boxes       = self.newObjectList(self.layout, "boxes")
        self.unplaced    = self.newObjectList(self.layout, "unplaced")

    def _fillInfo_(self):
        self.setText(self.description, "set",  self.solution.description.setname, str)
        self.setText(self.description, "name", self.solution.description.name,    str)
    
    def _fillContainers_(self):      
        for solContainer in self.solution.containers:
            baseContainer = self.newObject(self.containers, "container")
            self.addAttrib(baseContainer, "id",     solContainer.id,       int)
            self.addAttrib(baseContainer, "kindid", solContainer.kindid,   int)
            baseLoadingSpaces = self.newObjectList(baseContainer, "loadingspaces")
            for solLoadingspace in solContainer.loadingspaces:
                baseLoadingSpace = self.newObject(baseLoadingSpaces, "loadingspace")
                self.addAttrib(baseLoadingSpace, "id", solLoadingspace.id, int)
                basePlacements = self.newObjectList(baseLoadingSpace, "placements")
                for solPlacement in solLoadingspace.placements:
                    basePlacement = self.newObject(basePlacements, "placement")
                    self.addAttrib(basePlacement, "id", solPlacement.id, int)
                    if solPlacement.itemid is not None:
                        self.addAttrib(basePlacement, "itemid", solPlacement.itemid, int)
                    elif solPlacement.boxid is not None:
                        self.addAttrib(basePlacement, "boxid", solPlacement.boxid, int)
                    elif solPlacement.palletid is not None:
                        self.addAttrib(basePlacement, "palletid", solPlacement.palletid, int)
                    self.setText(basePlacement, "position", ",".join(map(str,solPlacement.position)), str)
                    self.setText(basePlacement, "orientation", solPlacement.orientation, str)

    def _fillPallets_(self):
        for solPallet in self.solution.pallets:
            basePallet = self.newObject(self.pallets, "pallet")
            self.addAttrib(basePallet, "id", solPallet.id, int)
            self.addAttrib(basePallet, "kindid", solPallet.kindid, int)
            baseLoadingspace = self.newObject(basePallet, "loadingspace")
            self.addAttrib(baseLoadingspace, "id", solPallet.loadingspace.id, int)
            basePlacements = self.newObjectList(baseLoadingspace, "placements")
            for solPlacement in solPallet.loadingspace.placements:
                basePlacement = self.newObject(basePlacements, "placement")
                self.addAttrib(basePlacement, "id", solPlacement.id, int)
                if solPlacement.itemid is not None:
                    self.addAttrib(basePlacement, "itemid", solPlacement.itemid, int)
                elif solPlacement.boxid is not None:
                    self.addAttrib(basePlacement, "boxid", solPlacement.boxid, int)
                elif solPlacement.palletid is not None:
                    self.addAttrib(basePlacement, "palletid", solPlacement.palletid, int)
                self.setText(basePlacement, "position",    ",".join(map(str,solPlacement.position)), str)
                self.setText(basePlacement, "orientation", solPlacement.orientation, str)
    
    def _fillBoxes_(self):
        for solBox in self.solution.boxes:
            baseBox = self.newObject(self.pallets, "pallet")
            self.addAttrib(baseBox, "id", solBox.id, int)
            self.addAttrib(baseBox, "kindid", solBox.kindid, int)
            baseLoadingspace = self.newObject(baseBox, "loadingspace")
            self.addAttrib(baseLoadingspace, "id", solBox.loadingspace.id, int)
            basePlacements = self.newObjectList(baseLoadingspace, "placements")
            for solPlacement in solBox.loadingspace.placements:
                basePlacement = self.newObject(basePlacements, "placement")
                self.addAttrib(basePlacement, "id", solPlacement.id, int)
                if solPlacement.itemid is not None:
                    self.addAttrib(basePlacement, "itemid", solPlacement.itemid, int)
                elif solPlacement.boxid is not None:
                    self.addAttrib(basePlacement, "boxid", solPlacement.boxid, int)
                elif solPlacement.palletid is not None:
                    self.addAttrib(basePlacement, "palletid", solPlacement.palletid, int)
                self.setText(basePlacement, "position", ",".join(map(str,solPlacement.position)), str)
                self.setText(basePlacement, "orientation", solPlacement.orientation, str)
            
    def _fillUnplaced_(self):
        for solPlacement in self.solution.unplaced:
            basePlacement = self.newObject(self.unplaced, "placement")
            self.addAttrib(basePlacement, "id", solPlacement.id, int)
            if solPlacement.itemid is not None:
                self.addAttrib(basePlacement, "itemid", solPlacement.itemid, int)
                self.addAttrib(basePlacement, "quantity", solPlacement.quantity, int)
            elif solPlacement.boxid is not None:
                self.addAttrib(basePlacement, "boxid", solPlacement.boxid, int)
            elif solPlacement.palletid is not None:
                self.addAttrib(basePlacement, "palletid", solPlacement.palletid, int)
        
    def _createBase_(self):
        self._createFrame_()
        self._fillInfo_()
        self._fillContainers_()
        self._fillPallets_()
        self._fillBoxes_()
        self._fillUnplaced_()
        
if __name__=="__main__":
    exit("Don't run this file")