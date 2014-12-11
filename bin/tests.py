#!/usr/bin/python2

import management
import unittest

class TestDataManager(unittest.TestCase):

    def test_using_defaults(self):

        #The Planner object should still be created but switch to defaults, if there are none no settings will be set
        self.assertRaises(management.NoSettings, management.PlannerSettings, '')

    def test_reading_course_paths(self):

        #Creates an planner settings object using settings.conf
        self.test_object = management.PlannerSettings('settings.conf')

        #Checks that the DataManager Object finds the correct paths for the modules
        expected_paths = ['../FirstYear/','../SecondYear/','../ThirdYear/']

        for path in expected_paths:
            self.assertTrue(path in self.test_object.settings['module_paths'])

        #Checks that the DataManager Object finds the correct paths for the courses
        expected_paths = ['../Courses/']
        for path in expected_paths:
            self.assertTrue(path in self.test_object.settings['course_paths'])

if __name__ == '__main__':
    unittest.main()
