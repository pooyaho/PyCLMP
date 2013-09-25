#!/usr/bin/python
from optparse import OptionParser
import sys

from string import Template

classTemplate = Template("""

class $name(Model):
    \"\"\"$documentation\"\"\"

    def __init__(self):
        super($name, self).__init__(self.__defaults())

    def __defaults(self):
        return $defaultValues

    $properties

""")

getterSetterTemplate = Template("""
    $name=property(lambda self: self.getAttribute("$name"), lambda self, data: self.setAttribute('$name', data))
""")

getterTemplate = Template("""
    $name=property(lambda self: self.getAttribute("$name"))
""")


def buildModel(name, documentation, fields):
    def _typeOf(desc):
        if type(desc) == dict and desc.has_key("type"):
            return desc["type"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 0:
            return desc[0]
        elif type(desc) == str:
            return desc
        else:
            return "str"

    def _safeTypeOf(desc):
        t = _typeOf(desc)
        if t in ("str", "number", "bool", "list", "dict"):
            return t
        else:
            raise TypeError, "Invalid field type '%s'" % t

    def _defaultValueOf(desc):
        if type(desc) == dict and desc.has_key("default"):
            return desc["default"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 1:
            return desc[1]
        else:
            return None

    def _safeDefaultValueOf(desc):
        v = _defaultValueOf(desc)
        if v is None:
            defVals = {"str": "", "number": 0, "bool": False, "list": [], "dict": {}}
            return defVals[_safeTypeOf(desc)]
        else:
            return v

    def _isReadOnly(desc):
        if type(desc) == dict and desc.has_key("readOnly"):
            return desc["readOnly"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 2:
            return desc[2]
        else:
            return False

    def _documentationOf(desc, doc=""):
        if type(desc) == dict and desc.has_key("doc"):
            return desc["doc"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 4:
            return desc[4]
        else:
            return doc

    def _matchConditionOf(desc):
        m = None
        if type(desc) == dict and desc.has_key("regexp"):
            m = desc["regexp"]
        elif (type(desc) == list or type(desc) == tuple) and len(desc) > 3:
            m = desc[3]

        if m is None:
            if desc == "str":
                return ".*"
            elif desc == "number":
                return "^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$"
            elif desc == "bool":
                return "^(True|False|true|false)$"
            else:
                return ".*"
        else:
            return m

    initialFields = {}
    properties = ""

    for k in fields.keys():
        desc = fields[k]
        initialFields[k] = {"value": _safeDefaultValueOf(desc), "constraint": _matchConditionOf(desc)}
        if _isReadOnly(desc):
            properties = properties + getterTemplate.substitute(
                    {"name": k, "documentation": _documentationOf(desc, "Property for   %s" % k)})
        else:
            properties = properties + getterSetterTemplate.substitute(
                    {"name": k, "documentation": _documentationOf(desc, "Property for   %s" % k)})

    return classTemplate.substitute({"name": name, "documentation": documentation, "defaultValues": initialFields,
                                     "properties": properties})


def trim(docstring):
    if not docstring:
        return ''
        # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
            # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
            # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
        # Return a single string:
    return '\n'.join(trimmed)


def loadTemplate(templatePath):
    fileData = ""
    f = open(templatePath, "r")
    for line in f.readlines():
        fileData += line + "\n"

    return Template(fileData)


def main():
    def __createOptions():
        usage = "usage: %prog [options] [-c ClassTemplate] [-s GetterSetterTemplate] [-g GetterTemplate] [Input "\
                "Definition "\
                "Files]"
        parser = OptionParser(usage)
        parser.add_option("-c", "--class_template",
                          action="store", type="string", dest="ctemplate",
                          help="Input template file for Class Template")
        parser.add_option("-s", "--setget_template",
                          action="store", type="string", dest="gstemplate",
                          help="Input template file for Getter and Setter "\
                               "Template")
        parser.add_option("-g", "--get_template",
                          action="store", type="string", dest="gtemplate",
                          help="Input template file for Getter Template")

        return parser.parse_args()


    (options, args) = __createOptions()
    if options.gtemplate is not None:
        global getterTemplate
        getterTemplate = loadTemplate(options.gtemplate)

    if options.gstemplate is not None:
        global getterSetterTemplate
        getterSetterTemplate = loadTemplate(options.gstemplate)
    if options.ctemplate is not None:
        global classTemplate
        classTemplate = loadTemplate(options.ctemplate)

    #for arg in sys.argv[1:]:
    #    Template.()
    variables = {}
    local = {}
    for arg in args:
        execfile(arg, {}, local)
        header = """from models import Model
                       import sys"""

        #print variables["a"]
        if local.has_key("output"):
            output = local["output"]
        else:
            raise Exception, "Define output in your file!"

        if local.has_key("header"):
            header = local["header"]

        f = open(output, 'w')
        f.write(trim(header))

        for _, k in enumerate(local):
            content = local[k]

            if type(content) == list and  len(content) >= 3 and type(content[2] == dict):
                f.write(buildModel(content[0], content[1], content[2]))
            if type(content) == dict and len(content) >= 3:
                if content.has_key("name") and content.has_key("fields"):
                    if content.has_key("comment"):
                        f.write(buildModel(content["name"], "", content["fields"]))
                    else:
                        f.write(buildModel(content["name"], content["comment"], content["fields"]))

        f.close()


if __name__ == "__main__":
    main()