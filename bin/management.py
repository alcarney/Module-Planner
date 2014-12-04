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
import yaml                             # For parsing yaml

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
            courses = settings.get("data", "courses_folder").replace('\"', '')

            # We will store all the courses in a list
            self.settings['course_paths'] = list()

            # They should be in a comma seperated list, so split by commas and loop through
            for c in courses.split(','):
                self.settings['course_paths'].append(root + c + '/')

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
    def getCoursePaths(self):
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
        self.loadCourseData()
        self.loadModuleData()

    """
    Function to load the Course Data from file, as specified by the settings.conf file
    """
    def loadCourseData(self):

        # We will store each course dict in a list
        self.courses = list()

        # Loop for each path that conatins a course definition
        for path in self.settings.getCoursePaths():

            # Now loop though each .md file
            for md_file in glob.glob(path + "*.md"):

                # Open the file and load the data
                with open(md_file, "r") as md:

                    # Extract the yaml data between the '---' tags
                    try:
                        yaml_data = md.read().split('---')[1]
                        self.courses.append(yaml.load(yaml_data))
                    except:
                        print "[loadCourseData]: ERROR: %s does not match expected format and will be ignored" % md_file


    """
    Loads the module data
    """
    def loadModuleData(self):

        # Store each module dictionary in a list
        self.modules = list()

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
                        self.modules.append(yaml.load(yaml_data))
                    except:
                        print "[loadModuleData]: ERROR: %s does not match expected format and will be ignored" % md_file

    def getCourses(self):
        return self.courses

    def getModules(self):
        return self.modules


    """
    Function that will check to see if a module is in a course
    """
    def inCourse(self, module):

        # Loop through all the courses
        for c in self.getCourses():

            # Check to see if it is part of a course
            if module['code'] in c['modules']:
                return True

        # Else it's not in a course and return false
        return False


    """
    Function to validate module data
    """
    def validateModuleData(self):

        # Get the modules we have loaded from the site
        modules = self.getModules()
        print modules[0]

        # Loop through each module
        for m in modules:

            # Check to see if the given module actually belongs to a course, if not skip it
            if not self.inCourse(m):
                print "[validateModuleData]: ERROR: Module %s does not belong to any defined course and will be ignored" % m['code']
                continue

            # 


# }}}

config = PlannerSettings('settings.conf')
data_manager = DataManager(config)
#print config.getModulePaths()
#print config.getCoursePaths()
print data_manager.getCourses()
data_manager.validateModuleData()

#data_manager.validateModuleData()

