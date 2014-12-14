"""
A script to check the that a particular module has been written in the correct format s given by the `data_specification.yml` file.

Usage: check_specifications.py module <modulefile> specification <specificationfile>

Options:
    -h --help    show this
"""
from yaml import load  # To read in the specification file
from docopt import docopt  # To create a command line argument library through documentation
from re import search

def read_specifications(specification_file):
    """
    Function to read in specification file

        >>> read_specifications('data_specification.yml')
        {'code': 'MA[0-9]{4}', 'layout': 'module', 'prequesites': "\\\\[('MA[0-9]{4}',+(,'MA[0-9]{4}')*)|'None'\\\\]", 'categories': 'firstyear|secondyear|thirdyear'}

    """
    specification_file = open(specification_file, 'r')
    specifications = load(specification_file)
    specification_file.close()
    return specifications

def read_module(module_file):
    """
    Function to read in module file.

        >>> read_module('./files_for_tests/module_data_file_test.md')
        {'code': 'MA0111', 'layout': 'module', 'title': 'Elementary Number Theory I', 'url': 'http://www.cardiff.ac.uk/maths/degreeprogrammes/modules/ma0111.html', 'prequesites': ['None'], 'categories': 'module firstyear'}

    """
    module_file = open(module_file, 'r')
    raw_string = module_file.read()
    module_specs = load(raw_string.split('---')[1])
    module_file.close()
    return module_specs

def check_module_obeys_specifications(module_file, specifications_file):
    """
    Check that a module obeys the regex of the specifications file

        >>> check_module_obeys_specifications('./files_for_tests/module_data_file_test.md', 'data_specification.yml')
        True

    Check that doesn't work if incorrect layout is in file (corresponding file has layout 'nonsense'):

        >>> check_module_obeys_specifications('./files_for_tests/wrong_layout_module_data_file_test.md', 'data_specification.yml')
        Traceback (most recent call last):
           ...
        ValueError: Variable 'layout' in './files_for_tests/wrong_layout_module_data_file_test.md' does not match specification

    Check that doesn't work if incorrect code is in file (corresponding file has code 'CS011'):

        >>> check_module_obeys_specifications('./files_for_tests/wrong_code_module_data_file_test.md', 'data_specification.yml')
        Traceback (most recent call last):
           ...
        ValueError: Variable 'code' in './files_for_tests/wrong_code_module_data_file_test.md' does not match specification



        >>> check_module_obeys_specifications('./files_for_tests/wrong_code_module_data_file_test.md', 'data_specification.yml')
        Traceback (most recent call last):
           ...
        ValueError: Variable 'code' in './files_for_tests/wrong_code_module_data_file_test.md' does not match specification

    Check that doesn't work if incorrect category is in file (corresponding file has category 'MSc'):

        >>> check_module_obeys_specifications('./files_for_tests/wrong_category_module_data_file_test.md', 'data_specification.yml')
        Traceback (most recent call last):
           ...
        ValueError: Variable 'categories' in './files_for_tests/wrong_category_module_data_file_test.md' does not match specification

    Check that works if correct prerequesites is in file

        >>> check_module_obeys_specifications('./files_for_tests/correct_prequesites_module_data_file_test.md', 'data_specification.yml')
        True

    Check that works if incorrect prerequesites is in file (corresponding file has one prequesites as 'Ice Cream'

        >>> check_module_obeys_specifications('./files_for_tests/incorrect_prequesites_module_data_file_test.md', 'data_specification.yml')
        Traceback (most recent call last):
           ...
        ValueError: Variable 'prequesites' in './files_for_tests/incorrect_prequesites_module_data_file_test.md' does not match specification

    """
    module_specs = read_module(module_file)
    specifications = read_specifications(specifications_file)
    for variable in specifications:
        if not bool(search(specifications[variable], str(module_specs[variable]))):
            raise ValueError("Variable '%s' in '%s' does not match specification" % (variable, module_file))
    return True


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments
