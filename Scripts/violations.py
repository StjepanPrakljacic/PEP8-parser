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
import tokenize
from io import BytesIO
import keyword

patterns = {
    "inline_comment": {
        "value": "^\s*#",
        "violation_type": 101,
        "key": "Line contains mixed spaces and tabs",
        },
    "imports_position": {
        "value": "",
        "violation_type": 400,
        "key": "Import positioning",
        },
    "multiple_imports": {
        "value": "^\\s*import\\s+[^#]*,[^#]*$",
        "violation_type": 401,
        "key": "Multiple imports on one line",
        },
    "expected_blank_lines": {
        "value": "",
        "violation_type": 302,
        "key": "Blank lines positioning",
        "expected": "{expected}",
        "received": "{received}"
        },
    "extraneous_whitespace": {
        "value": "[[({] | []}),;:]",
        "violation_type": [201, 202, 203],
        "key": ["Whitespace after '{}'", "Whitespace before '{}'"],
        },
    "missing_whitespace": {
        "value": "",
        "violation_type": 231,
        "key": "Missing whitespace after '{}'",
        },
    "whitespace_before_param": {
        "value": "(\w+)\s+\(",
        "violation_type": 211,
        "key": "Whitespace before parametars",
        },
    "whitespace_around_operator": {
        "value": "",
        "violation_type": [221, 222],
        "key": ["Multiple spaces before operator",
                "Multiple spaces after operator"],
        },
    "missing_newline": {
        "value": "",
        "violation_type": 292,
        "key": "No newline at end of file",
        },
    "trailing_whitespace": {
        "value": "",
        "violation_type": [291, 293],
        "key": ["Trailing whitespace", "Blank line contains whitespace"],
        },
}

BINARY_OPERATORS = frozenset(['**=', '*=', '+=', '-=', '!=', '<>', '%=', '^=',
                              '&=', '|=', '==', '/=', '//=', '<=', '>=', '<<=',
                              '>>=', '%',  '^',  '&',  '|',  '=',  '/',  '//',
                              '<',  '>',  '<<'])
UNARY_OPERATORS = frozenset(['>>', '**', '*', '+', '-'])
OPERATORS = BINARY_OPERATORS | UNARY_OPERATORS

#############################################################
#                     Helping functions                     #
#############################################################


def parse_pattern(pattern):
    """
    Parse the pattern dictionary and extract relevant information.

    Args:
        pattern (dict): A dictionary containing pattern information.

    Returns:
        tuple: A tuple containing the compiled pattern, violation type, and
               key and (expected' / 'received') if present.
    """

    compiled_pattern = re.compile(pattern.get("value"), re.MULTILINE)
    violation_type = pattern.get("violation_type")
    key = pattern.get("key")

    expected = pattern.get("expected", None)
    received = pattern.get("received", None)

    if expected is not None and received is not None:
        return compiled_pattern, violation_type, key, expected, received
    else:
        return compiled_pattern, violation_type, key


def calculate_blank_lines(file_content, line_number, expected_blank_lines):
    """
    Calculate and verify the number of blank lines above a specified line.

    Args:
        file_content (list): List of strings representing the content of the
                             file.
        line_number (int): The line number to check for blank lines.
        expected_blank_lines (int): The expected number of blank lines.

    Returns:
        dict or None: If the calculated blank lines differ from the expected
                      value, a dictionary representing the violation is
                      returned. Otherwise, None is returned.
    """
    pattern = parse_pattern(patterns["expected_blank_lines"])
    blank_lines_count = 0
    current_line = line_number - 2

    # Count blank lines until a non-blank line is encountered
    while current_line >= 0 and not file_content[current_line].strip():
        blank_lines_count += 1
        current_line -= 1

    if blank_lines_count != expected_blank_lines:
        return {
            "line_number": line_number,
            "violation_type": pattern[1],
            "key": pattern[2],
            "expected": pattern[3].format(expected=expected_blank_lines),
            "received": pattern[4].format(received=blank_lines_count),
        }
    return None

#############################################################
#                 Violations check section                  #
#############################################################


