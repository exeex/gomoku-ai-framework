import sys

file = None


def log(msg, *arg, **kwargs):
    print(msg, *arg, **kwargs, file=sys.stderr)
    print(msg, *arg, **kwargs, file=file)


def open_log_file(filename):
    global file
    file = open(filename, 'w')


def save_log_file():
    global file
    file.close()


if __name__ == '__main__':
    log('gg')
