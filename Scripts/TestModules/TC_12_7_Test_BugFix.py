'''
Updated on July 05, 2016
@author: Green Zhao
'''

import subprocess
import generateTestResultFile, fp
import sys, string, os
from random import randint
import re
from optparse import OptionParser
import glob


class TC_12_7_Class(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.countSupportedFormats = 0

        
    def run_TC_12_7(self, elemetnAttributeDictionary):
    
    
        eAD = elemetnAttributeDictionary;
        generateTestResultFile.testResultObject.openTestFile()
    
        tcNumber = eAD.get('number')
        fileName = eAD.get('string')
        folder = eAD.get('mainfolder')
        subdir = eAD.get('subfolder')
        
        
        print("------------------------------- Test Case " + tcNumber + " Execution Started --------------------------------------") 
        print("Test description: " + eAD.get('description'))
        
        print("Test case " + tcNumber + ": Test BugFix: ")
        generateTestResultFile.testResultObject.writeInTestFile("\n")
        generateTestResultFile.testResultObject.writeInTestFile(",,Test and verify buggy videos:\n")
        
        ############### Pre Command ################
        distortedVideosList = eAD.get("distVideos").split(',')
        referenceVideosList = eAD.get("refVideos").split(',')
        cmdlist = eAD.get("commandlist").split(',')
        #numberOfVideos = len(distortedVideosList)
        numberOfVideos = len(cmdlist)
        reportFileName = eAD.get('output')
        expectedresultList = eAD.get("expectedresult").split(',')
        expectedcount = len(expectedresultList) 
        
        ################ Test Command ################
        command = eAD.get('command')            # get command with parameters from dictionary which is taken from XML file
        commandList = command.split( )          # converted string to list as subprocess.POpen (...) accepts list or touple as input parameter    

        #-----------------------------------------------------------
        startindex = fp.num3start_end_Index_Of_TC[0] 
        endindex = fp.num3start_end_Index_Of_TC[1]
        
        for INDEX in range(numberOfVideos):
            if(endindex<INDEX+1):
                return ;
            if(INDEX+1<startindex):
                continue ;
            
            ref_Idx = 0
            test_Idx = 0
            if INDEX<3:
                    ref_Idx = 0
                    test_Idx = 0
            else:
                    ref_Idx = 1
                    test_Idx = 1
            videoCommandList = [fp.paths.sqmLibApplication, "-r", os.path.join(fp.paths.testDataDir,folder,subdir,referenceVideosList[ref_Idx]), "-d", os.path.join(fp.paths.testDataDir,folder,subdir,distortedVideosList[test_Idx])]
            cmdlist2 = cmdlist[INDEX].split()
            videoCommandList.extend(cmdlist2)
            videoCommandList.extend(commandList)
            
            lfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[test_Idx]) + ".log")
            rfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[test_Idx]) + "_Report.csv")
            pipePath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[test_Idx]) + ".screenlog")
            videoCommandList.extend(['-lt', 'file', '-lf', lfPath, '-rf', rfPath])
            #videoCommandList.extend(['-lt', 'file', '-lf', lfPath, '-rf', rfPath, '-f2p', eAD.get('f2p')])
            
            fp.util.printCommandList(videoCommandList)
            test_1 = subprocess.Popen(videoCommandList, stdout=subprocess.PIPE)         # execute command on command prompt and save output result in test veriable
                                 
            # If the process takes longer than 1500 seconds kill it and print the output so far

            try:
                outs, errs = test_1.communicate(timeout=1500)                
            except subprocess.TimeoutExpired:
                test_1.kill()
                outs, errs = test_1.communicate()
                print("ERROR: SQM TIMED OUT")
                print(outs.decode("utf-8"))
                print("ERROR: SQM TIMED OUT")
            
            fullOuts = outs.decode("utf-8")
            outs = (fullOuts[:53800] + '...') if len(fullOuts) > 53803 else fullOuts
            print("\nCommand output: ", outs)

            if( fp.screenshot==1):
                with open(pipePath,"w+") as fileobj:
                    for temp in range(len(videoCommandList)):
                        fileobj.write(videoCommandList[temp]+' ');
                    fileobj.write("\nCommand output: "+outs)    
            
            ################ Verification ################ 
            #
            conditionString = elemetnAttributeDictionary.get('conditions')
            conditions = conditionString.split(";")
            getFormat = str(distortedVideosList[test_Idx])
            
            # Check the csv report matches the gold file
            testReportPath = rfPath
            goldReportPath = os.path.join(fp.paths.goldFileFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[test_Idx]) + "_Report.csv")
            
            #prepare the warning and error meg
            elineinfo = ""
            wlineinfo = ""

            if not os.path.exists(lfPath):
                print(str(INDEX + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[1] + "\n")
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[INDEX]+ "," + "FAIL" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+ "   Failing condition: " + conditions[1] +wlineinfo+'  Thelogfile is not exist'+ ".\n")
                generateTestResultFile.testResultObject.TotalNumberOfFailTC +=1
                generateTestResultFile.testResultObject.totalNumberOfTC += 1  
                continue    
            

            with open (lfPath) as fplogfile:
                for line in fplogfile:
                    if 'Error' in line:
                        elineinfo =elineinfo+ line.strip();
                    if 'Warning' in line:
                        wlineinfo =wlineinfo+ line.strip();
                        
            # Check the log files shows it finished
            if not ('task is finished' in open(lfPath).read()):
                failinfo ="   The string 'task is finished' is NOT found in the log file" 
                print(str(INDEX + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + failinfo +"\n")
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[INDEX]+ "," + "FAIL" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+  failinfo +';'+ elineinfo+wlineinfo+ ".\n")
                generateTestResultFile.testResultObject.TotalNumberOfFailTC +=1
            elif (not fp.util.verifyReportCsvPair(testReportPath, goldReportPath)):                 
                print(str(INDEX + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[1] + "\n")  
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[INDEX]+ "," + "FAIL" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+  "   Failing condition: " + conditions[1] +wlineinfo+ ".\n")
                generateTestResultFile.testResultObject.TotalNumberOfFailTC +=1  
            # Check the perf log is within the allowed range
            elif not fp.util.verifyPerfLog(eAD):
                print(str(INDEX + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[2] + "\n")  
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[INDEX]+ "," + "FAIL" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+  conditions[2] +wlineinfo+ ".\n")
                generateTestResultFile.testResultObject.TotalNumberOfFailTC +=1
            else:
                passDescription = ""
                for val in conditions:
                    passDescription += "   " + val + " as expected. "
                    
                print(str(INDEX + 1) + " PASS - Format " + getFormat + " is supported.\n")  
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[INDEX]+ "," + "PASS" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+  passDescription + " " +wlineinfo+ "\n")
                generateTestResultFile.testResultObject.TotalNumberOfPassTC += 1
                self.countSupportedFormats += 1
             
            generateTestResultFile.testResultObject.totalNumberOfTC += 1
            

        #generateTestResultFile.testResultObject.TotalNumberOfFailTC += numberOfVideos - self.countSupportedFormats  
        generateTestResultFile.testResultObject.closeTestFile()

TC_12_7_ClassObject = TC_12_7_Class()



