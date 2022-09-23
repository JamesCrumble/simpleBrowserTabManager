from pydantic import BaseSettings


class Settings(BaseSettings):

    GOOGLE_OPTIONS_ARGUMENTS: list[str] = [
        "--disable-blink-features",
        "--disable-blink-features=AutomationControlled",
        "ignore-certificate-errors",
        "--no-sandbox",
        "disable-notifications",
        "--disable-infobars",
        "--disable-extensions"
    ]


settings = Settings()
