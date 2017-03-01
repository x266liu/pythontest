'''
Created on Aug 28, 2014

@author: maqeel
'''
from __future__ import print_function
import sys, string, os

class testResultClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # Variables for Test Summary report
        self.totalNumberOfTC = 0
        self.TotalNumberOfPassTC = 0
        self.TotalNumberOfFailTC = 0
        testReportPath = os.path.join('..','TestReport')

        self.Test_Result_File_Name = os.path.join(testReportPath, 'test_Results.csv')

    
    def openTestFile(self):
        self.testResults = open(self.Test_Result_File_Name, 'a')        # Opening Test Result file to write result of test case 1 

    def writeInTestFile(self, string):
        self.testResults.write(string)
        #print(string, self.Test_Result_File_Name)
        
    def OpenFileAndSetFilePointerAtBeginning(self):
        # Again set the pointer to the beginning
        self.testResults = open(self.Test_Result_File_Name, 'a')        # Opening Test Result file to write result of test case 1 
        self.testResults.seek(0, 0)

      #  print "Read Line: %s" % (line)
        
    def closeTestFile(self):
        self.testResults.close()

testResultObject = testResultClass()