def tabs_check(file_content):
    """
    Check for tabs in the given file content.

    Args:
        file_content (list): List of strings representing the content of the
                             file.

    Returns:
        list: A list containing violations, where each violation is a
              dictionary.
    """
    pattern = parse_pattern(patterns["inline_comment"])
    violations = list()
    in_multiline_comment = False

    for line_number, line in enumerate(file_content, start=1):
        if '"""' in line or "'''" in line:
            in_multiline_comment = not in_multiline_comment
            continue

        if in_multiline_comment:
            continue

        if re.match(pattern[0], line):
            continue

        tab_indices = [match.start() for match in re.finditer(r'\t', line)]

        for column in tab_indices:
            violations.append({
                "line_number": line_number,
                "violation_type": pattern[1],
                "key": pattern[2],
                "column": column
            })

    return violations if violations else None


def extraneous_whitespace_check(file_content):
    """
    Check for extraneous whitespace in the given file content.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
              dictionary.
    """
    pattern = parse_pattern(patterns["extraneous_whitespace"])
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        for match in pattern[0].finditer(line):
            whitespace_group = match.group()
            whitespace_char = whitespace_group.strip()
            whitespace_position = match.start()

            if (whitespace_group == whitespace_char \
                + ' ' and \
                whitespace_char in '([{'):
                violations.append({
                    "line_number": line_number,
                    "violation_type": pattern[1][0],
                    "key": pattern[2][0].format(whitespace_char),
                    "column": whitespace_position + 1
                })

            if (whitespace_group == ' ' \
                + whitespace_char and \
                line[whitespace_position - 1] != ','):

                next_non_whitespace_index = whitespace_position
                while (next_non_whitespace_index >= 0 and
                       line[next_non_whitespace_index].isspace()):
                    next_non_whitespace_index -= 1

                if whitespace_char in '}])':
                    violations.append({
                        "line_number": line_number,
                        "violation_type": pattern[1][1],
                        "key": pattern[2][1].format(whitespace_char),
                        "column": next_non_whitespace_index + 1
                    })
                if whitespace_char in ',;:':
                    violations.append({
                        "line_number": line_number,
                        "violation_type": pattern[1][2],
                        "key": pattern[2][1].format(whitespace_char),
                        "column": next_non_whitespace_index + 1
                    })

    return violations if violations else None


def missing_whitespace_check(file_content):
    """
    Check for missing whitespace in the given file content.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern = parse_pattern(patterns["missing_whitespace"])
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        for index in range(len(line) - 1):
            character = line[index]
            if character in ',;:' and line[index + 1] not in ' \t':
                line_before = line[:index]
                if (character == ':' and
                    line_before.count('[') > line_before.count(']')):
                    continue
                if character == ',' and line[index + 1] == ')':
                    continue
                violations.append({
                            "line_number": line_number,
                            "violation_type": pattern[1],
                            "key": pattern[2].format(character),
                            "column": index
                        })
    return violations if violations else None


def whitespace_before_parameters_check(file_content):
    """
    Check for whitespace before parameters.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern = parse_pattern(patterns["whitespace_before_param"])
    violations = list()
    for line_number, line in enumerate(file_content, start=1):
        matches = re.finditer(pattern[0], line)
        for match in matches:
            violation_column = match.start(1) + 1
            violations.append({
                "line_number": line_number,
                "violation_type": pattern[1],
                "key": pattern[2],
                "for_function": match.group(1),
                "column": violation_column
            })

    return violations if violations else None


