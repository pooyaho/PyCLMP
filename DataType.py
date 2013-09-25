__author__ = 'pooya'

class BaseType(object):

    def __new__(cls, *p, **k):
        inst = object.__new__(cls)
        return inst

    def toString(self):
        pass

    def setGenericType(self,genericType):
        self.__genericType=genericType

    def getGenericType(self):
        return self.__genericType

    def setName(self,name):
        self.__name=name

    def getName(self):
        return self.__name

class CsBoolean(BaseType):
    def toString(self):
        return "System.Boolean"


class CsComposition(BaseType):
    def toString(self):
        return super(CsComposition,self).getGenericType().toString()


class CsDateTime(BaseType):
    def  toString(self):
        return "System.DateTime"


class CsDecimal(BaseType):
    def toString(self):
        return "System.Decimal"


class CsDouble(BaseType):
    def toString(self):
        return "System.Double"


class CsFile(BaseType):
    def toString(self):
        return None


class CsInteger(BaseType):
    def toString(self):
        return "System.Int32"


class CsMoney(BaseType):
    def toString(self):
        return "System.Decimal"


class CsObject(BaseType):
    def toString(self):
        return "System.Object"


class CsString(BaseType):
    def toString(self):
        return "string"


class CsCustomType(BaseType):
    def __init__(self, typeName):
        self.__typeName = typeName

    def toString(self):
        return self.__typeName


class CsList(BaseType):
    def toString(self):
        return "System.Collections.Generic.List<%s>" % super(CsList, self).getGenericType().toString()


class CsMap(BaseType):
    def toString(self):
        return "System.Collections.HashMap"

__typeMaps = {
    "string": CsString,
    "integer": CsInteger,
    "double": CsDouble,
    "duration": None,
    "file": CsFile,
    "decimal": CsDecimal,
    "currency": CsMoney,
    "dateTime": CsDateTime,
    "map": CsMap,
    "list": CsList,
    "boolean": CsBoolean,
    "composition": CsComposition}


def createInstance(typeName, attMap):
    gType=None
    if attMap.has_key("type"):
        gType=attMap["type"]
    csType = __getType(typeName)
    csType.setName(attMap["name"])
    if gType is not None:
        genericType= __getType(gType)
        csType.setGenericType(genericType)

    return csType.toString()

def __getType(typeName):
    csType = __typeMaps[typeName]

    if csType is not None and (csType is not CsComposition):
        return BaseType.__new__(csType)
    else:
        return CsCustomType(typeName)

#print {"p":"a"}.has_key("a")