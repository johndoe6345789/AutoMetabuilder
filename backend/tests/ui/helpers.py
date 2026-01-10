from playwright.sync_api import Page

from autometabuilder import load_messages

UI_MESSAGES = load_messages()


def wait_for_nav(page: Page) -> None:
    page.wait_for_selector("[data-section='dashboard']")


def t(key: str, fallback: str | None = None) -> str:
    return UI_MESSAGES.get(key, fallback or key)
