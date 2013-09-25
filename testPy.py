__author__ = 'root'


class pooya(object):

    def __new__(cls, *p, **k):
        inst = object.__new__(cls)
        return inst

    def __init__(self):
        super(pooya, self).__init__()

    def printE(self):
        print "aaaaaaaaaaaaaaa"

    def __class__(self, *args, **kwargs):
        return super(pooya, self).__class__(*args, **kwargs)

__author__ = 'namnik'





def generateClass(fields, className):

    classText = "class %s : \n" % className

    for field in fields:
        cField=field.capitalize()
        fField=field[0].lower()+field[1:]
        classText += "\tdef get{0}(self):\n\t\treturn self.__{1}\n".format(cField,fField)

        classText += "\tdef set{0}(self,{1}):\n\t\tself.__{1}={1}\n".format(cField,fField)

    return classText

class A(object):

    def __new__(cls, *p, **k):
        inst = object.__new__(cls)
        return inst

    def getString(self):
        pass

class B(A):
    def getString(self):
        return "B"

class C(A):
    def getString(self):
        return "C"

myMap={"B":B,"C":C}

b=myMap["B"]
print A(b).getString()