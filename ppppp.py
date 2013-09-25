from models import Model
import sys


class                                               Layout(Model):
    """Layout information for page."""


    def __init__(self):
        super(Layout, self).__init__(self.__defaults())


    def __defaults(self):
        return {'field8': {'value': {}, 'constraint': '.*'}, 'field6': {'value': 'World', 'constraint': '.*'},
                'field7': {'value': [], 'constraint': '.*'}, 'field5': {'value': 'Hello', 'constraint': '^H'},
                'width': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'},
                'id': {'value': '', 'constraint': '.*'},
                'col': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'},
                'row': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'}}


    width = property(lambda self: self.getAttribute("width"), lambda self, data: self.setAttribute('width', data))

    field8 = property(lambda self: self.getAttribute("field8"), lambda self, data: self.setAttribute('field8', data))

    col = property(lambda self: self.getAttribute("col"), lambda self, data: self.setAttribute('col', data))

    field7 = property(lambda self: self.getAttribute("field7"), lambda self, data: self.setAttribute('field7', data))

    field5 = property(lambda self: self.getAttribute("field5"), lambda self, data: self.setAttribute('field5', data))

    field6 = property(lambda self: self.getAttribute("field6"))

    id = property(lambda self: self.getAttribute("id"), lambda self, data: self.setAttribute('id', data))

    row = property(lambda self: self.getAttribute("row"), lambda self, data: self.setAttribute('row', data))


class                                               Layout2(Model):
    """"""


    def __init__(self):
        super(Layout2, self).__init__(self.__defaults())


    def __defaults(self):
        return {'field8': {'value': {}, 'constraint': '.*'}, 'field6': {'value': 'World', 'constraint': '.*'},
                'field7': {'value': [], 'constraint': '.*'}, 'field5': {'value': 'Hello', 'constraint': '^H'},
                'width': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'},
                'id': {'value': '', 'constraint': '.*'},
                'col': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'},
                'row': {'value': 0, 'constraint': '^[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?$'}}


    width = property(lambda self: self.getAttribute("width"), lambda self, data: self.setAttribute('width', data))

    field8 = property(lambda self: self.getAttribute("field8"), lambda self, data: self.setAttribute('field8', data))

    col = property(lambda self: self.getAttribute("col"), lambda self, data: self.setAttribute('col', data))

    field7 = property(lambda self: self.getAttribute("field7"), lambda self, data: self.setAttribute('field7', data))

    field5 = property(lambda self: self.getAttribute("field5"), lambda self, data: self.setAttribute('field5', data))

    field6 = property(lambda self: self.getAttribute("field6"))

    id = property(lambda self: self.getAttribute("id"), lambda self, data: self.setAttribute('id', data))

    row = property(lambda self: self.getAttribute("row"), lambda self, data: self.setAttribute('row', data))




