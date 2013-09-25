#class A:
#
#    def toString(self):
#    def setString(self, s):
#        print "in setter %s" % s
#    string = property(toString, setString)
#a=A()
#class ModelContainer(BaseType):
#    pass # todo change this
#class ClassContainer(BaseType):
#    def __init__(self, filePath, schemaPath):
#        self.__filePath = filePath, self.__schemaPath = filePath, schemaPath
#
#    def fillContainer(self):
#        x = XmlDataModelUtils(self.__filePath, self.__schemaPath)
#        self.__className = x.getAttributeValue("dataModel","name")
#        definedTypes=x.getDefinedTypes()
#
from test2 import Model

a = {'atts': [], 'name': '', 'children': []}

class A(Model):
    def __init__(self):
        super(A, self).__init__(self.__defaults())

    #    def __setattr__(self, name, value):
    ##        print "in set"
    #        super(A,self).setAttribute(name,value)

    def __defaults(self):
        return {"__a": "11"}

    #    def __getattribute__(self, name):
    ##        print "in get"
    #        return super(A, self).getAttribute(name)


    a = property(lambda self: self.getAttribute("__a"), lambda self, data: self.setAttribute('__a', data))


b = A()
b.a = "12"
print b.a