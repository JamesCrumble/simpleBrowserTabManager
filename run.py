import time

from selenium import webdriver

from general.settings import settings
from general.browser_manager import BrowserManager

if __name__ == '__main__':

    TEST_URL: str = 'https://guidedhacking.com/'

    try:
        browser = BrowserManager(
            webdriver.Chrome,
            webdriver.ChromeOptions,
            settings.GOOGLE_OPTIONS_ARGUMENTS
        ).run()

        browser.load_page(TEST_URL)
        browser.open_new_tab(TEST_URL)
        browser.open_new_tab(TEST_URL)
        browser.open_new_tab(TEST_URL)
        browser.open_new_tab(TEST_URL)

        for tab_index in browser.tabs:

            while not browser.check_page_loading_state():
                time.sleep(0.1)

            browser.switch_to_tab(tab_index)
            time.sleep(0.5)

        print('all pages was loaded')
    except KeyboardInterrupt:
        browser.driver.close()