def whitespace_around_operator_check(file_content):
    """
    Check for whitespace around operators in the given file content.

    Args:
        file_content (list): List of strings representing the content of the file.
        patterns (dict): A dictionary containing pattern information for whitespace
                         around operators.
    Returns:
        list or None: A list containing violations, where each violation is a
        dictionary. If no violations are found, returns None.
    """
    pattern = parse_pattern(patterns["whitespace_around_operator"])
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        for character in line:
            if character in OPERATORS:
                index = line.index(character)
                step_before = index - 1
                whitespace_counter = 0
                while(line[step_before].isspace()):
                    step_before -= 1
                    whitespace_counter += 1
                if whitespace_counter > 1 and step_before > 1:
                    violations.append({
                        "line_number": line_number,
                        "violation_type": pattern[1][0],
                        "key": pattern[2][0],
                        "column": step_before + 1,
                    })
                whitespace_counter = 0
                step_after = index + 1
                while(step_after < len(line.rstrip()) and
                      line[step_after].isspace()):
                    step_after += 1
                    whitespace_counter += 1
                if whitespace_counter > 1:
                    violations.append({
                        "line_number": line_number,
                        "violation_type": pattern[1][1],
                        "key": pattern[2][1],
                        "column": index + 1,
                    })

    return violations if violations else None


def trailing_whitespace_check(file_content):
    """
    Check for trailing whitespace violations in the given file content.

    Args:
        file_content (list): List of strings representing the content of the
                             file.
        patterns (dict): A dictionary containing pattern information for
                         trailing whitespace.

    Returns:
        list or None: A list containing violations, where each violation is a
        dictionary. If no violations are found, returns None.
    """
    pattern = parse_pattern(patterns["trailing_whitespace"])
    violations = list()
    for line_number, line in enumerate(file_content, start=1):
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        stripped = line.rstrip()
        if line != stripped:
            if stripped:
                violations.append({
                    "line_number": line_number,
                    "violation_type": pattern[1][0],
                    "key": pattern[2][0],
                    "column": len(stripped)
                })
            else:
                violations.append({
                    "line_number": line_number,
                    "violation_type": pattern[1][1],
                    "key": pattern[2][1],
                    "column": 0
                })

    return violations if violations else None


def imports_position_check(file_content):
    """
    Check import position violations in the given file content.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern = parse_pattern(patterns["imports_position"])
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
    verdict = list()
    for node in imports_outside_functions_classes:
        if node not in imports_inside_functions_classes:
            verdict.append(node["line_number"])

    if verdict and verdict != list(range(1, verdict[-1] + 1)):
        for line_number in verdict:
            violations.append({
                "line_number": line_number,
                "violation_type": pattern[1],
                "key": pattern[2]
            })
    return violations if violations else None


def multiple_imports_check(file_content):
    """
    Check multiple imports violations in the given file content.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    pattern = parse_pattern(patterns["multiple_imports"])
    violations = list()

    for line_number, line in enumerate(file_content, start=1):
        match = re.match(pattern[0], line)
        if match:
            violations.append({"line_number": line_number,
                               "violation_type": pattern[1],
                               "key": pattern[2]})

    return violations if violations else None


def expected_blank_lines_check(file_content):
    """
    Check expected blank lines violations in the given file content.
    Args:
        file_content (list): List of strings representing the content of the
                             file.
    Returns:
        list: A list containing violations, where each violation is a
        dictionary.
    """
    content = "".join(file_content)
    tree = ast.parse(content)
    standalone_functions_classes = list()
    methods = list()
    violations = list()
    current_class = None

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if current_class is None:
                standalone_functions_classes.append(node.lineno)
            elif isinstance(node, ast.FunctionDef):
                methods.append(node.lineno)

        elif isinstance(node, ast.ClassDef):
            current_class = node
            standalone_functions_classes.append(node.lineno)
            for inner_node in node.body:
                if isinstance(inner_node, ast.FunctionDef):
                    methods.append(inner_node.lineno)
            current_class = None

    for line in standalone_functions_classes:
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


def missing_newline_check(file_content):
    """
    Check for missing newline at the end of the file content.

    Args:
        file_content (list): List of strings representing the content of the
                             file.
        patterns (dict): A dictionary containing pattern information for
                         missing newline.
    Returns:
        list or None: A list containing violations, where each violation is a
        dictionary. If no violations are found, returns None.
    """
    pattern = parse_pattern(patterns["missing_newline"])
    violations = list()
    if not file_content[-1].endswith('\n'):
        violations.append({
            "line_number": len(file_content),
            "violation_type": pattern[1],
            "key": pattern[2],
            "column": len(file_content[-1]) + 1,
        })

    return violations if violations else None
