from ..ThreeDsolution     import ThreeDsolution
from ..ThreeDcontainer    import ThreeDcontainer
from ..ThreeDpallet       import ThreeDpallet
from ..ThreeDbox          import ThreeDbox
from ..ThreeDplacement    import ThreeDplacement
from ..ThreeDloadingspace import ThreeDloadingspace

class BaseToThreeDsolution(object):
    @staticmethod 
    def safeFindRoot(filename="", text=""):
        raise Exception("Derived classes of BaseToThreeDinstance need to override the safeFindRoot-method")

    @staticmethod
    def safeFindOne(container, containername):
        raise Exception("Derived classes of BaseToThreeDinstance need to override the safeFindOne-method")
    
    @staticmethod
    def safeFindAll(container, containername):
        raise Exception("Derived classes of BaseToThreeDinstance need to override the safeFindAll-method")

    @staticmethod
    def safeGetAttr(container, propertyname, cast):
        raise Exception("Derived classes of BaseToThreeDinstance need to override the safeGetAttr-method")
    
    @staticmethod
    def safeGetText(container, propertyname, cast):
        raise Exception("Derived classes of BaseToThreeDinstance need to override the safeGetText-method")

    def __init__(self, filename="", text=""):
        self.filename    = filename
        self.text        = text
        self.base        = self.safeFindRoot(self.filename, self.text)
        self.description = self.safeFindOne(self.base,   'description')
        self.layout      = self.safeFindOne(self.base,   'layout')
        self.containers  = self.safeFindOne(self.layout, 'containers')
        self.pallets     = self.safeFindOne(self.layout, 'pallets')
        self.boxes       = self.safeFindOne(self.layout, 'boxes')
        self.unplaced    = self.safeFindOne(self.layout, 'unplaced')
        
    def _fillInfo_(self,threeDsolution):
        threeDsolution.description.setname = self.safeGetText(self.description, 'set',  str)
        threeDsolution.description.name    = self.safeGetText(self.description, 'name', str)
        
    def _fillContainers_(self,threeDsolution):
        for baseContainer in self.safeFindAll(self.containers, 'container'):
            solContainer        = ThreeDcontainer()
            solContainer.id     = self.safeGetAttr(baseContainer, 'id',     int)
            solContainer.kindid = self.safeGetAttr(baseContainer, 'kindid', int)
            loadingSpaces = self.safeFindOne(baseContainer, 'loadingspaces')
            for baseLoadingspace in self.safeFindAll(loadingSpaces, 'loadingspace'):
                solLoadingspace = ThreeDloadingspace()
                solLoadingspace.id = self.safeGetAttr(baseLoadingspace, 'id', int)
                placements = self.safeFindOne(baseLoadingspace, 'placements')
                for basePlacement in self.safeFindAll(placements, 'placement'):
                    solPlacement             = ThreeDplacement()
                    solPlacement.id          = self.safeGetAttr(basePlacement, 'id',          int)
                    solPlacement.itemid      = self.safeGetAttr(basePlacement, 'itemid',      int)
                    solPlacement.boxid       = self.safeGetAttr(basePlacement, 'boxid',       int)
                    solPlacement.palletid    = self.safeGetAttr(basePlacement, 'palletid',    int)
                    solPlacement.position    = self.safeGetText(basePlacement, 'position',    str)
                    solPlacement.orientation = self.safeGetText(basePlacement, 'orientation', str)
                    solPlacement.color       = self.safeGetAttr(basePlacement, 'color',       str)
                    if solPlacement.position is not None and isinstance(solPlacement.position, str):
                        try:
                            solPlacement.position = solPlacement.position.split(',')
                            solPlacement.position = list(map(int, solPlacement.position))
                        except Exception:
                            pass
                    solLoadingspace.addPlacement(solPlacement)
                solContainer.addLoadingspace(solLoadingspace)
            threeDsolution.addContainer(solContainer)
        
    def _fillPallets_(self,threeDsolution):
        for basePallet in self.safeFindAll(self.pallets, 'pallet'):
            solPallet                 = ThreeDpallet()
            solPallet.id              = self.safeGetAttr(basePallet, 'id',     int)
            solPallet.kindid          = self.safeGetAttr(basePallet, 'kindid', int)
            baseLoadingspace          = self.safeFindOne(basePallet, 'loadingspace')
            solPallet.loadingspace    = ThreeDloadingspace()
            solPallet.loadingspace.id = self.safeGetAttr(baseLoadingspace, 'id', int)
            placements = self.safeFindOne(baseLoadingspace, 'placements')
            for basePlacement in self.safeFindAll(placements, 'placement'):
                solPlacement             = ThreeDplacement()
                solPlacement.id          = self.safeGetAttr(basePlacement, 'id',          int)
                solPlacement.itemid      = self.safeGetAttr(basePlacement, 'itemid',      int)
                solPlacement.boxid       = self.safeGetAttr(basePlacement, 'boxid',       int)
                solPlacement.palletid    = self.safeGetAttr(basePlacement, 'palletid',    int)
                solPlacement.position    = self.safeGetText(basePlacement, 'position',    str)
                solPlacement.orientation = self.safeGetText(basePlacement, 'orientation', str)
                solPlacement.color       = self.safeGetAttr(basePlacement, 'color',       str)
                if solPlacement.position is not None and isinstance(solPlacement.position, str):
                    try:
                        solPlacement.position = solPlacement.position.split(',')
                        solPlacement.position = list(map(int, solPlacement.position))
                    except Exception:
                        pass
                solPallet.loadingspace.addPlacement(solPlacement)
            threeDsolution.addPallet(solPallet)
    
    def _fillBoxes_(self,threeDsolution):
        for baseBox in self.safeFindAll(self.boxes, 'box'):
            solBox                 = ThreeDbox()
            solBox.id              = self.safeGetAttr(baseBox, 'id',     int)
            solBox.kindid          = self.safeGetAttr(baseBox, 'kindid', int)
            baseLoadingspace       = self.safeFindOne(baseBox, 'loadingspace')
            solBox.loadingspace    = ThreeDloadingspace()
            solBox.loadingspace.id = self.safeGetAttr(baseLoadingspace, 'id', int)
            placements = self.safeFindOne(baseLoadingspace, 'placements')
            for basePlacement in self.safeFindAll(placements, 'placement'):
                solPlacement             = ThreeDplacement()
                solPlacement.id          = self.safeGetAttr(basePlacement, 'id',          int)
                solPlacement.itemid      = self.safeGetAttr(basePlacement, 'itemid',      int)
                solPlacement.boxid       = self.safeGetAttr(basePlacement, 'boxid',       int)
                solPlacement.palletid    = self.safeGetAttr(basePlacement, 'palletid',    int)
                solPlacement.position    = self.safeGetText(basePlacement, 'position',    str)
                solPlacement.orientation = self.safeGetText(basePlacement, 'orientation', str)
                solPlacement.color       = self.safeGetAttr(basePlacement, 'color',       str)
                if solPlacement.position is not None and isinstance(solPlacement.position, str):
                    try:
                        solPlacement.position = solPlacement.position.split(',')
                        solPlacement.position = list(map(int, solPlacement.position))
                    except Exception:
                        pass
                solBox.loadingspace.addPlacement(solPlacement)
            threeDsolution.addBox(solBox)
    
    def _fillUnplaced_(self,threeDsolution):
        for baseUnplaced in self.safeFindAll(self.unplaced, 'placement'):
            solUnplaced             = ThreeDplacement()
            solUnplaced.id          = self.safeGetAttr(baseUnplaced, 'id',       int)
            solUnplaced.itemid      = self.safeGetAttr(baseUnplaced, 'itemid',   int)
            solUnplaced.boxid       = self.safeGetAttr(baseUnplaced, 'boxid',    int)
            solUnplaced.palletid    = self.safeGetAttr(baseUnplaced, 'palletid', int)
            solUnplaced.type        = self.safeGetAttr(baseUnplaced, 'type',     str)
            solUnplaced.quantity    = self.safeGetAttr(baseUnplaced, 'quantity', int)
            if solUnplaced.quantity is None:
                solUnplaced.quantity = 1
            solUnplaced.position    = solUnplaced.UNPLACED
            solUnplaced.orientation = solUnplaced.UNPLACED
            threeDsolution.unplaced.append(solUnplaced)
    
    def CreateThreeDsolution(self, threeDinstance):
        threeDsolution = ThreeDsolution(threeDinstance)
        self._fillInfo_(threeDsolution)
        self._fillBoxes_(threeDsolution)
        self._fillPallets_(threeDsolution)
        self._fillContainers_(threeDsolution)
        self._fillUnplaced_(threeDsolution)
        return threeDsolution

if __name__=="__main__":
    exit("Don't run this file")