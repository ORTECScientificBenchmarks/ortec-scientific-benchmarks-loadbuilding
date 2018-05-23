from ..ThreeDinstance      import ThreeDinstance
from ..ThreeDcontainerkind import ThreeDcontainerkind
from ..ThreeDitemkind      import ThreeDitemkind
from ..ThreeDloadingspace  import ThreeDloadingspace
import xml.etree.ElementTree as ET

def attempt(fun, default = None):
    return (lambda x: (fun(x) if x is not None else default))

class CLBStoThreeDinstance(object):
    class Shapes(object):
        class Shape(object):
            def __init__(self, i_id = None, i_boundingBox = None):
                self.id = i_id
                self.boundingBox = i_boundingBox
            def IsValid(self):
                return self.id is not None and self.boundingBox is not None
        def __init__(self):
            self.shapes = dict()
        def addShape(self, shape):
            if not isinstance(shape, self.Shape) or not shape.IsValid(): 
                raise Exception("Shape is not valid")
            if shape.id in self.shapes: 
                raise Exception("Shape exists")
            self.shapes[shape.id] = shape
        
    class Orders(object):
        class Order(object):
            def __init__(self, i_id = None, i_count = None, i_productId = None):
                self.id = i_id
                self.count = i_count
                self.productId = i_productId
            def IsValid(self):
                return self.id is not None and self.count is not None and self.productId is not None
        def __init__(self):
            self.orders = dict()
        def addOrder(self, order):
            if not isinstance(order, self.Order) or not order.IsValid(): 
                raise Exception("Order is not valid")
            if order.id in self.orders:
                raise Exception("Order exists")
            self.orders[order.id] = order
    
    class Products(object):
        class Product(object):
            def __init__(self, i_id = None, i_weight = None, i_shapeId = None, i_orientations = None):
                self.id = i_id
                self.weight = i_weight
                self.shapeId = i_shapeId
                self.orientations = i_orientations
            def IsValid(self):
                return self.id is not None and self.weight is not None and self.shapeId is not None and self.orientations is not None
        def __init__(self):
            self.products = dict()
        def addProduct(self, product):
            if not isinstance(product, self.Product) or not product.IsValid(): 
                raise Exception("Product is not valid")
            if product.id in self.products: 
                raise Exception("Product exists")
            self.products[product.id] = product
            
    class ResourceKinds(object):
        class ResourceKind(object):
            def __init__(self, i_id = None, i_configurationId = None, i_shapeId = None):
                self.id = i_id
                self.configurationId = i_configurationId
                self.shapeId = i_shapeId
            def IsValid(self):
                return self.id is not None and self.configurationId is not None and self.shapeId is not None
        def __init__(self):
            self.resourcekinds = dict()
        def addResourceKind(self, resourcekind):
            if not isinstance(resourcekind, self.ResourceKind) or not resourcekind.IsValid(): 
                raise Exception("ResourceKind is not valid")
            if resourcekind.id in self.resourcekinds: 
                raise Exception("ResourceKind exists")
            self.resourcekinds[resourcekind.id] = resourcekind
        
    class Configurations(object):
        class Configuration(object):
            def __init__(self, i_id = None, i_capacity = None):
                self.id = i_id
                self.capacity = i_capacity
            def IsValid(self):
                return self.id is not None and self.capacity is not None
        def __init__(self):
            self.configurations = dict()
        def addConfiguration(self, configuration):
            if not isinstance(configuration, self.Configuration) or not configuration.IsValid(): 
                raise Exception("Configuration is not valid")
            if configuration.id in self.configurations: 
                raise Exception("Configuration exists")
            self.configurations[configuration.id] = configuration
        
    def _makeShapes_(self):
        elbeShapes = self.localDataElements.find('elbeshapes')
        self.shapes = self.Shapes()
        for elbeShape in elbeShapes:
            assert elbeShape.tag == 'elbeshape'
            shape = self.Shapes.Shape()
            shape.id = int(elbeShape.get("id"))
            inner = elbeShape.find('inner')
            if inner is not None:
                cuboid = inner.find('cuboid')
                length = cuboid.get('length')
                width = cuboid.get('width')
                height = cuboid.get('height')
                #position = cuboid.get('position')
            else:
                outer = elbeShape.find('outer')
                cuboid = outer.find('cuboid')
                length = cuboid.get('length')
                width = cuboid.get('width')
                height = cuboid.get('height')
                #position = cuboid.get('position')
            shape.boundingBox = list(map(attempt(int,1),[length,width,height]))
            self.shapes.addShape(shape)
    
    def _makeConfigurations_(self):
        configs = self.localDataElements.find('configurations')
        self.configurations = self.Configurations()
        for configInfo in configs:
            assert configInfo.tag == 'configuration'
            config = self.Configurations.Configuration()
            config.id = int(configInfo.get('id'))
            config.capacity = float(configInfo.get('capacity')[2:])
            self.configurations.addConfiguration(config)

    def _makeOrders_(self):
        ordersInXml  = self.localDataElements.find('orders')
        self.orders = self.Orders()
        for orderInfo in ordersInXml:
            assert orderInfo.tag == 'order'
            order = self.Orders.Order()
            order.id = int(orderInfo.get('id'))
            fields = orderInfo.find('fields')
            order.count = int(fields.get('itemCount'))
            order.productId = int(fields.get('productId'))
            self.orders.addOrder(order)
            
    def _makeProducts_(self):
        productsInXml = self.localDataElements.find('products')
        self.products = self.Products()
        for productInfo in productsInXml:
            assert productInfo.tag == 'product'
            product = self.Products.Product()
            product.id = int(productInfo.get('id'))
            try:
                product.weight = attempt(float, 0)(productInfo.get("amount")[2:])
            except Exception:
                product.weight = 0
            elbefields = productInfo.find('elbefields')
            product.shapeId = int(elbefields.get('elbeshapeId'))
            product.orientations = set(elbefields.get('allowedOrientations').split(','))
            self.products.addProduct(product)
            
    def _makeResourceKinds_(self):
        resourcekindsInXml = self.localDataElements.find('resourcekinds')
        self.resourcekinds = self.ResourceKinds()
        for resourcekindInfo in resourcekindsInXml:
            assert resourcekindInfo.tag == 'resourcekind'
            resourcekind = self.ResourceKinds.ResourceKind()
            resourcekind.id = int(resourcekindInfo.get('id'))
            fields = resourcekindInfo.find('fields')
            configurationIds = fields.get('configurationIds')
            resourcekind.configurationId = int(configurationIds)
            elbefields = resourcekindInfo.find('elbefields')
            resourcekind.shapeId = int(elbefields.get('elbeshapeId'))
            self.resourcekinds.addResourceKind(resourcekind)

    def _addItemsToInstance_(self,threeDinstance):
        for itemInfo in self.parameters.findall("order"):
            item = ThreeDitemkind()
            item.id = int(itemInfo.get("id"))
            assert item.id in self.orders.orders, 'Order %d not found' % item.id
            order = self.orders.orders[item.id]
            assert order.productId in self.products.products, 'Product %d not found' % order.productId
            product = self.products.products[order.productId]
            assert product.shapeId in self.shapes.shapes, 'Shape %d not found' % product.shapeId
            item.weight       = product.weight
            item.boundingBox  = self.shapes.shapes[product.shapeId].boundingBox
            item.quantity     = int(order.count)
            item.orientations = product.orientations
            threeDinstance.addItemkind(item)
        
    def _addResourceKindsToInstance_(self,threeDinstance):
        for resourceKindInfo in self.parameters.findall("resourcekindcombination"):
            container = ThreeDcontainerkind()
            container.id = int(resourceKindInfo.get("id"))
            assert container.id in self.resourcekinds.resourcekinds, 'ResourceKind %d not found' % container.id
            resource = self.resourcekinds.resourcekinds[container.id]
            configurationId = resource.configurationId
            assert configurationId in self.configurations.configurations, 'Configuration %d not found' % configurationId
            configuration = self.configurations.configurations[configurationId]
            container.maxWeight = configuration.capacity
            assert resource.shapeId in self.shapes.shapes, 'Shape %d not found' % resource.shapeId
            container.quantity = attempt(int,1)(resourceKindInfo.get("maxNumber"))
            for resourceKindCombination in self.localDataElements.find('resourcekindcombinations').findall("resourcekindcombination"):
                if resourceKindCombination.get("id") != resourceKindInfo.get("id"):
                    continue
                for item in resourceKindCombination.findall("item"):
                    loadingspace             = ThreeDloadingspace()
                    loadingspace.id          = int(item.get("id"))
                    loadingspace.boundingBox = self.shapes.shapes[int(item.get("resourcekind_id"))].boundingBox
                    loadingspace.position    = [0,0,0]
                    container.addLoadingspace(loadingspace)
            threeDinstance.addContainerkind(container)
        
    def __init__(self,filename):
        self.filename = filename
        self.clbsXML = ET.parse(self.filename)
        self.xmlRoot = self.clbsXML.getroot()
        self.parameters = self.xmlRoot.find('parameters')
        self.localDataElements = self.parameters.find('localDataElements')
        
        self._makeShapes_()
        self._makeConfigurations_()
        self._makeOrders_()
        self._makeProducts_()
        self._makeResourceKinds_()       
        
    def CreateThreeDinstance(self):
        threeDinstance = ThreeDinstance()
        self._addItemsToInstance_(threeDinstance)
        self._addResourceKindsToInstance_(threeDinstance)    
        return threeDinstance
        
if __name__=="__main__":
    exit("Don't run this file")