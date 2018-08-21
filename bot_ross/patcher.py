import os


def patch():
    if os.name == 'nt':  # meaning Windows
        # patch the HOME variable so pycnc doesn't error when it tries to store files there
        # HOMEPATH is usually C:\Users\{username}
        os.environ['HOME'] = os.environ['HOMEPATH']
