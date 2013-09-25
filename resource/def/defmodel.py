__author__ = 'pooya'

output = "ppppp.py"
header = """from models import Model
          import sys"""
a = [
    "Layout",
    "Layout information for page.",
        {
        "id": (),
        "row": ("number"),
        "col": ("number"),
        "width": ("number"),
        "field5": ("str", "Hello", False, "^H"),
        "field6": ("str", "World", True, None, "Documentation of field6"),
        "field7": ("list"),
        "field8": ("dict")
    }]

b = {"name": "Layout2", "comment": "Layout information for page.",
     "fields":
        {
        "id": (),
        "row": ("number"),
        "col": ("number"),
        "width": ("number"),
        "field5": ("str", "Hello", False, "^H"),
        "field6": ("str", "World", True, None, "Documentation of field6"),
        "field7": ("list"),
        "field8": ("dict")
    }}