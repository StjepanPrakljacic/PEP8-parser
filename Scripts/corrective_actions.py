# PyCode Style Corrective module

#Description: A Python module designed to automatically correct style
#             violations in Python code files.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git

# Version: 1.0.0
###############################################################################

import inspect
import re
from .logging_handler import log_obj

#############################################################
#                     Helping functions                     #
#############################################################


def get_info_format(value):
    """
    Format and log information about the running function.

    Args:
        value(str): The name of the function.

    Returns:
        None
    """
    value = value.split('_')
    info = ' '.join([value[0].capitalize()] + value[1:])
    log_obj.info(f"Running: {info}")


def write_to_file(path, content):
    """
    Write the modified content back to the file.

    Args:
        path(str): The path to the file.
        content(list): The modified content as a list of strings.

    Returns:
        None
    """
    with open(path, "w") as f:
        f.writelines(content)


def remove_whitespace_and_count(s, start_index):
    """
    Remove consecutive whitespaces from a string starting from the given index.

    Args:
        s(str): The input string.
        start_index(int): The starting index for whitespace removal.

    Returns:
        tuple: A tuple containing the modified line with removed whitespaces
               and the count of deleted whitespaces.
    """
    count = 0
    end_index = start_index
    while end_index < len(s) and s[end_index].isspace():
        count += 1
        end_index += 1

    modified_line = (
        s[:start_index]
        + s[start_index:end_index].replace(" ", "")
        + s[end_index:])

    return modified_line, count


def insert_whitespace(line, position):
    """
    Insert whitespace at the specified position in the given line.

    Args:
        line(str): The line of code.
        position(int): The position where whitespace needs to be inserted.

    Returns:
        str: The line with whitespace inserted at the specified position.
    """
    return line[:position] + ' ' + line[position:]


#############################################################
#               Violations corrective section               #
#############################################################


def tabs_corrective_action(path, content, violations):
    """
    Correct tab violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of tab violations, where each violation is
                          represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1] = (lines[line_number - 1][:column] \
                                  + ' ' * 4 \
                                  + lines[line_number - 1][column + 1:])
        write_to_file(path, lines)
        prev_line_number = line_number


def extraneous_whitespace_corrective_action(path, content, violations):
    """
    Correct extraneous whitespace violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of extraneous whitespace violations, where
                          each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1], _ = remove_whitespace_and_count(
            lines[line_number - 1], \
            column)
        write_to_file(path, lines)
        prev_line_number = line_number


def missing_whitespace_corrective_action(path, content, violations):
    """
    Correct missing whitespace violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of missing whitespace violations, where
                          each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1] = insert_whitespace(
            lines[line_number - 1], \
            column + 1)
        write_to_file(path, lines)
        prev_line_number = line_number


def whitespace_before_parameters_corrective_action(path, content, violations):
    """
    Correct whitespace before parameters violations in the given file content.

    Args:
        path (str):The path to the file being corrected.
        content (list):The content of the file.
        violations(list): A list of missing whitespace violations, where
                          each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    for violation in violations:
        line_number = violation["line_number"]
        function = violation["for_function"]
        column = violation["column"]
        index = column + len(function)
        lines[line_number - 1], count = remove_whitespace_and_count(
            lines[line_number - 1], \
            index - 1)
        write_to_file(path, lines)


def whitespace_around_operator_corrective_action(path, content, violations):
    """
    Correct whitespace around operators violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of whitespace around operators violations,
                          where each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1], _ = remove_whitespace_and_count(
            lines[line_number - 1], \
            column + 1)
        write_to_file(path, lines)
        prev_line_number = line_number


def missing_whitespace_around_operator_corrective_action(path, 
                                                         content,
                                                         violations):
    """
    Correct whitespace around operators violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of whitespace around operators violations,
                          where each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1] = insert_whitespace(
            lines[line_number - 1], \
            column + 1)
        write_to_file(path, lines)
        prev_line_number = line_number


