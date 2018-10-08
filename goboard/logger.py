import sys


def log(msg, *arg, **kwargs):
    print(msg, *arg, **kwargs, file=sys.stderr)


if __name__ == '__main__':
    log('gg')
