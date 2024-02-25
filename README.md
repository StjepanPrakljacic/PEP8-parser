# PEP8-parser
The PEP 8 Parser is a Python tool designed to automatically enforce and apply the PEP 8 style guide to a collection of Python files within a specified folder. PEP 8 is the official style guide for Python code, providing conventions for writing clean, readable, and consistent code.
## Features 
- **Automatic Styling:** The parser scans through Python files in the specified folder and automatically formats them according to PEP 8 standards.

- **Non-Destructive:** The tool applies changes in a non-destructive manner, preserving the original code while creating styled versions of the files.

- **Customization:** Users have the flexibility to configure certain aspects of the styling process, adapting it to their specific project requirements.
## Usage
1. **Clone the repository to your local machine**
2. **Install the necessary dependencies (if any) using the provided instructions:**
   ```bash
     pip install -r requirements.txt
   ```
3. **Run the PEP 8 parser on a target folder:**
```bash
python program.py
```
4. **The tool will process all .py files in the specified folder, ensuring adherence to the PEP 8 style guide.**
## Known Limitations
1. **FutureWarning in PEP8-parser:
When using the PEP8-parser module, a FutureWarning may be encountered with the message "Possible nested set at position 1." This warning is related to the use of regular expressions and is a known issue. While it does not affect the functionality of the code, users may encounter this warning. This issue is on our radar, and we are actively working to address it in future releases.

2. **Indentation Functions:
The functions indentation_check() and indentation_corrective_action() are currently not implemented and tested. These features are planned for inclusion in the next release. Users are advised to be cautious when relying on these functions in the current version.

3. **Max Line Length Functions:
The functions max_line_length_check() and max_line_length_corrective_action() are not yet implemented and tested. These features are scheduled for inclusion in the upcoming release. Users should be aware that the current version lacks these functionalities, and they are encouraged to check for updates in subsequent releases.

4. **Code Structure:
The parser does not automatically separate imports into their own new lines. For example, writing import os, sys # Comment on a single line is syntactically correct but may lead to readability issues. It's not a recommended coding practice, and future versions of the code may address this limitation by providing a more structured and readable format.
## Testing
The code has undergone testing using scripts located in the "Test" folder. We have ensured comprehensive test coverage to validate the functionality and reliability of the software. Users are encouraged to explore and run the provided test scripts to verify the behavior of the code in different scenarios. If you encounter any issues during testing or have additional test cases you'd like us to consider, please let us know through our support channels.

We appreciate your cooperation and feedback as we strive to deliver a robust and reliable solution.
## Contributing
Contributions are welcome! If you find issues, have suggestions, or want to enhance the PEP 8 parser, feel free to submit pull requests.
## License
This project is licensed under the [MIT License](LICENSE).
## Contact
