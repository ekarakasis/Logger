#  ==================================================================================
#  
#  Copyright (c) 2019, Evangelos G. Karakasis 
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#  
#  ==================================================================================

import os
import logging

class Logger: 
    """Organizes loggers and the corresponding log files for easy access. 
    
    The loggers and the log files are kept in static lists and each instance of the 
    class have access to a particular list element. It is good practice to kill 
    all loggers and remove all log files at the start of your module. 
    
    Parameters
    ---------- 
    loggerName: str
        The name of the added logger. 
        
    logFileName: str 
        The name of the log file that is connected with the logger. You may have the same
        log file attached to different loggers. 
        
    rootFolder: str, (optional, default: 'Logs')
        The name of the folder in which the log files will be saved. 
        
    formatType: str, (optional, default: 'time-name-level-message')
        It determines the formatter for the logger. The supported formats are:
            * 'time-name-level-message'            
            * 'time-level-message'            
            * 'time-message'            
            * 'level-message'
            * 'unformated'
            
    Examples 
    -------- 
    
    Logger.KillAllLoggers()
    Logger.DeleteAllLogFiles()

    print(Logger.logFileList)
    print(Logger.loggerList)

    # defines two loggers that are attached to the same log file
    logger_frm = Logger('calibLogger.TNLM', 'calibrationLog', 'Logs', 'time-name-level-message')
    logger_unf = Logger('calibLogger.U', 'calibrationLog', 'Logs', 'unformated')

    print(Logger.logFileList)
    print(Logger.loggerList)

    # ---------------------------------------

    # DO SOMETHING
    logger_unf.Log(True, 'info', "===== SEPARATOR =====")
    logger_frm.Log(True, 'debug', "This is a DEBUG level record.")
    logger_frm.Log(True, 'warning', "This is a WARNING level record.")
    logger_frm.Log(True, 'info', "This is an INFO level record.")
    logger_frm.Log(True, 'error', "This is an ERROR level record.")
    logger_frm.Log(True, 'critical', "This is a CRITICAL level record.")

    # YOUR LOG FILE SHOULD LOOKS LIKE THAT
    #
    # ===== SEPARATOR =====
    # 2019-Aug-26 - 11:10:59 - calibLogger.TNLM - DEBUG - This is a DEBUG level record.
    # 2019-Aug-26 - 11:10:59 - calibLogger.TNLM - WARNING - This is a WARNING level record.
    # 2019-Aug-26 - 11:10:59 - calibLogger.TNLM - INFO - This is an INFO level record.
    # 2019-Aug-26 - 11:10:59 - calibLogger.TNLM - ERROR - This is an ERROR level record.
    # 2019-Aug-26 - 11:10:59 - calibLogger.TNLM - CRITICAL - This is a CRITICAL level record.

    # ---------------------------------------

    # since the loggers are attached to the same log file
    # we have first to close both in order to delete the file
    logger_frm.CloseLogger()
    logger_unf.CloseLogger()
    # after having closed both loggers, we can delete the file.
    # Actually only one delete process is enough to remove the file,
    # but the second delete takes place in order to update the static lists
    # loggerList and logFileList. We set the lists elements to None, because 
    # we do not want the other instances to lose their access to the correct loggers. 
    logger_unf.DeleteLogFile()
    logger_frm.DeleteLogFile()

    print(Logger.logFileList)
    print(Logger.loggerList)

    # and if we want to reset the static lists...
    Logger.KillAllLoggers()
    Logger.DeleteAllLogFiles()

    print(Logger.logFileList)
    print(Logger.loggerList)
    
    """
    
    loggerList = []
    logFileList = []        
    
    def __init__(self, loggerName, logFileName, rootFolder='Logs', formatType='time-name-level-message'):        
        if not os.path.exists(rootFolder):
            os.mkdir(rootFolder)      
        logFileExtension = '.log'
        
        self._loggerIdx = len(Logger.loggerList)
        
        self._logFileFullPath = rootFolder + '/' + logFileName + logFileExtension
        self._loggerName = loggerName
        self._formatType = formatType
        
        Logger.loggerList.append(Logger.CreateLogger(self._loggerName, self._logFileFullPath, self._formatType))
        Logger.logFileList.append(self._logFileFullPath)
                
        self._logger = Logger.loggerList[-1]
        self._loggerClosed = False            
                   
    def Log(self, logFlag, logLevel, *args):
        """Applies the logger. 
        
        Parameters
        ---------- 
        logFlag: bool
            Determines if the logger will be applied or not. By setting this flag to False
            you can actually disable the logging functionality. Its purpose is to allow
            dynamically enabling/disabling the logging service.
            
        logLevel: str
            The record's logger level. The supported levels are:
                * 'debug'
                * 'warning'
                * 'info'
                * 'error'
                * 'critical'
            
        *args: tuple of arguments
            These argumets are the ones you would have to feed to a regular logger. 
            
        Example
        ------- 
        Logger.KillAllLoggers()
        Logger.DeleteAllLogFiles()
        
        logger_tnlm = Logger('LoggerName.TNLM', 'LogFile', 'Logs', 'time-name-level-message')        
        EnableLogging = True
        
        logger_tnlm.Log(EnableLogging, 'info', "This is an INFO level record.")
        logger_tnlm.Log(EnableLogging, 'warning', "This is an WARNING level record.")
        """
        if logFlag:
            if logLevel == 'info':
                self._logger.info(*args)
            elif logLevel == 'warning':
                self._logger.warning(*args)
            elif logLevel == 'error':
                self._logger.error(*args)
            elif logLevel == 'critical':
                self._logger.critical(*args)
            elif logLevel == 'debug':
                self._logger.debug(*args)
            else:
                self._logger.info(*args)            
     
    def CloseLogger(self):    
        """Removes the handler for a particular class instance. 
        
        Sets corresponding loggerList element to None.
        """
        handlers = self._logger.handlers[:]
        for handler in handlers:
            handler.close()
            self._logger.removeHandler(handler)        
        self._loggerClosed = True        
        Logger.loggerList[self._loggerIdx] = None
            
    def DeleteLogFile(self):
        """Deletes the log file from the hard disc. 
        
        The corresponding logger must have been closed first. 
        It also sets the corresponding logFileList element to None.
        """
        if self._loggerClosed:
            if os.path.exists(self._logFileFullPath):
                os.remove(self._logFileFullPath)
            Logger.logFileList[self._loggerIdx] = None
                
    @staticmethod
    def KillAllLoggers():
        """It closes (kills) all the logger elements in the loggerList and resets it as an emtpy list.
        """
        for logger in Logger.loggerList:
            if logger is not None:
                handlers = logger.handlers[:]
                for handler in handlers:
                    handler.close()
                    logger.removeHandler(handler)                  
        Logger.loggerList = []
                
    @staticmethod
    def DeleteAllLogFiles():
        """It deletes all the log files which are kept in the logFileList and resets it as an emtpy list.
        """
        for logfile in Logger.logFileList:
            if logfile is not None:
                if os.path.exists(logfile):
                    os.remove(logfile)
        Logger.logFileList = []
                
    @staticmethod
    def CreateLogger(loggerName, logFileFullPath, formatType='time-level-message'): 
        """Creates the logger. 
        
        Parameters
        ---------- 
        loggerName: str
            The name of the added logger. 

        logFileFullPath: str 
            The full path of the log file that is connected with the logger. You may have the same
            log file attached to different loggers.  

        formatType: str, (optional, default: 'time-name-level-message')
            It determines the formatter for the logger. The supported formats are:
                * 'time-name-level-message'            
                * 'time-level-message'            
                * 'time-message'            
                * 'level-message'
                * 'unformated'
                
        Returns 
        ------- 
        Logger object
            The function return the logger object that has been created. 
            The handler of the log file is a RotatingFileHandler with maxBytes=1024*1000 and backupCount=5.
        """
        if formatType == 'time-name-level-message':
            FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%b-%d - %H:%M:%S')
        elif formatType == 'time-level-message':
            FORMAT = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%b-%d - %H:%M:%S')        
        elif formatType == 'time-message':
            FORMAT = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%b-%d - %H:%M:%S')        
        elif formatType == 'level-message':
            FORMAT = logging.Formatter('%(levelname)s - %(message)s')        
        elif formatType == 'unformated':
            FORMAT = logging.Formatter('')
        else:
            FORMAT = logging.Formatter('')

        logger = logging.getLogger(loggerName)    
        logger.setLevel(logging.DEBUG)

        fileHandler = logging.handlers.RotatingFileHandler(logFileFullPath, maxBytes=1024*1000, backupCount=5)
        fileHandler.setFormatter(FORMAT)
        logger.addHandler(fileHandler)

        return logger