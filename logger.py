from datetime import datetime

LOG_ENABLED = True


class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(*args):
    if LOG_ENABLED:
        print(C.OKBLUE+"["+datetime.now().strftime("%H:%M:%S.%f")[:-3]+"]"+C.ENDC, *args)
