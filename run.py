import time

from selenium import webdriver

from general.settings import settings
from general.browser_manager import BrowserManager


if __name__ == '__main__':

    browser = BrowserManager(
        webdriver.Chrome,
        webdriver.ChromeOptions,
        settings.GOOGLE_OPTIONS_ARGUMENTS
    ).run()

    try:

        browser.load_page(settings.VK_PAGE)
        browser.open_new_tab(settings.VK_PAGE)
        browser.open_new_tab(settings.VK_PAGE)
        browser.open_new_tab(settings.VK_PAGE)
        browser.open_new_tab(settings.VK_PAGE)

        for tab_index in browser.tabs:

            while not browser.check_page_loading_state():
                time.sleep(0.1)

            browser.switch_to_tab(tab_index)
            time.sleep(0.5)

    except KeyboardInterrupt:
        browser.driver.close()
