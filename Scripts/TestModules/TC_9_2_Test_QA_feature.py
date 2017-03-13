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


class TC_9_2_Class(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.countSupportedFormats = 0

        
    def run_TC_9_2(self, elemetnAttributeDictionary):
    
    
        eAD = elemetnAttributeDictionary;
        generateTestResultFile.testResultObject.openTestFile()
    
        tcNumber = eAD.get('number')
        fileName = eAD.get('string')
        folder = eAD.get('mainfolder')
        folder2 = eAD.get('subfolder')
        
        print("------------------------------- Test Case " + tcNumber + " Execution Started --------------------------------------") 
        print("Test description: " + eAD.get('description'))
        
        print("Test case " + tcNumber + ": Test Different Resolutions: ")
        generateTestResultFile.testResultObject.writeInTestFile("\n")
        generateTestResultFile.testResultObject.writeInTestFile(",,Test and verify PID support function:\n")
        
        ############### Pre Command ################
        distortedVideosList = eAD.get("distVideos").split(',')
        referenceVideosList = eAD.get("refVideos").split(',')
        cmdlist = eAD.get("commandlist").split(',')
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
            if(endindex<INDEX+1) :
                return ;
            if(INDEX+1<startindex):
                continue ;
        

            if INDEX>=8:
                videoCommandList = [fp.paths.sqmLibApplication, "-r", os.path.join(fp.paths.testDataDir,folder,folder2 ,referenceVideosList[0]), "-d", os.path.join(fp.paths.testDataDir,folder,folder2,distortedVideosList[8])]
            else:                
                videoCommandList = [fp.paths.sqmLibApplication, "-r", os.path.join(fp.paths.testDataDir,folder,folder2 ,referenceVideosList[0]), "-d", os.path.join(fp.paths.testDataDir,folder,folder2,distortedVideosList[INDEX])]

            cmdlist2 = cmdlist[INDEX].split()
            videoCommandList.extend(cmdlist2)
            videoCommandList.extend(commandList)
            
            if INDEX>=8:
                lfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[8].split('.ts ',1)[0]) + ".log")
                rfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[8].split('.ts ',1)[0]) + "_Report.csv")
                pipePath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[8].split('.ts ',1)[0]) + ".screenlog")
            else:    
                lfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[INDEX].split('.ts ',1)[0]) + ".log")
                rfPath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[INDEX].split('.ts ',1)[0]) + "_Report.csv")
                pipePath = os.path.join(fp.paths.testRunLogFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[INDEX].split('.ts ',1)[0]) + ".screenlog")

            videoCommandList.extend(['-lt', 'file', '-lf', lfPath, '-rf', rfPath, '-f2p', eAD.get('f2p')])
            
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
            if not os.path.exists(lfPath):
                print(str(INDEX + 1) + " FAIL - Format " + getFormat + " is NOT supported. Failing condition: " + conditions[1] + "\n")
                generateTestResultFile.testResultObject.writeInTestFile(tcNumber + "." + str(INDEX + 1) + "," +expectedresultList[0]+ "," + "FAIL" + "," + getFormat[-3:] + ',' + " ".join(videoCommandList) +','+ "   Failing condition: " + conditions[1] +wlineinfo+'  Thelogfile is not exist'+ ".\n")
                generateTestResultFile.testResultObject.TotalNumberOfFailTC +=1
                generateTestResultFile.testResultObject.totalNumberOfTC += 1  
                continue    
            
            if INDEX>=8:
                getFormat = str(distortedVideosList[8])
            else:    
                getFormat = str(distortedVideosList[INDEX])
            
           
            if INDEX>=8:
                goldReportPath = os.path.join(fp.paths.goldFileFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[8]) + "_Report.csv")
            else :
                goldReportPath = os.path.join(fp.paths.goldFileFolder, reportFileName + str(INDEX + 1) + '_' + str(distortedVideosList[INDEX]) + "_Report.csv")
            
            #prepare the warning and error meg
            elineinfo = ""
            wlineinfo = ""
            
            

            generateTestResultFile.testResultObject.verify1(elemetnAttributeDictionary, getFormat, goldReportPath, rfPath, fp, reportFileName, INDEX, lfPath, expectedresultList, tcNumber, videoCommandList, self.countSupportedFormats);
            

        #generateTestResultFile.testResultObject.TotalNumberOfFailTC += numberOfVideos - self.countSupportedFormats  
        generateTestResultFile.testResultObject.closeTestFile()

TC_9_2_ClassObject = TC_9_2_Class()



