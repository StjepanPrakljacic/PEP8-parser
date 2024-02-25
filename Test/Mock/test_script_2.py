#### This is a test_script_2.py
def multiply_by_5(        value      ):
    return value        * 5

import os
import sys
from datetime import datetime
class Book:
    import time
    def __init__(self   , title,    author="Unknown"):
        self.title    =       title
        self.author                       = author

    def get_info(self):
        return f"{     self.title} by {self.author}"

import json

class Vehicle:
    def __init__(self,    make,  model    , year=        2022        ):
        pass
# New class for detecting violations
class ViolationChecker:
    def __init__(self, violations):
        self.violations = violations
    def check_violations(self):
        for violation in self.violations:
            print("Violation found:", violation)
def calculate_square(x   ):
    return x     *    2

# Intentional violations for testing detection
numbers = [1,  2,     3]
violations_to_check = [
    (numbers[1  ], {  "apple": 2}),
    (  numbers[1], {"apple": 2   }),
    (                    numbers[  1 ], {   "apple": 2}             ),
    (numbers[    1   ], {"apple": 2}),
]

checker = ViolationChecker(violations_to_check)
checker.check_violations()
result = multiply_by_5(4    )
print(result, 4)
book = Book(    "The Great Gatsby", "F. Scott Fitzgerald")
print(book.get_info())
current_time = datetime.now()
print("Current time:", current_time)
