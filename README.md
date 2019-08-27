# Logger

This project created with the intention to build a handy simple class for managing loggers. The main idea is to keep different loggers in a static list and each class instance to have access to a specific logger.

## Getting Started

There are no dependencies for this project.

### Installing

To install this package just download this repository from GitHub or by using the following command line:

> $ git clone https://github.com/ekarakasis/Logger

Afterwards, go to the local root folder, open a command line and run:

> $ pip install .

and if you want to install it to a specific Anaconda environment then write:

> $ activate <Some_Environment_Name>
>
> $ pip install .

### Uninstalling

To uninstall the package just open a command and write:

> $ pip unistall Logger

To uninstall it from a specific conda environment write:

> $ activate <Some_Environment_Name>
>
> $ pip unistall Logger


## Examples

### Example 1

Let us assume a function Func1, which use one input and does nothing. And let us further assume that we want this input to be a number (integer or float, not None) and that this number can only take values in the range [1,10].

```python
Logger.KillAllLoggers()
Logger.DeleteAllLogFiles()

print(Logger.logFileList)
print(Logger.loggerList)

# defines two loggers that are attached to the same log file
logger_frm = Logger(
    'someLogger.TNLM', 
    'LogFile', 
    'Logs', 
    'time-name-level-message'
)

logger_unf = Logger(
    'someLogger.U', 
    'LogFile', 
    'Logs', 
    'unformated'
)

print(Logger.logFileList)
print(Logger.loggerList)

# ---------------------------------------

# DO SOMETHING
logger_unf.Log(True, 'info', "\n===== SEPARATOR =====")
logger_frm.Log(True, 'debug', "This is a DEBUG level record.")
logger_frm.Log(True, 'warning', "This is a WARNING level record.")
logger_frm.Log(True, 'info', "This is an INFO level record.")
logger_frm.Log(True, 'error', "This is an ERROR level record.")
logger_frm.Log(True, 'critical', "This is a CRITICAL level record.")

# YOUR LOG FILE SHOULD LOOKS LIKE THAT
#
# ===== SEPARATOR =====
# 2019-Aug-26 - 11:10:59 - someLogger.TNLM - DEBUG - This is a DEBUG level record.
# 2019-Aug-26 - 11:10:59 - someLogger.TNLM - WARNING - This is a WARNING level record.
# 2019-Aug-26 - 11:10:59 - someLogger.TNLM - INFO - This is an INFO level record.
# 2019-Aug-26 - 11:10:59 - someLogger.TNLM - ERROR - This is an ERROR level record.
# 2019-Aug-26 - 11:10:59 - someLogger.TNLM - CRITICAL - This is a CRITICAL level record.

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
```

## License

This project is licensed under the MIT License.
