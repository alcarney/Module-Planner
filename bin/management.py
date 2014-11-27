#!/usr/bin/python2

"""
This file provides various utilities for mamnaging the module planner.
Current features include:

    => Data Management

        - Verification: Given a specification of what should define
        a module, course etc. This will check whether or not any
        records are not compliant with this specification

        - Conversion: While Jeckyll uses YAML to store its data for the
        module info pages, the module planner will work best with
        JSON so this provides tools for converting it

        - Compilation: The data is spread out accross all the pages of the
        site however ideally we want to be downloading as few files as
        possible over the web so this compiles all the data into a single
        JSON file
"""

# Import the tools we need
import ConfigParser                     # For parsing settings.conf
import glob                             # For looping through files in a directory
import json                             # For exporting json data

# {{{ Planner Settings
class PlannerSettings():

    """
    Constructor for the settings class, takes a single argument:
        - config_file: The filepath to the configuration file
    """
    def __init__(self, config_file):

            # Create an empty dict to store our settings later once they've been organised
            self.settings = dict()

            # We want to pack up the settings into a more useful structure for
            # code later on
            settings = ConfigParser.ConfigParser()
            files_parsed = settings.read(config_file)

            # Check to see if the file was loaded correctly, if not then an empty
            # list is returned
            if files_parsed == []:

                # If we can't load the file try and use defaults instead
                print "[PlannerSettings]: WARN: Unable to load settings.conf, trying to continue with defaults"
                self.useDefaults()

                return

            # Get the root of the site - this comes with quotes so let's get rid of those while we're at it
            root = settings.get("core", "site_root").replace('\"', '')

            # Get the folder(s) containing the course data - same here also
            courses = settings.get("data", "course_folder").replace('\"', '')

            

            # They should be in a comma seperated list, so split by commas and loop through
            for c in courses.split(','):


            # Now get the folder(s) containing the module data - same with this one
            modules = settings.get("data", "module_folder").replace('\"', '')

            # We will store the filepaths for the data in a list
            self.settings['module_paths'] = list()

            # They should be in a comma seperated list so split by commas and loop through
            for m in modules.split(','):

                # Concatenate the 'root' and 'module names'
                self.settings['module_paths'].append(root + m + '/')

    """
    This function is only run if we cannot load the settings file and attempts
    to provide a set of sane defaults
    """
    def useDefaults(self):
        pass

    """
    Function to get the file path(s) where course data is located
    """
    return self.settings['course_paths']

    """
    Function to get the file path(s) where module data is located
    """
    def getModulePaths(self):
        return self.settings['module_paths']

# }}}

# {{{ Data Manager
class DataManager():

    """
    Init function for the DataManager class, the only argument is a
    PlannerSettings object so this can discover the appropriate file
    paths etc.
    """
    def __init__(self, settings):
        self.settings = settings

    """
    Function that will parse the yaml data since the yaml library
    works in a bizarre way and it's not too hard to do it manually
    """
    def parseYaml(self, yaml):

        # Create an empty dictionary to store the values in
        parsed_data = dict()

        # Each yaml entry is on a single line so split by new lines
        for line in yaml.split("\n"):

            # The yaml string seems to come with extra guff so only do the following on lines that contain
            # the ':' seperator
            if ':' in line:

                # Split the line according to the seperator, since URLs also contain ':' we will
                # split only by the first occurance
                linesplit = line.split(':', 1)

                # The first segment will be the dictionary key
                key = linesplit[0].rstrip()         # Remove trailing whitespace

                # The value is a bit more complicated so, first let's strip the leading spaces
                value = linesplit[1].lstrip()       # Remove leading whitespace

                # There are cases where we need to build a list
                if '[' in value:
                    value = eval(value)

                # Add the values to the dictionary
                parsed_data[key] = value

        # Return the dictionary
        return parsed_data

    """
    Function to load the Course Data from file, as specified by the settings.conf file
    """
    def loadCourseData(self):



    """
    This function loops through all the .md files in the directories
    specified by PlannerSettings.getModulePaths(), parses the yaml and
    makes sure it conforms to the specification
    """
    def validateModuleData(self):

        # First things first loop through the module paths
        for path in self.settings.getModulePaths():

            # Now for each path loop through all the markdown files
            for md_file in glob.glob(path + "*.md"):

                # Open the markdown file
                with open(md_file, 'r') as md:

                    # Since the yaml data that we are interested in is inbetween two '---' tags
                    # let's split the string by that as we read the file
                    try:
                        yaml_data = md.read().split('---')[1]
                        print self.parseYaml(yaml_data)
                    except:
                        print "[validateModuleData]: ERROR: %s does not match expected format and will be ignored" % md_file

# }}}

config = PlannerSettings('settings.conf')
data_manager = DataManager(config)
print config.getModulePaths()
data_manager.validateModuleData()

