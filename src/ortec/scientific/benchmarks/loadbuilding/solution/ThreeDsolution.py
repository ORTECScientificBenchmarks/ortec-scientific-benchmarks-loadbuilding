from ..common.Requirements import BaseRequirement, ExistenceRequirement
from ..common.NgoiMatrix import NgoiMatrix
from ..common.utils import key, Report, checkDuplicateIds
from operator import le, eq

from ..instance.ThreeDdescription import ThreeDdescription
from .ThreeDcontainer import ThreeDcontainer
from .ThreeDpallet    import ThreeDpallet
from .ThreeDbox       import ThreeDbox
from .ThreeDplacement import ThreeDplacement

class ThreeDsolution(object):
    def __init__(self, threeDinstance):
        self.threeDinstance = threeDinstance
        self.description = ThreeDdescription()
        self.containers  = list()
        self.pallets     = list()
        self.boxes       = list()
        self.unplaced    = list()
        self.decorated   = False
    
    def sort(self):
        if self.threeDinstance != None:
            self.threeDinstance.sort()
        if self.containers != None:
            self.containers.sort(key=key("id"))
            for container in self.containers:
                if container != None:
                    container.sort()
        if self.pallets != None:
            self.pallets.sort(key=key("id"))
            for pallet in self.pallets:
                if pallet != None:
                    pallet.sort()
        if self.boxes != None:
            self.boxes.sort(key=key("id"))
            for box in self.boxes:
                if box != None:
                    box.sort()
        if self.unplaced != None:
            self.unplaced.sort(key=key("id"))
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        self.sort()
        other.sort()
        return self.__dict__ == other.__dict__

    def __ne__(self,other):
        return not self.__eq__(other)

    def addContainer(self, container):
        if not isinstance(container, ThreeDcontainer):
            raise Exception("Expected a container")
        self.containers.append(container)
        self.decorated = False

    def addPallet(self, pallet):
        if not isinstance(pallet, ThreeDpallet):
            raise Exception("Expected a pallet")
        self.pallets.append(pallet)
        self.decorated = False

    def addBox(self, box):
        if not isinstance(box, ThreeDbox):
            raise Exception("Expected a box")
        self.boxes.append(box)
        self.decorated = False

    def addUnplaced(self, unplaced):
        if not isinstance(unplaced, ThreeDplacement):
            raise Exception("Expected a placement")
        self.unplaced.append(unplaced)
        self.decorated = False

    def GetAllPlacements(self):
        placements = list(self.unplaced) # make a shallow copy of self.unplaced
        for container in self.containers:
            for loadingspace in container.loadingspaces:
                for placement in loadingspace.placements:
                    placements.append(placement)
        for pallet in self.pallets:
            for placement in pallet.loadingspace.placements:
                placements.append(placement)
        for box in self.boxes:
            for placement in box.loadingspace.placements:
                placements.append(placement)
        return placements
    
    def CheckDescriptionEquivalence(self):
        if self.description != self.threeDinstance.description:
            return False, "Instance and solution descriptions are not equivalent. <- VIOLATION"
        return True, "Instance and solution descriptions are equivalent."

    # Checks two things (default: cmp = operator.le):
    #     \forall o in objs:  o.kindid in kinds
    #     \forall k in kinds: cmp(# of objs of kind k, k.quantity)
    @staticmethod
    def CountOccurrences(kinds, objs, attribute, label, cmp=le):
        valid, warnings = True, [""]
        for used_kind in sorted([getattr(obj, attribute) for obj in objs]):
            if used_kind not in [kind.id for kind in kinds]:
                valid = False
                warnings.append(label.capitalize() + " of kind " + str(used_kind) + " not present in instance file <- VIOLATION")
        for kind in kinds:
            count = sum([obj.quantity if hasattr(obj, "quantity") else 1 for obj in objs if getattr(obj, attribute) == kind.id])
            temp  = label.capitalize() + " of kind " + str(kind.id) + ": " + str(count) + "/" + str(kind.quantity)
            if not cmp(count, kind.quantity):
                valid = False
                temp += " <- VIOLATION"
            warnings.append(temp)
        if valid:
            return True, "All " + label + " counts were within bounds."
        return False, "Not all " + label + " counts were within bounds:" + "\n\t- ".join(warnings)
    
    @staticmethod
    def CheckPlacedAndLoaded(definitions, placements, attribute, label):
        valid, warnings = True, [""]
        definition_ids = set()
        placement_ids  = set()
        multiple_definitions = set()
        multiple_placements  = set()
        for definition in definitions:
            if definition.id in definition_ids:
                valid = False
                multiple_definitions.add(definition.id)
            else:
                definition_ids.add(definition.id)
        for placement in placements:
            if getattr(placement, attribute) in placement_ids:
                valid = False
                multiple_placements.add(getattr(placement, attribute))
            else:
                placement_ids.add(getattr(placement, attribute))
        for def_id in multiple_definitions:
            warnings.append("Multiple loading patterns of " + label + " with id " + str(def_id) + " <- VIOLATION")
        for pla_id in multiple_placements:
            warnings.append("Multiple placements of " + label + " with " + attribute + " " + str(pla_id) + " <- VIOLATION")
        if valid:
            for unplaced_definition in definition_ids.difference(placement_ids):
                valid = False
                warnings.append(label.capitalize() + " loading pattern with id " + str(unplaced_definition) + " has no corresponding placement <- VIOLATION")
            for undefined_placement in placement_ids.difference(definition_ids):
                valid = False
                warnings.append(label.capitalize() + " placement with " + attribute + " " + str(undefined_placement) + " has no corresponding loading pattern <- VIOLATION")
            if valid:
                return True, "All " + label + " placements/loading patterns were correct."
        return False, "Not all " + label + " placements/loading patterns were correct:" + "\n\t- ".join(warnings)
        
    @staticmethod
    def ExcludePlaceInside(objs, excluded_type, label):
        valid, warnings = True, [""]
        for obj in objs:
            loadingspaces = []
            if hasattr(obj, "loadingspaces"):
                loadingspaces = obj.loadingspaces
            elif hasattr(obj, "loadingspace"):
                loadingspaces = [obj.loadingspace]
            for loadingspace in loadingspaces:
                for placement in loadingspace.placements:
                    if getattr(placement, excluded_type + "id") != None:
                        valid = False
                        warnings.append(obj.TypeString().capitalize() + " with id " + str(obj.id) + " contained " + excluded_type + " with id " + str(placement.id)) + " <- VIOLATION"
        return valid, ("All" if valid else "Not all") + " " + excluded_type + "->" + label + " exclusions were adhered to" + ("." if valid else ":" + "\n\t- ".join(sorted(warnings)))

    @staticmethod
    def CheckLoadingspaceIds(kinds, objs, label):
        valid, warnings = True, [""]
        loadingspaces_by_kind = {}
        for kind in kinds:
            if hasattr(kind, "loadingspaces"):
                loadingspaces_by_kind[kind.id] = {loadingspace.id for loadingspace in kind.loadingspaces}
            elif hasattr(kind, "loadingspace"):
                loadingspaces_by_kind[kind.id] = {kind.loadingspace.id}
        for obj in objs:
            kind_loadingspace = loadingspaces_by_kind[obj.kindid]
            obj_loadingspaces = set()
            if hasattr(obj, "loadingspaces"):
                obj_loadingspaces = {loadingspace.id for loadingspace in obj.loadingspaces}
            elif hasattr(obj, "loadingspace"):
                obj_loadingspaces = {obj.loadingspace.id}
            if not obj_loadingspaces.issubset(kind_loadingspace):
                valid = False
                warnings.append("Loadingspace(s) with id(s) " + ", ".join(map(str,obj_loadingspaces.difference(kind_loadingspace))) + " in " + label + " with id " + str(obj.id) + " <- VIOLATION")
        return valid, ("All" if valid else "Not all") + " " + label + " loadingspace ids were defined in instance" + ("." if valid else ":" + "\n\t- ".join(warnings))
        
    def IsValid(self):
        placed_pallets = [placement for placement in self.GetAllPlacements() if placement.palletid is not None]
        placed_boxes   = [placement for placement in self.GetAllPlacements() if placement.boxid is not None]
        placed_items   = [placement for placement in self.GetAllPlacements() if placement.itemid is not None]
        
        report = Report()
        # Check if the description is valid
        report.add(self.description.IsValid())
        report.add(self.CheckDescriptionEquivalence())

        # Check duplicate ids of containers, loadingspaces, pallets, boxes, placements
        report.add(checkDuplicateIds(self.containers))
        for container in self.containers:
            report.add(checkDuplicateIds(container.loadingspaces))
        report.add(checkDuplicateIds(self.pallets))
        report.add(checkDuplicateIds(self.boxes))
        report.add(checkDuplicateIds(self.GetAllPlacements()))
        
        # Check whether box ids / pallet ids of placements are defined and used exactly once
        report.add(self.CheckPlacedAndLoaded(self.pallets, placed_pallets, "palletid", "pallet"))
        report.add(self.CheckPlacedAndLoaded(self.boxes,   placed_boxes,   "boxid",    "box"))
        
        # Check if quantity of referenced kinds do not exceed the allowed number (for itemkinds they must correspond exactly)
        report.add(self.CountOccurrences(self.threeDinstance.containerkinds, self.containers, "kindid", "container"))
        report.add(self.CountOccurrences(self.threeDinstance.palletkinds,    self.pallets,    "kindid", "pallet"))
        report.add(self.CountOccurrences(self.threeDinstance.boxkinds,       self.boxes,      "kindid", "box"))
        report.add(self.CountOccurrences(self.threeDinstance.itemkinds,      placed_items,    "itemid", "item", eq))
        
        # Check if pallets do not occur in pallets or boxes, and boxes do not occur in boxes
        report.add(self.ExcludePlaceInside(self.pallets, "pallet", "pallet"))
        report.add(self.ExcludePlaceInside(self.boxes,   "pallet", "box"))
        report.add(self.ExcludePlaceInside(self.boxes,   "box",    "box"))
        
        # Check correspondence of loadingspace ids to those of the instance file
        report.add(self.CheckLoadingspaceIds(self.threeDinstance.containerkinds, self.containers, "container"))
        report.add(self.CheckLoadingspaceIds(self.threeDinstance.palletkinds,    self.pallets,    "pallet"))
        report.add(self.CheckLoadingspaceIds(self.threeDinstance.boxkinds,       self.boxes,      "box"))

        # Check if all containers, pallets, boxes, and placements are valid
        for container in self.containers:
            report.add(container.IsValid())
        for pallet in self.pallets:
            report.add(pallet.IsValid())
        for box in self.boxes:
            box.add(pallet.IsValid())
        for placement in self.unplaced:
            report.add(placement.IsValid())

        if not report.get()[0]:
            return report.get()
        
        self.DecorateSolution()
        
        report.add(self.CheckOverlapInside())
        return report.get()

    def DecorateLoadingspace(self, loadingspace):
        loadingspace.ngoi = None
        if hasattr(loadingspace, "boundingBox"):
            loadingspace.ngoi = NgoiMatrix(*loadingspace.boundingBox)
            for placement in sorted(loadingspace.placements, key=lambda x: x.position[2]):
                if not hasattr(placement, "support") or placement.support is None:
                    placement.support = 0.0
                if placement.boundingBox is not None and placement.support is not None:
                    loadingspace.ngoi.addCuboid(placement)

    # TODO: decorate box + pallet
    def DecoratePlacement(self, placement):
        placement.correct      = True
        placement.boundingBox  = None
        placement.orientations = None
        if placement.itemid is not None:
            placement.type = "item"
            for itemkind in self.threeDinstance.itemkinds:
                if itemkind.id != placement.itemid:
                    continue
                placement.boundingBox  = itemkind.boundingBox
                placement.orientations = itemkind.orientations
                for field in self.itemkindFields:
                    if hasattr(itemkind, field):
                        setattr(placement, field, getattr(itemkind, field))
                break
        elif placement.boxid is not None:
            placement.type = "box"
            placement.kindid = None
            for box in self.boxes:
                if box.id == placement.boxid:
                    placement.kindid       = box.kindid
                    placement.loadingspace = box.loadingspace
            for boxkind in self.threeDinstance.boxkinds:
                if boxkind.id != placement.kindid:
                    continue
                placement.boundingBox  = boxkind.boundingBox
                placement.orientations = boxkind.orientations
                for field in self.boxkindFields:
                    if hasattr(boxkind, field):
                        setattr(placement, field, getattr(boxkind, field))
                break
        else:
            # TODO: test
            placement.type = "pallet"
            placement.kindid = None
            for pallet in self.pallets:
                if pallet.id == placement.palletid:
                    placement.kindid       = pallet.kindid
                    placement.loadingspace = pallet.loadingspace
            for palletkind in self.threeDinstance.palletkinds:
                if palletkind.id != placement.kindid:
                    continue
                placement.orientations = palletkind.orientations
                for field in self.palletkindFields:
                    if hasattr(palletkind, field):
                        setattr(placement, field, getattr(palletkind, field))
                pallet_min = list(palletkind.position)
                pallet_max = list(map(sum,zip(pallet_min, palletkind.boundingBox)))
                placements_min = list(map(min,zip(*map(lambda x: x.position,               palletkind.loadingspace.placements))))
                placements_max = list(map(max,zip(*map(lambda x: x.position+x.boundingBox, palletkind.loadingspace.placements))))
                loadingspace_min = list(map(sum,zip(palletkind.loadingspace.position, placements_min)))
                loadingspace_max = list(map(sum,zip(palletkind.loadingspace.position, placements_max)))
                
                min_coords = list(map(min,zip(pallet_min,loadingspace_min)))
                max_coords = list(map(max,zip(pallet_max,loadingspace_max)))
                max_coords = list(map(lambda x: x[0]-x[1], zip(max_coords, min_coords)))

                placement.position    = list(map(sum, zip(placement.position, min_coords)))
                placement.boundingBox = list(map(sum, zip(placement.position, max_coords)))
                break
        if placement.boundingBox is not None and placement.boundingBox != 'UNPLACED' and\
           placement.orientation is not None and placement.orientation != 'UNPLACED':
            l_index = placement.orientation.upper().find("L")
            w_index = placement.orientation.upper().find("W")
            h_index = placement.orientation.upper().find("H")
            permutation = [l_index, w_index, h_index]
            placement.boundingBox = [placement.boundingBox[i] for i in permutation]
            
    # Will attempt to 'decorate' the solution by adding instance fields to the solution object, such as bounding boxes, orientations, etc.
    def DecorateSolution(self):
        if not self.decorated:
            self.containerkindFields = set()
            self.palletkindFields    = set()
            self.boxkindFields       = set()
            self.itemkindFields      = set()
            self.loadingspaceFields  = set()
            for r in BaseRequirement.OBJECTIVE_LIST + BaseRequirement.CONSTRAINT_LIST:
                self.containerkindFields |= set([req.field for req in r.containerkindRequirements if isinstance(req, ExistenceRequirement)])
                self.palletkindFields    |= set([req.field for req in r.palletkindRequirements    if isinstance(req, ExistenceRequirement)])
                self.boxkindFields       |= set([req.field for req in r.boxkindRequirements       if isinstance(req, ExistenceRequirement)])
                self.itemkindFields      |= set([req.field for req in r.itemkindRequirements      if isinstance(req, ExistenceRequirement)])
                self.loadingspaceFields  |= set([req.field for req in r.loadingspaceRequirements  if isinstance(req, ExistenceRequirement)])
            for container in self.containers:
                for containerkind in self.threeDinstance.containerkinds:
                    if containerkind.id != container.kindid:
                        continue
                    for loadingspace in container.loadingspaces:
                        for ls_inst in containerkind.loadingspaces:
                            if loadingspace.id != ls_inst.id:
                                continue
                            loadingspace.boundingBox = ls_inst.boundingBox
                            loadingspace.position    = ls_inst.position
                            for field in self.loadingspaceFields:
                                setattr(loadingspace, field, getattr(ls_inst, field))
                            break
                        for placement in loadingspace.placements:
                            self.DecoratePlacement(placement)
                        self.DecorateLoadingspace(loadingspace)
                    for field in self.containerkindFields:
                        setattr(container, field, getattr(containerkind, field))
                    break
            for pallet in self.pallets:
                for palletkind in self.threeDinstance.palletkinds:
                    if palletkind.id != pallet.kindid:
                        continue
                    pallet.loadingspace.boundingBox = palletkind.loadingspace.boundingBox
                    pallet.loadingspace.position    = palletkind.loadingspace.position
                    for field in self.loadingspaceFields:
                        setattr(pallet.loadingspace, field, getattr(palletkind.loadingspace, field))
                    for field in self.palletkindFields:
                        setattr(pallet, field, getattr(palletkind, field))
                    break
                for placement in pallet.loadingspace.placements:
                    self.DecoratePlacement(placement)
                self.DecorateLoadingspace(pallet.loadingspace)
            for box in self.boxes:
                for boxkind in self.threeDinstance.boxkinds:
                    if boxkind.id != box.kindid:
                        continue
                    box.loadingspace.boundingBox = boxkind.loadingspace.boundingBox
                    box.loadingspace.position    = boxkind.loadingspace.position
                    for field in self.loadingspaceFields:
                        setattr(box.loadingspace, field, getattr(boxkind.loadingspace, field))
                    for field in self.boxkindFields:
                        setattr(box, field, getattr(boxkind, field))
                    break
                for placement in box.loadingspace.placements:
                    self.DecoratePlacement(placement)
                self.DecorateLoadingspace(box.loadingspace)
            for placement in self.unplaced:
                self.DecoratePlacement(placement)
            self.decorated = True

    def CheckOverlapInside(self):
        overlap_valid, overlap = True, [""]
        outside_valid, outside = True, [""]
        for container in self.containers:
            for loadingspace in container.loadingspaces:
                outside += loadingspace.ngoi.outside_report
                overlap += loadingspace.ngoi.overlap_report
                outside_valid = outside_valid and loadingspace.ngoi.outside_valid
                overlap_valid = overlap_valid and loadingspace.ngoi.overlap_valid
        for pallet in self.pallets:
            outside += pallet.loadingspace.ngoi.outside_report
            overlap += pallet.loadingspace.ngoi.overlap_report
            outside_valid = outside_valid and pallet.loadingspace.ngoi.outside_valid
            overlap_valid = overlap_valid and pallet.loadingspace.ngoi.overlap_valid
        for box in self.boxes:
            outside += box.loadingspace.ngoi.outside_report
            overlap += box.loadingspace.ngoi.overlap_report
            outside_valid = outside_valid and box.loadingspace.ngoi.outside_valid
            overlap_valid = overlap_valid and box.loadingspace.ngoi.overlap_valid
        warnings = ""
        if outside_valid:
            warnings = "All placements lie inside their loadingspace."
        else:
            warnings = "Not all placements lie inside their loadingspace:" + "\n\t- ".join(outside)
        warnings += "\n"
        if overlap_valid:
            warnings += "No overlapping placements."
        else:
            warnings += "Some placements overlap:" + "\n\t- ".join(overlap)
        return outside_valid and overlap_valid, warnings

    # Returns a list of weighted objective values (ordered according to the priorities)
    # Note that the list ordering in Python is lexicographic by default and so comparison is straightforward
    def EvaluateObjectives(self):
        self.DecorateSolution()
        result = {"individual": []}
        objective_values = {}
        for objective in self.threeDinstance.objectives:
            new_objective = {"name": objective.objective.name}
            value = objective.objective.Evaluate(self)
            new_objective["value"] = value
            result["individual"].append(new_objective)
            weighted = objective.weight * value
            if objective.priority in objective_values:
                objective_values[objective.priority] += weighted
            else:
                objective_values[objective.priority] = weighted
        lexicographic = list()
        for _,v in sorted(objective_values.items()):
            lexicographic.append(v)
        result["total"] = lexicographic
        return result

    # Checks whether all constraints are valid, and returns a report on which constraints were and were not
    def ValidateConstraints(self):
        self.DecorateSolution()
        self.sort()
        result = []
        for constraint in self.threeDinstance.constraints:
            new_constraint = {"name": constraint.constraint.name}
            new_constraint["valid"], new_constraint["warnings"] = constraint.constraint.Validate(self)
            result.append(new_constraint)
        return result

    def PrintResults(self):
        result = self.GetResults()
        if result["validity"]["value"]:
            valid = True
            print("Solution of '%s':" % (self.description.InstanceName()) )
            for constraint in result["constraints"]:
                valid = valid and constraint["valid"]
                print(constraint["warnings"])
            value = result["objectives"]["total"]
            print("Objective = " + str(value))
        else:
            print(result["validity"]["warnings"])

    def GetResults(self):
        result = {}
        result["validity"] = {}
        result["validity"]["value"], result["validity"]["warnings"] = self.IsValid()
        if result["validity"]["value"]:
            result["constraints"] = self.ValidateConstraints()
            result["objectives"]  = self.EvaluateObjectives()
        return result
    
if __name__=="__main__":
    exit("Don't run this file")