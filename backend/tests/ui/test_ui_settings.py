from playwright.sync_api import Page, expect

from .helpers import t, wait_for_nav


def test_update_settings(page: Page, server: str):
    page.goto(server)
    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    page.wait_for_timeout(1000)

    page.fill("#settings input[name='new_env_key']", "TEST_SETTING")
    page.fill("#settings input[name='new_env_value']", "42")

    page.click(f"#settings button:has-text('{t('ui.settings.save_all')}')")

    page.reload()
    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    expect(page.locator("#settings input[name='env_TEST_SETTING']")).to_be_visible()
