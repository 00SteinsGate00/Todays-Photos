import datetime
import os

def parseTimeArgument(time_argument):
    if(time_argument == 'today'):
        return datetime.date.today()
    elif(time_argument == 'yesterday'):
        return datetime.date.today() - datetime.timedelta(1)
    else:
        try:
            year, month, day = time_argument.split('-')
            return datetime.date(int(year), int(month), int(day))
        except Exception as e:
            return None


def modTimestamp(file):
    return datetime.date.fromtimestamp(os.path.getmtime(file))
