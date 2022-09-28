import logging

from pydantic import BaseSettings

from .services.path import CHROME_USER_DATA_DIR


class Settings(BaseSettings):

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FILE_PATH: str | None = None

    VK_PAGE: str = 'https://vk.com'
    GOOGLE_OPTIONS_ARGUMENTS: list[str] = [
        f"--user-data-dir={CHROME_USER_DATA_DIR}",
        "--disable-blink-features",
        "--disable-blink-features=AutomationControlled",
        "ignore-certificate-errors",
        "--no-sandbox",
        "disable-notifications",
        "--disable-infobars",
        "--disable-extensions",
    ]


settings = Settings()
