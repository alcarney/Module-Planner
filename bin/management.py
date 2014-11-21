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
import ConfigParser
import json
import yaml

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

            # Now get the folders containing the module data - same with this one
            modules = settings.get("data", "modules").replace('\"', '')

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
    Function to get the file paths where module data is located
    """
    def getModulePaths(self):
        return self.settings['module_paths']

config = PlannerSettings('settings.conf')
print config.getModulePaths()

