#### 	This is a test_script_1.py (TODO NE dirati tabove u komentarima)

def add_10       (value):
    return value 	+    10 # \t

import os, sys
from math import sqrt, pow

class Person:
    import time
    def __init__	(   self,name,age =      18    ) -> None: # \t 
        self.name =     name
        self.age   =    age
    def get_name(self):
        return self.name
import json
class Animal:
    def __init__  (self,species     ,age        = 1	): # \t
        pass

# New class for detecting violations
class ViolationDetector:
    def __init__     (self, violations):
        self.violations = violations


    def process_violations(self):
        for violation in self.violations:
            print("Violation detected:", violation)

def func_increment(i):
    i=i+1 # missing_whitespace_around_operator

# Intentional violations for testing detection
ham = [1, 2, 3]
violations_to_detect = [
    (  ham[1], {"eggs": 2}),
    (ham[  1], {  "eggs": 2}),
    (ham[1], {  "eggs": 2}),
    (  ham[  1  ], {  "eggs": 2}  ),
    ]

detector = ViolationDetector                     (   violations_to_detect    )
detector.process_violations()
value = add_10  (    10)
print	(value,	10) # \t # whitespace_around_comma
human = Person("Ian", 23   )


#TODO
# missing_whitespace_around_operator, !!
# whitespace_around_comma
# whitespace_before_inline_comment
# compound_statements ??
# maximum_line_length !!!!!!