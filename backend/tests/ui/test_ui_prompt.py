from playwright.sync_api import Page, expect

from .helpers import t, wait_for_nav


def test_update_prompt(page: Page, server: str):
    page.goto(server)
    wait_for_nav(page)
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")

    system_prompt = page.locator("#prompt textarea[name='system_content']")
    user_prompt = page.locator("#prompt textarea[name='user_content']")
    system_prompt.fill("Test system prompt")
    user_prompt.fill("Test user prompt")

    with page.expect_navigation():
        page.click(f"#prompt button:has-text('{t('ui.prompt.save')}')")

    wait_for_nav(page)
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")
    expect(page.locator("#prompt textarea[name='system_content']")).to_have_value("Test system prompt")
    expect(page.locator("#prompt textarea[name='user_content']")).to_have_value("Test user prompt")
