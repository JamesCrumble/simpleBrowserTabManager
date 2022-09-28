import os
import sys


def create_if_not_existed(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path)

    return path


PC_USERNAME: str = 'namst'

# ROOT_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ROOT_PATH: str = os.curdir
CHROME_DRIVER_PATH: str = os.path.join(ROOT_PATH, 'chrome_driver', 'chromedriver.exe')  # noqa
# CHROME_USER_DATA_DIR: str = create_if_not_existed(os.path.join(ROOT_PATH, 'chrome_user_data'))  # noqa
CHROME_USER_DATA_ROOT: str = os.path.join(
    # START OF PATH LIKE C:\\ or /home
    # os.path.abspath('.').split(os.path.sep)[0] + os.path.sep,
    'C:\\' if sys.platform == 'win32' else '/home',
    'Users', PC_USERNAME, 'AppData', 'Local', 'Google', 'Chrome',

)
CHROME_USER_DATA_DIR: str = os.path.join(CHROME_USER_DATA_ROOT, 'selenium_chrome_driver')  # noqa
