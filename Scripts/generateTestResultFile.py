'''
Created on Aug 28, 2014

@author: maqeel
'''
from __future__ import print_function
import sys, string, os

def equal(a, b):
    if(a == b[0]):
        return "Pass"
    else:
        return "Fail"


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
        
    def verify(self, eAD, dVL, rfpath, fp, rfn, idx, lfpath, erL, tcN, vcl, count):
        elemetnAttributeDictionary = eAD
        conditionString = elemetnAttributeDictionary.get('conditions')
        conditions = conditionString.split(";")
        getFormat = str(dVL[0])
        
        # Check the csv report matches the gold file
        testReportPath = rfpath
        goldReportPath = os.path.join(fp.paths.goldFileFolder, rfn + str(idx + 1) + '_' + str(dVL[0]) + "_Report.csv")
        
        #prepare the warning and error meg
        elineinfo = ""
        wlineinfo = ""


        with open (lfpath) as fplogfile:
            for line in fplogfile:
                if 'Error' in line:
                    elineinfo =elineinfo+ line.strip();
                if 'Warning' in line:
                    wlineinfo =wlineinfo+ line.strip();
                    
        # Check the log files shows it finished
        if not ('task is finished' in open(lfpath).read()):
            failinfo ="   The string 'task is finished' is NOT found in the log file" 
            print(str(idx + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + failinfo +"\n")
            self.writeInTestFile(tcN + "." + str(idx + 1) + "," +erL[idx]+ "," +  "FAIL" + "," + equal(erL[idx] , "FAIL") + "," + getFormat[-3:] + ',' + " ".join(vcl) +','+  failinfo +';'+ elineinfo+wlineinfo+ ".\n")
            self.TotalNumberOfFailTC +=1
        elif (not fp.util.verifyReportCsvPair(testReportPath, goldReportPath)):                 
            print(str(idx + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[1] + "\n")  
            self.writeInTestFile(tcN + "." + str(idx + 1) + "," +erL[idx]+ "," +  "FAIL" + "," + equal(erL[idx] , "FAIL") + "," + getFormat[-3:] + ',' + " ".join(vcl) +','+  "   Failing condition: " + conditions[1] +wlineinfo+ ".\n")
            self.TotalNumberOfFailTC +=1  
        # Check the perf log is within the allowed range
        elif not fp.util.verifyPerfLog(eAD):
            print(str(idx + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[2] + "\n")  
            self.writeInTestFile(tcN + "." + str(idx + 1) + "," +erL[idx]+ "," +  "FAIL" + "," + equal(erL[idx] , "FAIL") + "," + getFormat[-3:] + ',' + " ".join(vcl) +','+  conditions[2] +wlineinfo+ ".\n")
            self.TotalNumberOfFailTC +=1
        else:
            passDescription = ""
            for val in conditions:
                passDescription += "   " + val + " as expected. "
                
            print(str(idx + 1) + " PASS - Format " + getFormat + " is supported.\n")  
            self.writeInTestFile(tcN + "." + str(idx + 1) + "," +erL[idx]+ "," +  "PASS" + "," + equal(erL[idx] , "PASS") + "," + getFormat[-3:] + ',' + " ".join(vcl) +','+  passDescription + " " +wlineinfo+ "\n")
            self.TotalNumberOfPassTC += 1
            count += 1
            #self.countSupportedFormats += 1
         
        self.totalNumberOfTC += 1            
        

testResultObject = testResultClass()
