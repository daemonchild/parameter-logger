import os
from datetime import datetime


""" 

    Functions for Log File Management


"""

def file_init (LOGPATH,LOGFILE):

    logfile = LOGPATH + LOGFILE

    if not os.path.exists(LOGPATH):
            os.makedirs(LOGPATH)

    if not os.path.exists(logfile):

        now = datetime.now()

        try:
            with open(logfile, 'a') as fh:
                fh.write(f"Log Initialised: {str(now.date())} at {str(now.time())} \n")
                os.utime(logfile, None)
                fh.close()
                return (0)
        except IOError as err:
            print("OS error: {0}".format(err))
            return (1)

    else:

        return (1)


def file_delete (LOGPATH,LOGFILE):

    logfile = LOGPATH + LOGFILE

    if os.path.exists(LOGPATH):
            # DELETE IT! :)
            return (0)
    else:
            return (1)


def file_list (LOGPATH):

    logfiles = []

    for file in os.listdir(LOGPATH):
        if file.endswith('.log'):
            logfile = {'file': str(file)}
            logfiles.append(logfile)

    return (logfiles)


""" 

    Functions for Log Entry Management


"""

def entry_add (LOGPATH, LOGFILE, message):

    logfile = LOGPATH + LOGFILE

    try:
        with open(logfile, 'a') as fh:

            now = datetime.now()
            stamp = now.strftime("%Y%m%d-%H%M%S")

            entry = f"{stamp} {str(message)} \n"

            fh.write(entry)
            fh.close()
    except IOError as err:
        print("OS error: {0}".format(err))
        return (1)

    return (0)
