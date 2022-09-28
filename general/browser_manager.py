from typing import Callable
from selenium import webdriver

from .schemas import Tab
from .services.logger import BROWSER_LOGGER
from .services.path import CHROME_DRIVER_PATH


class BrowserManager:

    __slots__ = (
        'driver', 'tabs',
        '_tabs_by_uuid', 'driver_options', 'option_arguments'
    )

    def __init__(
        self,
        driver: webdriver.Chrome,
        driver_options: webdriver.ChromeOptions = None,
        option_arguments: list[str] = list()
    ):
        self.tabs: dict[int, Tab] = dict()
        self._tabs_by_uuid: dict[str, Tab] = dict()
        self.driver: webdriver.Chrome = driver
        self.driver_options = driver_options
        self.option_arguments = option_arguments

    def _append_tab(self, tab: Tab) -> None:
        self.tabs[len(self.tabs)] = tab
        self._tabs_by_uuid[tab.uuid] = tab

    def open_new_tab(self, url: str = None) -> None:
        self.driver.execute_script(f'''window.open("{url or ''}");''')
        self._append_tab(Tab(
            index=len(self.tabs),
            uuid=self.driver.window_handles[-1]
        ))

    def switch_to_tab(self, index: int) -> bool:
        if tab := self.tabs.get(index):
            self.driver.switch_to.window(tab.uuid)
            BROWSER_LOGGER.info(f'SWITCHED TO {index} TAB')
            return True

        return False

    def check_page_loading_state(
        self,
        page_loading_state_handler: Callable[
            [webdriver.Chrome], bool
        ] = lambda v: True
    ) -> bool:
        tab_index: int = self._tabs_by_uuid[self.driver.current_window_handle].index
        BROWSER_LOGGER.info(f"CHECKING IF \"{tab_index}\" PAGE IS LOADED")

        if (
            page_loading_state_handler(self.driver)
            and self.driver.execute_script(
                'return document.readyState;'
            ) == 'complete'
        ):
            BROWSER_LOGGER.info(
                f"\"{tab_index}\" TAB PAGE SUCCESSFULLY LOADED"
            )
            return True

        return False

    def load_page(self, url: str) -> None:
        self.driver.get(url)

    def run(self) -> 'BrowserManager':

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['pageLoadStrategy'] = "none"  # default is "normal".

        BROWSER_LOGGER.debug('ADDING CHROME DRIVER OPTIONS')

        if self.driver_options is not None:
            self.driver_options: webdriver.ChromeOptions = self.driver_options()

            for argument in self.option_arguments:
                self.driver_options.add_argument(argument)

        BROWSER_LOGGER.debug('ADDING CHROME DRIVER OPTIONS: "DONE"')

        self.driver: webdriver.Chrome = self.driver(
            executable_path=CHROME_DRIVER_PATH,
            options=self.driver_options,
            desired_capabilities=capabilities
        )

        BROWSER_LOGGER.info('DRIVER WAS STARTED')

        self._append_tab(Tab(
            index=len(self.tabs),
            uuid=self.driver.current_window_handle
        ))

        del self.driver_options
        del self.option_arguments

        return self

    def shutdown(self) -> None:
        BROWSER_LOGGER.info('SHUTTING DOWN. BYE .-.')
        self.driver.close()