def whitespace_after_comma_corrective_action(path, content, violations):
    """
    Correct whitespace after comma violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of whitespace around operators violations,
                          where each violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        lines[line_number - 1], _ = remove_whitespace_and_count(
            lines[line_number - 1], \
            column + 1)
        write_to_file(path, lines)
        prev_line_number = line_number


def trailing_whitespace_corrective_action(path, content, violations):
    """
    Correct trailing whitespace violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of trailing whitespace violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()

    for violation in violations:
        line_number = violation["line_number"]
        violation_type = int(violation["violation_type"])
        column = int(violation["column"])
        if violation_type == 291:
            lines[line_number - 1], _ = remove_whitespace_and_count(
                lines[line_number - 1], \
                column)
        elif violation_type == 293:
            lines[line_number - 1] = lines[line_number - 1].strip() + '\n'
    with open(path, "w") as f:
        f.writelines(lines)


def imports_position_corrective_action(path, content, violations):
    """
    Correct import position violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of import position violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    stored_lines = list()
    lines_to_remove = list()

    for violation in violations:
        line_number = violation["line_number"]
        lines_to_remove.append(line_number)
        stored_lines.append(lines[line_number - 1].strip())

    remove = set(lines_to_remove)
    lines = [line for i, line in enumerate(lines, start=1) if i not in remove]

    for i, line in enumerate(stored_lines):
        lines.insert(i, line + '\n')

    write_to_file(path, lines)


def multiple_imports_corrective_action(path, content, violations):
    """
    Correct multiple imports violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of multiple imports violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    offset = 0

    for violation in violations:
        line_number = violation["line_number"] + offset
        import_line = lines[line_number - 1]
        indentation = import_line.split("import")[0]

        imports = [f"{indentation}import {module.strip()}" for module in \
                   import_line.replace("import ", '').split(',')]
        lines[line_number - 1] = imports[0] + '\n'
        for new_line in imports[1:]:
            line_number += 1
            lines.insert(line_number - 1, new_line + '\n')
            offset += 1

    write_to_file(path, lines)


def blank_lines_corrective_action(path, content, violations):
    """
    Correct blank line violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of blank line violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    offset = 0

    for violation in violations:
        line_number = violation["line_number"] + offset
        expected_blank_lines = int(violation["expected"])
        received_blank_lines = int(violation["received"])

        blank_lines_diff = expected_blank_lines - received_blank_lines
        offset += blank_lines_diff

        if blank_lines_diff > 0:
            while blank_lines_diff:
                lines.insert(line_number - 1, '\n')
                line_number += 1
                blank_lines_diff -= 1
        elif blank_lines_diff < 0:
            while blank_lines_diff:
                del lines[line_number - 2]
                line_number -= 1
                blank_lines_diff += 1

    write_to_file(path, lines)


def whitespace_before_inline_comment_corrective_action(path, \
                                                       content, \
                                                       violations):
    """
    Correct whitespaces before inline comment violations in the given file
    content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of blank line violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    prev_line_number = None
    for violation in violations:
        line_number = violation["line_number"]
        violation_type = violation["violation_type"]
        column = violation["column"]
        if prev_line_number == line_number:
            continue
        if violation_type == 262:
            lines[line_number - 1] = re.sub(r"#+\s*", \
                                            r"# ", \
                                            lines[line_number - 1])
            write_to_file(path, lines)
        if violation_type == 261:
            lines[line_number - 1] = insert_whitespace(
                lines[line_number - 1], \
                column)
            write_to_file(path, lines)
        prev_line_number == line_number


def missing_newline_corrective_action(path, content, violations):
    """
    Correct missing newline violations in the given file content.

    Args:
        path(str): The path to the file being corrected.
        content(list): The content of the file.
        violations(list): A list of missing newline violations, where each
                          violation is represented as a dictionary.

    Returns:
        None
    """
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = content.copy()
    lines.append('\n')
    write_to_file(path, lines)
