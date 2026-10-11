###logStdErr.py
import sys
import os
import pjTkInter as tk
import traceback
class logStdErrClass:
  def __init__(self):
    self.bundleAppPath="/private/var/containers/Bundle/Application/62C432BB-3DAA-483B-B90B-8547E6261865/PeterJohn-iphoneos.app"
    self.bundlePyResPath="/private/var/containers/Bundle/Application/62C432BB-3DAA-483B-B90B-8547E6261865/PeterJohn-iphoneos.app/python-resources"
    self.sandBoxDocumentsPath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents"
    self.sandBoxProjDirPath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash"
    os.makedirs("/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles", exist_ok=True)
    self.errFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdErr.txt"
    self.outFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdOut.txt"
    self.inFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdIn.txt"
    self.clHistoryFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logCommandLineHistory.txt"
    pythonVersionDir="python3.11"
    self.sitePackagesNumPyPyCacheDirPath=self.sandBoxDocumentsPath + "/usrLocal/lib/" + pythonVersionDir + "site-packages/numpy/__pycache__"
    try :
      ####os.makedirs(self.sitePackagesNumPyPyCacheDirPath, exist_ok=True)
      import pj ##YassunAdd;2026-0404;
      pj.forceFreeMemoryMBytes(100) ##YassunAdd;2026-0404;
    except PermissionError as e :
      self.printExc( e )
####
  def setProjectName(self,projectName):
    self.bundleAppPath="/private/var/containers/Bundle/Application/62C432BB-3DAA-483B-B90B-8547E6261865/PeterJohn-iphoneos.app"
    self.bundlePyResPath="/private/var/containers/Bundle/Application/62C432BB-3DAA-483B-B90B-8547E6261865/PeterJohn-iphoneos.app/python-resources"
    self.sandBoxDocumentsPath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents"
    self.sandBoxProjDirPath=self.sandBoxDocumentsPath + '/' + projectName
    self.errFilePath=="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdErr.txt"
    self.outFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdOut.txt"
    self.inFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logStdIn.txt"
    self.clHistoryFilePath="/var/mobile/Containers/Data/Application/2E46F557-1822-4FD2-95CA-3971E5A01A41/Documents/s005ThreeDimSquash/logFiles/logCommandLineHistory.txt"
####
  def __del__(self):
    del self.bundleAppPath
    del self.bundlePyResPath
    del self.sandBoxDocumentsPath
    del self.sandBoxProjDirPath
    del self.errFilePath
    del self.outFilePath
    del self.inFilePath
    del self.clHistoryFilePath
####
  ###
  import traceback
  def errToFile(self) :
    try :
      self.errFile=open(\
self.errFilePath,'w+')
      self.outFile=open(\
self.outFilePath,'w+')
      self.inFile=open(\
self.inFilePath,'w+')
      sys.stderr=self.errFile
      sys.stdout=self.outFile
      sys.stdin=self.inFile
    except FileNotFoundError as e : ###YassunAdd;
      pass ####YassunModified;2023-0816;;
      ###s = traceback.format_exc()
      ###tk.appendTitleLabel(s)
  ###
  import traceback
  def printExc(self, e) :
    s = traceback.format_exc()
    try :
      f = open(self.errFilePath, "a")
      import os
      f.seek(0, os.SEEK_END)
      f.write(s)
      f.close()
      tk.appendTitleLabel(s)
    except FileNotFoundError as e : ###YassunAdd;
      pass ###YassunAdd;2023-0816;;
      ###s = traceback.format_exc()
      ###tk.appendTitleLabel(s)
  ####
  def print(self, anyStr) : ##AvoidNameConflicts;;
    s = anyStr+'\n'
    try :
      ####f = open(self.errFilePath, "a")
      import os 
      dirName = os.path.dirname(self.errFilePath) ##YassunAdd;2026-0412;EvenIf"w"mode,if there'sNot the directory,causesFileNotFound(ErrNo2);;
      os.makedirs(dirName,exist_ok=True)
      with open(self.errFilePath, 'a', encoding='utf-8') as f: ##YassunAdd;2026-0412;toOutput self.divChar(0xF7);;
        f.seek(0, os.SEEK_END)
        f.write(s)
        f.close()
        tk.appendTitleLabel(s)
    except FileNotFoundError as e : ###YassunAdd;
      pass ###YassunAdd;2023-0816;;
      ###s = traceback.format_exc()
      ###tk.appendTitleLabel(s)
#lse=logStdErrClass()
#lse.errToFile()
#a=1+"2"