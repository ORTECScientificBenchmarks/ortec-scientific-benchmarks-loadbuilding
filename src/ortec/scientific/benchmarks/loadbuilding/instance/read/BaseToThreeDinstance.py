from ..ThreeDinstance      import ThreeDinstance
from ..ThreeDcontainerkind import ThreeDcontainerkind
from ..ThreeDitemkind      import ThreeDitemkind
from ..ThreeDboxkind       import ThreeDboxkind
from ..ThreeDpalletkind    import ThreeDpalletkind
from ..ThreeDloadingspace  import ThreeDloadingspace
from ..ThreeDconstraint    import ThreeDconstraint
from ..ThreeDobjective     import ThreeDobjective

from ...common.Requirements import BaseRequirement, ExistenceRequirement

class BaseToThreeDinstance(object):
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
    
    def __init__(self,filename="",text=""):
        self.filename    = filename
        self.text        = text
        self.base        = self.safeFindRoot(self.filename, self.text)
        self.description = self.safeFindOne(self.base, 'description')
        self.constraints = self.safeFindOne(self.base, 'constraints')
        self.objectives  = self.safeFindOne(self.base, 'objectives')
        self.data        = self.safeFindOne(self.base, 'data')
        self.containers  = self.safeFindOne(self.data, 'containerkinds')
        self.pallets     = self.safeFindOne(self.data, 'palletkinds')
        self.boxes       = self.safeFindOne(self.data, 'boxkinds')
        self.items       = self.safeFindOne(self.data, 'itemkinds')
        
    def _fillInfo_(self,threeDinstance):
        threeDinstance.description.setname = self.safeGetText(self.description, 'set',  str)
        threeDinstance.description.name    = self.safeGetText(self.description, 'name', str)
        
    def _fillContainerKinds_(self,threeDinstance):
        for baseContainer in self.safeFindAll(self.containers, 'containerkind'):
            lbContainer          = ThreeDcontainerkind()
            lbContainer.id       = self.safeGetAttr(baseContainer, 'id',       int)
            lbContainer.quantity = self.safeGetText(baseContainer, 'quantity', int)
            loadingSpaces        = self.safeFindOne(baseContainer, 'loadingspaces')
            for loadingSpace in self.safeFindAll(loadingSpaces, 'loadingspace'):
                lbLoadingSpace    = ThreeDloadingspace()
                lbLoadingSpace.id = self.safeGetAttr(loadingSpace, 'id', int)
                size              = self.safeFindOne(loadingSpace, 'size')
                length            = self.safeGetText(size, 'length', int)
                width             = self.safeGetText(size, 'width',  int)
                height            = self.safeGetText(size, 'height', int)
                lbLoadingSpace.boundingBox = [length, width, height]
                lbLoadingSpace.position = self.safeGetText(loadingSpace, 'position', str)
                if lbLoadingSpace.position is not None and isinstance(lbLoadingSpace.position, str):
                    try:
                        lbLoadingSpace.position = lbLoadingSpace.position.split(',')
                        lbLoadingSpace.position = list(map(int, lbLoadingSpace.position))
                    except Exception:
                        pass
                
                # Load all known optional fields
                loadingspaceFields = set()
                for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                    loadingspaceFields |= set([req for req in r.loadingspaceRequirements])
                for lf in filter(lambda x: isinstance(x, ExistenceRequirement), loadingspaceFields):
                    setattr(lbLoadingSpace, lf.field, self.safeGetText(loadingSpace, lf.field, lf.cast))
                lbContainer.addLoadingspace(lbLoadingSpace)      

            # Load all known optional fields
            containerRequirements = list()
            for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                containerRequirements += requirements.containerkindRequirements
            for field, cast in set([(requirement.field, requirement.cast) for requirement in containerRequirements if isinstance(requirement, ExistenceRequirement)]):
                setattr(lbContainer, field, self.safeGetText(baseContainer, field, cast))
            threeDinstance.addContainerkind(lbContainer)
    
    def _fillPalletKinds_(self,threeDinstance):
        for basePallet in self.safeFindAll(self.pallets, 'palletkind'):
            lbPallet             = ThreeDpalletkind()
            lbPallet.id          = self.safeGetAttr(basePallet, 'id',       int)
            lbPallet.quantity    = self.safeGetText(basePallet, 'quantity', int)
            palletSize           = self.safeFindOne(basePallet, 'size')
            palletLength         = self.safeGetText(palletSize, 'length', int)
            palletWidth          = self.safeGetText(palletSize, 'width',  int)
            palletHeight         = self.safeGetText(palletSize, 'height', int)
            lbPallet.boundingBox = [palletLength, palletWidth, palletHeight]
            lbPallet.position    = self.safeGetText(basePallet, 'position', str)
            if lbPallet.position is not None and isinstance(lbPallet.position, str):
                try:
                    lbPallet.position = lbPallet.position.split(',')
                    lbPallet.position = list(map(int, lbPallet.position))
                except Exception:
                    pass
            loadingspace      = self.safeFindOne(basePallet, 'loadingspace')
            size              = self.safeFindOne(loadingspace, 'size')
            length            = self.safeGetText(size, 'length', int)
            width             = self.safeGetText(size, 'width',  int)
            height            = self.safeGetText(size, 'height', int)
            lbPallet.loadingspace             = ThreeDloadingspace()
            lbPallet.loadingspace.id          = self.safeGetAttr(loadingspace, 'id', int)
            lbPallet.loadingspace.boundingBox = [length, width, height]
            lbPallet.loadingspace.position = self.safeGetText(loadingspace, 'position', str)
            if lbPallet.loadingspace.position is not None and isinstance(lbPallet.loadingspace.position, str):
                try:
                    lbPallet.loadingspace.position = lbPallet.loadingspace.position.split(',')
                    lbPallet.loadingspace.position = list(map(int, lbPallet.loadingspace.position))
                except Exception:
                    pass
            orientations      = self.safeGetText(basePallet, 'orientations', str)
            if orientations is not None and isinstance(orientations, str):
                lbPallet.orientations = set(orientations.split(','))
            
            # Load all known optional fields
            palletRequirements = list()
            for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                palletRequirements += requirements.palletkindRequirements
            for field, cast in set([(requirement.field, requirement.cast) for requirement in palletRequirements if isinstance(requirement, ExistenceRequirement)]):
                setattr(lbPallet, field, self.safeGetText(basePallet, field, cast))
            threeDinstance.addPalletkind(lbPallet)
            
    def _fillBoxKinds_(self,threeDinstance):
        for baseBox in self.safeFindAll(self.boxes, 'boxkind'):
            lbBox             = ThreeDboxkind()
            lbBox.id          = self.safeGetAttr(baseBox, 'id',       int)
            lbBox.quantity    = self.safeGetText(baseBox, 'quantity', int)
            boxSize           = self.safeFindOne(baseBox, 'size')
            boxLength         = self.safeGetText(boxSize, 'length', int)
            boxWidth          = self.safeGetText(boxSize, 'width',  int)
            boxHeight         = self.safeGetText(boxSize, 'height', int)
            lbBox.boundingBox = [boxLength, boxWidth, boxHeight]
            lbBox.position    = self.safeGetText(baseBox, 'position', str)
            if lbBox.position is not None and isinstance(lbBox.position, str):
                try:
                    lbBox.position = lbBox.position.split(',')
                    lbBox.position = list(map(int, lbBox.position))
                except Exception:
                    pass
            loadingspace = self.safeFindOne(baseBox, 'loadingspace')
            size   = self.safeFindOne(loadingspace, 'size')
            length = self.safeGetText(size, 'length', int)
            width  = self.safeGetText(size, 'width',  int)
            height = self.safeGetText(size, 'height', int)
            lbBox.loadingspace             = ThreeDloadingspace()
            lbBox.loadingspace.id          = self.safeGetAttr(loadingspace, 'id', int)
            lbBox.loadingspace.boundingBox = [length, width, height]
            lbBox.loadingspace.position    = self.safeGetText(loadingspace, 'position', str)
            if lbBox.loadingspace.position is not None and isinstance(lbBox.loadingspace.position, str):
                try:
                    lbBox.loadingspace.position = lbBox.loadingspace.position.split(',')
                    lbBox.loadingspace.position = list(map(int, lbBox.loadingspace.position))
                except Exception:
                    pass
            orientations = self.safeGetText(baseBox, 'orientations', str)
            if orientations is not None and isinstance(orientations, str):
                lbBox.orientations = set(orientations.split(','))
            
            # Load all known optional fields
            boxRequirements = list()
            for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                boxRequirements += requirements.boxkindRequirements
            for field, cast in set([(requirement.field, requirement.cast) for requirement in boxRequirements if isinstance(requirement, ExistenceRequirement)]):
                setattr(lbBox, field, self.safeGetText(baseBox, field, cast))
            threeDinstance.addBoxkind(lbBox)
   
    def _fillItemKinds_(self,threeDinstance):
        for baseItem in self.safeFindAll(self.items, 'itemkind'):
            lbItem          = ThreeDitemkind()
            lbItem.id       = self.safeGetAttr(baseItem, 'id', int)
            lbItem.quantity = self.safeGetText(baseItem, 'quantity',     int)
            size            = self.safeFindOne(baseItem, 'size')
            length          = self.safeGetText(size, 'length', int)
            width           = self.safeGetText(size, 'width',  int)
            height          = self.safeGetText(size, 'height', int)
            orientations    = self.safeGetText(baseItem, 'orientations', str)
            lbItem.boundingBox = [length, width, height]
            if orientations is not None and isinstance(orientations, str):
                lbItem.orientations = set(orientations.split(','))
            
            # Load all known optional fields
            itemRequirements = list()
            for requirements in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                itemRequirements += requirements.itemkindRequirements
            for field, cast in set([(requirement.field, requirement.cast) for requirement in itemRequirements if isinstance(requirement, ExistenceRequirement)]):
                setattr(lbItem, field, self.safeGetText(baseItem, field, cast))
            threeDinstance.addItemkind(lbItem)
    
    def _fillConstraints_(self,threeDinstance):
        for baseConstraint in self.safeFindAll(self.constraints, 'constraint'):
            lbConstraint = ThreeDconstraint()
            name = self.safeGetAttr(baseConstraint, 'name', str)
            for c in BaseRequirement.CONSTRAINT_LIST:
                if c.name == name:
                    lbConstraint.constraint = c
                    break
            threeDinstance.addConstraint(lbConstraint)
        
    def _fillObjectives_(self,threeDinstance):
        for baseObjective in self.safeFindAll(self.objectives, 'objective'):
            lbObjective = ThreeDobjective()
            name = self.safeGetAttr(baseObjective, 'name', str)
            for o in BaseRequirement.OBJECTIVE_LIST:
                if o.name == name:
                    lbObjective.objective = o
                    break
            lbObjective.weight   = self.safeGetText(baseObjective, 'weight',   float)
            lbObjective.priority = self.safeGetText(baseObjective, 'priority', int)
            threeDinstance.addObjective(lbObjective)
    
    def CreateThreeDinstance(self):
        threeDinstance = ThreeDinstance()
        self._fillInfo_(threeDinstance)
        self._fillConstraints_(threeDinstance)
        self._fillObjectives_(threeDinstance)
        self._fillContainerKinds_(threeDinstance)
        self._fillPalletKinds_(threeDinstance)
        self._fillBoxKinds_(threeDinstance)
        self._fillItemKinds_(threeDinstance)
        return threeDinstance

if __name__=="__main__":
    exit("Don't run this file")