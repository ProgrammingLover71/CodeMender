from src.main import *

class Person:
    def __init__(self, age: float):
        self.age = age
    
    def is_adult(self):
        return self.age >= 18


class PersonIsAdultPatch(CodeMender.MethodPatch):
    def postfix(self, target, call_res: Any, *orig_args, **orig_kwds):
        age = getattr(target, "age")
        return age >= 21

person = Person(20.0)

patch = PersonIsAdultPatch("person_patch_0", person, "is_adult")

print(person.is_adult()) # Original Method
patch.apply()
print(person.is_adult()) # Patched Method
