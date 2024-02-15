# PyCode Style Checker

# Description: A Python module designed to automatically check code files for
#              style violations.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git

# Version: 1.0.0
###############################################################################

import re
import ast

patterns = {
    "imports_position": {
        "value": "",
        "violation_type": "E400",
        "key": "Import positioning",
        "expected": None,
        "received": None
        },
    "multiple_imports": {
        "value": "^\\s*import\\s+[^#]*,[^#]*$",
        "violation_type": "E401",
        "key": "Multiple imports on one line",
        "expected": None,
        "received": None
        },
    "expected_blank_lines": {
        "value": "",
        "violation_type": "E302",
        "key": "Blank lines positioning",
        "expected": "{expected}",
        "received": "{received}"
        },
    "extraneous_whitespace": {
        "value": "[[({] | []}),;:]",
        "violation_type": ["E201", "E202", "E203"],
        "key": ["whitespace after {}", "whitespace before {}"],
        "expected": None,
        "received": None
        }
}

#############################################################
#                     Helping functions                     #
#############################################################


def parse_pattern(pattern):
    return (re.compile(pattern.get("value"), re.MULTILINE),
            pattern.get("violation_type"),
            pattern.get("key"),
            pattern.get("expected"),
            pattern.get("received"),)


def calculate_blank_lines(file_content, line_number, expected_blank_lines):
    _, violation_type, key, exp, rec = parse_pattern(
        patterns["expected_blank_lines"]
        )
    blank_lines_count = 0
    current_line = line_number - 2

    # Count blank lines until a non-blank line is encountered
    while current_line >= 0 and not file_content[current_line].strip():
        blank_lines_count += 1
        current_line -= 1

    # Check if the calculated blank lines match the expected pattern
    if blank_lines_count != expected_blank_lines:
        return {
            "line_number": line_number,
            "violation_type": violation_type,
            "key": key,
            "expected": exp.format(expected=expected_blank_lines),
            "received": rec.format(received=blank_lines_count),
        }
    return None

#############################################################
#                 Violations check section                  #
#############################################################


def imports_position_check(file_content):
    """
    Check import position violations in the given file content.

    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    _, violation_type, key, _, _ = parse_pattern(
        patterns["imports_position"]
        )
    violations = list()
    imports_outside_functions_classes = list()
    imports_inside_functions_classes = list()
    file_content = "".join(file_content)
    tree = ast.parse(file_content)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports_outside_functions_classes.append(
                {"node": node,"line_number": node.lineno}
                )

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            for inner_node in ast.walk(node):
                if isinstance(inner_node, (ast.Import, ast.ImportFrom)):
                    imports_inside_functions_classes.append(
                        {"node": inner_node, "line_number": inner_node.lineno}
                        )

    for node in imports_outside_functions_classes:
        if node not in imports_inside_functions_classes:
            violations.append({"line_number": node["line_number"],
                               "violation_type": violation_type,
                               "key": key})

    line_numbers = [v.get("line_number") for v in violations]
    if line_numbers == list(range(min(line_numbers), max(line_numbers) + 1)):
        return None
    return violations


def multiple_imports_check(file_content):
    """
    Check multiple imports violations in the given file content.

    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern, violation_type, key, _, _ = parse_pattern(
        patterns["multiple_imports"]
        )
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        match = re.match(pattern, line)
        if match:
            violations.append({"line_number": line_number,
                               "violation_type": violation_type,
                               "key": key})

    return violations if violations else None


def expected_blank_lines_check(file_content):
    """
    Check expected blank lines violations in the given file content.

    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    content = "".join(file_content)
    tree = ast.parse(content)
    classes_and_functions = list()
    methods = list()
    violations = list()
    current_class = None

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if current_class is None:
                classes_and_functions.append(node.lineno)
            elif isinstance(node, ast.FunctionDef):
                methods.append(node.lineno)

        elif isinstance(node, ast.ClassDef):
            current_class = node
            classes_and_functions.append(node.lineno)
            for inner_node in node.body:
                if isinstance(inner_node, ast.FunctionDef):
                    methods.append(inner_node.lineno)
            current_class = None

    for line in classes_and_functions:
        violation = calculate_blank_lines(file_content, line, 2)
        if violation:
            violations.append(violation)

    for line in methods:
        violation = calculate_blank_lines(file_content, line, 1)
        if violation:
            violations.append(violation)

    output = sorted(violations, key=lambda x: x["line_number"]) \
        if violations else None
    return output


def extraneous_whitespace_check(file_content):
    """
    Check for extraneous whitespace in the given file content.

    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern, violation_types, keys, _, _ = parse_pattern(
        patterns["extraneous_whitespace"]
    )
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        for match in pattern.finditer(line):
            whitespace_group = match.group()
            whitespace_char = whitespace_group.strip()
            whitespace_position = match.start()

            if whitespace_group == whitespace_char + ' ' and \
                    whitespace_char in '([{':
                violations.append({
                    "line_number": line_number,
                    "violation_type": violation_types[0],
                    "key": keys[0].format(whitespace_char),
                    "at_position": whitespace_position + 1
                })
            if whitespace_group == ' ' + whitespace_char and \
                    line[whitespace_position - 1] != ',':
                if whitespace_char in '}])':
                    violations.append({
                        "line_number": line_number,
                        "violation_type": violation_types[1],
                        "key": keys[1].format(whitespace_char),
                        "at_position": whitespace_position
                    })
                if whitespace_char in ',;:':
                    violations.append({
                        "line_number": line_number,
                        "violation_type": violation_types[2],
                        "key": keys[1].format(whitespace_char),
                        "at_position": whitespace_position
                    })

    return violations if violations else None







