# PyCode Style Corrective module

#Description: A Python module designed to automatically correct style
#             violations in Python code files.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git

# Version: 1.0.0
###############################################################################

import inspect
from .logging_handler import log_obj

#############################################################
#                     Helping functions                     #
#############################################################


def get_info_format(value):
    value = value.split('_')
    info = ' '.join([value[0].capitalize()] + value[1:])
    log_obj.info(f"Running: {info}")


def write_to_file(file_path, file_content):
     with open(file_path, 'w') as f:
        f.writelines(file_content)

#############################################################
#               Violations corrective section               #
#############################################################


def imports_position_corrective_action(file_path, file_content, violations):
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = file_content.copy()
    stored_lines = list()
    lines_to_remove = list()

    for violation in violations:
        line_number = violation['line_number']
        lines_to_remove.append(line_number)
        stored_lines.append(lines[line_number - 1].strip())

    remove = set(lines_to_remove)
    lines = [line for i, line in enumerate(lines, start=1) if i not in remove]

    for i, line in enumerate(stored_lines):
        lines.insert(i, line + '\n')

    write_to_file(file_path, lines)


def multiple_imports_corrective_action(file_path, file_content, violations):
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = file_content.copy()
    offset = 0

    for violation in violations:
        line_number = violation['line_number'] + offset
        import_line = lines[line_number - 1]
        indentation = import_line.split('import')[0]

        imports = [f"{indentation}import {module.strip()}" for module in
                   import_line.replace('import ', '').split(',')]
        lines[line_number - 1] = imports[0] + '\n'
        for new_line in imports[1:]:
            line_number += 1
            lines.insert(line_number - 1, new_line + '\n')
            offset += 1

    write_to_file(file_path, lines)


def blank_lines_corrective_action(file_path, file_content, violations):
    get_info_format(inspect.currentframe().f_code.co_name)
    lines = file_content.copy()
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

    write_to_file(file_path, lines)
