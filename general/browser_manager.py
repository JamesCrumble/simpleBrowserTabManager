from typing import Callable
from selenium import webdriver

from .schemas import Tab


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
            print(f'switched to {index} tab')
            return True

        return False

    def check_page_loading_state(
        self,
        page_loading_state_handler: Callable[
            [webdriver.Chrome], bool
        ] = lambda v: True
    ) -> bool:
        tab_index: int = self._tabs_by_uuid[self.driver.current_window_handle].index
        print(f"Checking if \"{tab_index}\" page is loaded.")
        if (
            page_loading_state_handler(self.driver)
            and self.driver.execute_script(
                'return document.readyState;'
            ) == 'complete'
        ):
            print(f"\"{tab_index}\" tab page successfully loaded.")
            return True

        return False

    def load_page(self, url: str) -> None:
        self.driver.get(url)

    def run(self) -> 'BrowserManager':

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['pageLoadStrategy'] = "none"  # default is "normal".

        if self.driver_options is not None:
            self.driver_options: webdriver.ChromeOptions = self.driver_options()

            for argument in self.option_arguments:
                self.driver_options.add_argument(argument)

        self.driver: webdriver.Chrome = self.driver(
            options=self.driver_options,
            desired_capabilities=capabilities
        )

        self._append_tab(Tab(
            index=len(self.tabs),
            uuid=self.driver.current_window_handle
        ))

        del self.driver_options
        del self.option_arguments

        return self

    def shutdown(self) -> None:
        self.driver.close()
