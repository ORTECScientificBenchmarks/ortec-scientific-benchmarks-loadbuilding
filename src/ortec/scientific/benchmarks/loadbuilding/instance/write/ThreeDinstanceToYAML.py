
import yaml
from collections import OrderedDict
from ...instance.write.ThreeDinstanceToBase import ThreeDinstanceToBase

def represent_unsortableordereddict(dumper, mapping, flow_style=None):
    value = []
    node = yaml.nodes.MappingNode('tag:yaml.org,2002:map', value, flow_style=flow_style)
    if dumper.alias_key is not None:
        dumper.represented_objects[dumper.alias_key] = node
    best_style = True
    if hasattr(mapping, 'items'):
        mapping = list(mapping.items())
    for item_key, item_value in mapping:
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        if not (isinstance(node_key, yaml.nodes.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.nodes.ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dumper.default_flow_style is not None:
            node.flow_style = dumper.default_flow_style
        else:
            node.flow_style = best_style
    return node

class ThreeDinstanceToYAML(ThreeDinstanceToBase):
    class UnsortableList(list):
        def sort(self, *args, **kwargs):
            pass

    class UnsortableOrderedDict(OrderedDict):
        def items(self, *args, **kwargs):
            return ThreeDinstanceToYAML.UnsortableList(OrderedDict.items(self, *args, **kwargs))

    @staticmethod
    def newObject(container, new_obj):
        if isinstance(container, list):
            obj = ThreeDinstanceToYAML.UnsortableOrderedDict()
            container.append(obj)
            return obj
        else:
            container[new_obj] = ThreeDinstanceToYAML.UnsortableOrderedDict()
            return container[new_obj]
    
    @staticmethod
    def newObjectList(container, new_obj):
        container[new_obj] = list()
        return container[new_obj]
    
    @staticmethod
    def addAttrib(container, attr, val, cast):
        container[attr] = cast(val)
    
    @staticmethod
    def setText(container, tag, text, cast):
        container[tag] = cast(text)
        
    @staticmethod 
    def createBase():
        return ThreeDinstanceToYAML.UnsortableOrderedDict()
    
    def WriteInstance(self,filename):
        self._createBase_()
        with open(filename,'w') as f:
            yaml.dump(self.base, f, default_flow_style = False)
            
yaml.add_representer(ThreeDinstanceToYAML.UnsortableOrderedDict, represent_unsortableordereddict)
        
if __name__=="__main__":
    exit("Don't run this file")