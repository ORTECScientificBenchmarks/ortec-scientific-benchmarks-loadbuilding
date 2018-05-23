from ...common.Requirements import BaseRequirement, ExistenceRequirement

class ThreeDinstanceToBase(object):
    @staticmethod
    def newObject(container, new_obj):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the newObject-method")
    
    @staticmethod
    def newObjectList(container, new_obj):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the newObjectList-method")
    
    @staticmethod
    def addAttrib(container, attr, val, cast):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the addAttrib-method")
    
    @staticmethod
    def setText(container, tag, text, cast):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the setText-method")

    @staticmethod 
    def createBase(filename):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the createBase-method")
                
    def WriteInstance(self,filename):
        raise Exception("Derived classes of ThreeDinstanceToBase need to override the createBase-method")

    def __init__(self,instance):
        self.instance = instance
    
    def _createFrame_(self):
        self.base           = self.createBase()
        self.description    = self.newObject(self.base, "description")
        self.constraints    = self.newObjectList(self.base, "constraints")
        self.objectives     = self.newObjectList(self.base, "objectives")
        self.data           = self.newObject(self.base, "data")
        self.containerkinds = self.newObjectList(self.data, "containerkinds")
        self.palletkinds    = self.newObjectList(self.data, "palletkinds")
        self.boxkinds       = self.newObjectList(self.data, "boxkinds")
        self.itemkinds      = self.newObjectList(self.data, "itemkinds")

    def _fillInfo_(self):
        self.setText(self.description, "set",  self.instance.description.setname, str)
        self.setText(self.description, "name", self.instance.description.name,    str)
    
    def _fillContainers_(self):      
        for lbContainer in self.instance.containerkinds:
            baseContainer = self.newObject(self.containerkinds, "containerkind")
            self.addAttrib(baseContainer, "id", lbContainer.id, int)
            self.setText(baseContainer, "quantity", lbContainer.quantity, int)
            baseLoadingSpaces = self.newObjectList(baseContainer, "loadingspaces")
            for loadingSpace in lbContainer.loadingspaces:
                baseLoadingSpace = self.newObject(baseLoadingSpaces, "loadingspace")
                self.addAttrib(baseLoadingSpace, "id", loadingSpace.id, int)
                self.setText(baseLoadingSpace, "position", ",".join(map(str,loadingSpace.position)), str)
                size = self.newObject(baseLoadingSpace, "size")
                self.setText(size, "length", loadingSpace.boundingBox[0], int)
                self.setText(size, "width",  loadingSpace.boundingBox[1], int)
                self.setText(size, "height", loadingSpace.boundingBox[2], int)
                
                # automatic writing of optional fields
                fields = set()
                for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                    fields |= set([req for req in r.loadingspaceRequirements])
                for field, cast in set([(req.field, req.cast) for req in filter(lambda x: isinstance(x, ExistenceRequirement), fields)]):
                    if hasattr(loadingSpace, field):
                        attr = getattr(loadingSpace, field)
                        if attr is not None:
                            self.setText(baseLoadingSpace, field, attr, cast)

            # automatic writing of optional fields
            fields = set()
            for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                fields |= set([req for req in r.containerkindRequirements])
            for field, cast in set([(req.field, req.cast) for req in filter(lambda x: isinstance(x, ExistenceRequirement), fields)]):
                if hasattr(lbContainer, field):
                    attr = getattr(lbContainer, field)
                    if attr is not None:
                        self.setText(baseContainer, field, attr, cast)

    def _fillPallets_(self):
        for lbPallet in self.instance.palletkinds:
            basePallet = self.newObject(self.palletkinds, "palletkind")
            self.addAttrib(basePallet, "id", lbPallet.id, int)
            self.setText(basePallet, "quantity", lbPallet.quantity, int)
            size = self.newObject(basePallet, "size")
            self.setText(size, "length", lbPallet.boundingBox[0], int)
            self.setText(size, "width",  lbPallet.boundingBox[1], int)
            self.setText(size, "height", lbPallet.boundingBox[2], int)
            self.setText(basePallet, "position", ",".join(map(str, lbPallet.position)), str)
            loadingspace = self.newObject(basePallet, "loadingspace")
            self.addAttrib(loadingspace, "id", lbPallet.loadingspace.id, int)
            size = self.newObject(loadingspace, "size")
            self.setText(size, "length", lbPallet.loadingspace.boundingBox[0], int)
            self.setText(size, "width",  lbPallet.loadingspace.boundingBox[1], int)
            self.setText(size, "height", lbPallet.loadingspace.boundingBox[2], int)
            self.setText(loadingspace, "position", ",".join(map(str, lbPallet.loadingspace.position)), str)
            self.setText(basePallet, "orientations", ",".join(lbPallet.orientations), str)

            # automatic writing of optional fields
            fields = set()
            for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                fields |= set([req for req in r.palletkindRequirements])
            for field, cast in set([(req.field, req.cast) for req in filter(lambda x: isinstance(x, ExistenceRequirement), fields)]):
                if hasattr(lbPallet, field):
                    attr = getattr(lbPallet, field)
                    if attr is not None:
                        self.setText(basePallet, field, attr, cast)
    
    def _fillBoxes_(self):
        for lbBox in self.instance.boxkinds:
            baseBox = self.newObject(self.boxkinds, "palletkind")
            self.addAttrib(baseBox, "id", lbBox.id, int)
            self.setText(baseBox, "quantity", lbBox.quantity, int)
            size = self.newObject(baseBox, "size")
            self.setText(size, "length", lbBox.boundingBox[0], int)
            self.setText(size, "width",  lbBox.boundingBox[1], int)
            self.setText(size, "height", lbBox.boundingBox[2], int)
            self.setText(baseBox, "position", ",".join(map(str, lbBox.position)), str)
            loadingspace = self.newObject(baseBox, "loadingspace")
            self.addAttrib(loadingspace, "id", lbBox.loadingspace.id, int)
            size = self.newObject(loadingspace, "size")
            self.setText(size, "length", lbBox.loadingspace.boundingBox[0], int)
            self.setText(size, "width",  lbBox.loadingspace.boundingBox[1], int)
            self.setText(size, "height", lbBox.loadingspace.boundingBox[2], int)
            self.setText(loadingspace, "position", ",".join(map(str, lbBox.loadingspace.position)), str)
            self.setText(baseBox, "orientations", ",".join(lbBox.orientations), str)

            # automatic writing of optional fields
            fields = set()
            for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                fields |= set([req for req in r.boxkindRequirements])
            for field, cast in set([(req.field, req.cast) for req in filter(lambda x: isinstance(x, ExistenceRequirement), fields)]):
                if hasattr(lbBox, field):
                    attr = getattr(lbBox, field)
                    if attr is not None:
                        self.setText(baseBox, field, attr, cast)
            
    def _fillItems_(self):
        for lbItem in self.instance.itemkinds:
            baseItem = self.newObject(self.itemkinds, "itemkind")
            self.addAttrib(baseItem, "id", lbItem.id, int)
            self.setText(baseItem, "quantity", lbItem.quantity, int)
            size = self.newObject(baseItem, "size")
            self.setText(size, "length", lbItem.boundingBox[0], int)
            self.setText(size, "width",  lbItem.boundingBox[1], int)
            self.setText(size, "height", lbItem.boundingBox[2], int)
            self.setText(baseItem, "orientations", lbItem.GetOrientationString(), str)
            
            # automatic writing of optional fields
            fields = set()
            for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                fields |= set([req for req in r.itemkindRequirements])
            for field, cast in set([(req.field, req.cast) for req in filter(lambda x: isinstance(x, ExistenceRequirement), fields)]):
                if hasattr(lbItem, field):
                    attr = getattr(lbItem, field)
                    if attr is not None:
                        self.setText(baseItem, field, attr, cast)
            
    def _fillConstraints_(self):
        for lbConstraint in self.instance.constraints:
            baseConstraint = self.newObject(self.constraints, "constraint")
            self.addAttrib(baseConstraint, "name", lbConstraint.constraint.name, str)

    def _fillObjectives_(self):
        for lbObjective in self.instance.objectives:
            baseObjective = self.newObject(self.objectives, "objective")
            self.addAttrib(baseObjective, "name", lbObjective.objective.name, str)
            self.setText(baseObjective, "weight", lbObjective.weight, float)
            self.setText(baseObjective, "priority", lbObjective.priority, int)
        
    def _createBase_(self):
        self._createFrame_()
        self._fillInfo_()
        self._fillConstraints_()
        self._fillObjectives_()
        self._fillContainers_()
        self._fillPallets_()
        self._fillBoxes_()
        self._fillItems_()
        
if __name__=="__main__":
    exit("Don't run this file")