import DataType

__author__ = 'pooya'

from io import StringIO
from tokenize import generate_tokens
import libxml2


class XpathResult:
    def __init__(self, filePath, schemaPath):
        self.__doc = libxml2.parseFile(filePath)
        self.__ctxt = self.__doc.xpathNewContext()
        self.__ctxt.xpathRegisterNs("app", schemaPath)

    def getXpathResult(self, xpathQuery):
        xpathQueryWithNs = self.__makeXpathQueryWithNS(xpathQuery)
        res = self.__ctxt.xpathEval(xpathQueryWithNs)
        return  res

    def __getNs(self):
        return "app"

    def __makeXpathQueryWithNS(self, xpathQuery):
        s = unicode(xpathQuery)
        #    result = []
        g = generate_tokens(StringIO(s).readline)   # tokenize the string
        string = ""
        prevToken = ""
        for _, tokval, _, _, _ in g:
            if prevToken != "@" and tokval.isalpha() and  prevToken != "/@":
                string += self.__getNs() + ":" + tokval
            else:
                string += tokval
            prevToken = tokval
        return  string

    def __del__(self):
        self.__doc.freeDoc()
        self.__ctxt.xpathFreeContext()


class XmlUtil:
    def __init__(self, xmlNode):
        self.__xmlNode = xmlNode

    def getAttributesMapFromNode(self):
        if self.__xmlNode is None:
            return {}
        a = {}
        for i in self.__xmlNode.properties:
            a[i.name] = i.content
        return  a

    def getChild(self, childName):
        if self.__xmlNode is None:
            return None
        if  self.__xmlNode.get_children() is None:
            return  None
        for c in self.__xmlNode.get_children():
            if c.name == childName:
                return c

    def getChildMapFromNode(self, childName):
        children = self.getChild(childName)
        tMap = {}
        if children is None or children.get_children() is None:
            return {}

        for node in children.get_children():
            if node.type == "element":
                tMap[node.name] = node.content
        return tMap

#xpath = XpathResult("datamodel/main.xml", "DataModel.xsd")
#xmlNode = xpath.getXpathResult("//dataModel/elements/*")
#for i in xmlNode:
#    xmlUtil = XmlUtil(i)
#    childMap = xmlUtil.getChildMapFromNode("restriction")
#    for index, k in enumerate(childMap):
#        print i.name, k, childMap[k]
class XmlDataModelUtils:
    BASE_NODE = "dataModel"

    def __init__(self, filePath, schemaPath):
        self.__xpathR = XpathResult(filePath, schemaPath)

    def getAttributeValue(self, nodeName, attName):
        result = self.__xpathR.getXpathResult("//" + nodeName + "/@" + attName)
        if len(result) <= 0:
            return None
        return result[0].content

    def getDataTypes(self):
        types = self.__xpathR.getXpathResult("//dataModel/elements/*")
        a = []
        for dataType in types:
            util = XmlUtil(dataType)
            b =\
                {"type": dataType.name,
                 "node": dataType,
                 "atts": util.getAttributesMapFromNode(),
                 "rests": util.getChildMapFromNode("restriction")
            }
            a.append(b)
        return a


    def getDataType(self, typeName):
        dType = self.__xpathR.getXpathResult("//dataModel/elements/*[@name=\"%s\"]" % typeName)
        if len(dType) <= 0 or len(dType) > 1:
            return  None
        return dType[0]

    def getDefinedTypes(self):
        return self.__xpathR.getXpathResult("//dataModel/type")

    def getRestrictionsOfType(self, typeName):
        node = self.getDataType(typeName)
        xUtils = XmlUtil(node)
        return xUtils.getChildMapFromNode("restriction")

    def getName(self):
        return self.getAttributeValue("dataModel", "name")


class CsDataModel(object):
    def __init__(self, filePath, schemaPath):
        self.__xDM = XmlDataModelUtils(filePath, schemaPath)

    def generateString(self):
        template = "Class %s {\n" % self.__xDM.getName()

        for dataType in self.__xDM.getDataTypes():
            attMap = dataType["atts"]
            typeN = dataType["type"]
            csTypeName = DataType.createInstance(typeN, attMap)
            template += "public %s %s {get ; set;}\n" % (csTypeName, attMap["name"])

        template += "}"
        return template

#
#        return  template

#xpath = XpathResult("resource/datamodel/main.xml", "DataModel.xsd")
#for i in  xpath.getXpathResult("//dataModel/elements/*[@name=\"bc\"]"):
#    print i

xpath = XpathResult("resource/datamodel/test.xml", "container.xsd")
for i in  xpath.getXpathResult("//container/widget/*[@name=\"lblfirstName\"]"):
    print i
    a=XmlUtil(i)
    print a.getAttributesMapFromNode()
#for i in xmlNode:
#    xmlUtil = XmlUtil(i)
#    childMap = xmlUtil.getChildMapFromNode("restriction")
#    for index, k in enumerate(childMap):
#        print i.name, k, childMap[k]