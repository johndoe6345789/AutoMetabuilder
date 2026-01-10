import re
from playwright.sync_api import Page, expect

from .helpers import t, wait_for_nav


def test_login_and_dashboard(page: Page, server: str):
    page.goto(server)
    expect(page.locator("#dashboard.active h1")).to_contain_text(t("ui.dashboard.title"))
    expect(page.locator(".amb-sidebar-footer")).to_contain_text("testuser")


def test_run_bot_mock(page: Page, server: str):
    page.goto(server)
    run_btn = page.locator("#run-btn")
    expect(run_btn).to_be_visible()
    status = page.locator("#status-indicator")
    expect(status).to_be_visible()
    run_btn.click()
    expect(page.locator("#dashboard")).to_be_attached()


def test_navigation_sections(page: Page, server: str):
    page.goto(server)
    expect(page.locator("#dashboard")).to_have_class(re.compile(r"active"))
    sections = ["workflow", "prompt", "settings", "translations"]
    for section in sections:
        wait_for_nav(page)
        page.click(f"[data-section='{section}']")
        page.wait_for_timeout(100)
        expect(page.locator(f"#{section}")).to_have_class(re.compile(r"active"))
        expect(page.locator("#dashboard")).not_to_have_class(re.compile(r"active"))


def test_theme_toggle(page: Page, server: str):
    page.goto(server)
    html = page.locator("html")
    initial_theme = html.get_attribute("data-theme")
    page.click("[data-theme-toggle]")
    page.wait_for_timeout(100)
    new_theme = html.get_attribute("data-theme")
    assert new_theme != initial_theme, f"Theme did not change from {initial_theme}"
    page.click("[data-theme-toggle]")
    page.wait_for_timeout(100)
    final_theme = html.get_attribute("data-theme")
    assert final_theme == initial_theme, f"Theme should return to {initial_theme}"
