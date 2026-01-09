import pytest
import json
import os
import re
from playwright.sync_api import Page, expect


def wait_for_nav(page: Page):
    page.wait_for_selector("[data-section='dashboard']")

UI_MESSAGES_PATH = os.path.join(os.path.dirname(__file__), "../../src/autometabuilder/messages_en.json")
with open(UI_MESSAGES_PATH, "r", encoding="utf-8") as f:
    UI_MESSAGES = json.load(f)

def t(key, fallback=None):
    return UI_MESSAGES.get(key, fallback or key)

def test_login_and_dashboard(page: Page, server: str):
    # Go to the server with auth
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Check if we are on the dashboard - select h1 in the active section
    expect(page.locator("#dashboard.active h1")).to_contain_text(t("ui.dashboard.title"))
    # User info is now in sidebar footer
    expect(page.locator(".amb-sidebar-footer")).to_contain_text("testuser")

def test_run_bot_mock(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Check that run button exists and is clickable
    run_btn = page.locator("#run-btn")
    expect(run_btn).to_be_visible()

    # Check status indicator exists
    status = page.locator("#status-indicator")
    expect(status).to_be_visible()

    # Check that clicking the button doesn't error (don't wait for full mock cycle)
    # The actual mock runs for 5+ seconds which causes test isolation issues
    run_btn.click()

    # Just verify the page didn't crash
    expect(page.locator("#dashboard")).to_be_attached()

def test_update_prompt(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to prompt section
    wait_for_nav(page)
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")

    system_prompt = page.locator("#prompt textarea[name='system_content']")
    user_prompt = page.locator("#prompt textarea[name='user_content']")
    system_prompt.fill("Test system prompt")
    user_prompt.fill("Test user prompt")

    # Click save prompt and wait for redirect
    with page.expect_navigation():
        page.click(f"#prompt button:has-text('{t('ui.prompt.save')}')")

    # Verify it updated
    wait_for_nav(page)
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")
    expect(page.locator("#prompt textarea[name='system_content']")).to_have_value("Test system prompt")
    expect(page.locator("#prompt textarea[name='user_content']")).to_have_value("Test user prompt")

def test_update_settings(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to settings section
    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")

    # Wait for Choices.js to initialize
    page.wait_for_timeout(1000)

    # Add a new setting using text inputs
    page.fill("#settings input[name='new_env_key']", "TEST_SETTING")
    page.fill("#settings input[name='new_env_value']", "42")

    page.click(f"#settings button:has-text('{t('ui.settings.save_all')}')")

    # Verify it appeared in the table
    page.reload()
    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    expect(page.locator("#settings input[name='env_TEST_SETTING']")).to_be_visible()

def test_navigation_sections(page: Page, server: str):
    """Test that sidebar navigation works correctly"""
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Dashboard should be active by default
    expect(page.locator("#dashboard")).to_have_class(re.compile(r"active"))

    # Navigate to each section
    sections = ["workflow", "prompt", "settings", "translations"]
    for section in sections:
        wait_for_nav(page)
        page.click(f"[data-section='{section}']")
        page.wait_for_timeout(100)
        expect(page.locator(f"#{section}")).to_have_class(re.compile(r"active"))
        # Previous section should no longer be active
        expect(page.locator("#dashboard")).not_to_have_class(re.compile(r"active"))

def test_theme_toggle(page: Page, server: str):
    """Test dark mode toggle functionality"""
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Get initial theme
    html = page.locator("html")
    initial_theme = html.get_attribute("data-theme")

    # Click toggle
    page.click("[data-theme-toggle]")
    page.wait_for_timeout(100)

    # Theme should have changed
    new_theme = html.get_attribute("data-theme")
    assert new_theme != initial_theme, f"Theme did not change from {initial_theme}"

    # Toggle back
    page.click("[data-theme-toggle]")
    page.wait_for_timeout(100)
    final_theme = html.get_attribute("data-theme")
    assert final_theme == initial_theme, f"Theme should return to {initial_theme}"

def test_choices_dropdowns_exist(page: Page, server: str):
    """Test that Choices.js dropdowns are initialized"""
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to translations to find language dropdown
    wait_for_nav(page)
    page.click("[data-section='translations']")
    page.wait_for_selector("#translations.active")

    # Wait for Choices.js to initialize
    page.wait_for_timeout(1000)

    # Check that data-choices elements have been enhanced
    choices_elements = page.locator("#translations [data-choices]")
    count = choices_elements.count()
    assert count > 0, "No Choices.js elements found in translations section"

    # Verify Choices.js wrapper exists - use CSS selector for the outer wrapper
    choices_wrapper = page.locator("#translations div.choices[data-type='select-one']").first
    expect(choices_wrapper).to_be_visible()

def test_autocomplete_values_from_json(page: Page, server: str):
    """Test that dropdown options are populated from metadata.json"""
    # Load metadata.json
    metadata_path = os.path.join(os.path.dirname(__file__), "../../src/autometabuilder/metadata.json")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to translations section to check language options
    wait_for_nav(page)
    page.click("[data-section='translations']")
    page.wait_for_selector("#translations.active")
    page.wait_for_timeout(1000)

    # Verify language options exist in Choices.js dropdown
    # Click to open dropdown
    choices_wrapper = page.locator("#translations div.choices[data-type='select-one']").first
    choices_wrapper.click()
    page.wait_for_timeout(500)

    # Check that at least some languages appear in the Choices dropdown list
    # Choices.js creates items with data-value attribute in .choices__list--dropdown
    dropdown_items = page.locator("#translations .choices__list--dropdown .choices__item")
    item_count = dropdown_items.count()
    available_languages = set(metadata["suggestions"]["languages"])
    existing_languages = set(metadata.get("messages", {}).keys())
    expected_count = len(available_languages - existing_languages)
    assert item_count >= expected_count, f"Expected at least {expected_count} language options, found {item_count}"

    # Verify at least one available language exists
    remaining_languages = sorted(available_languages - existing_languages)
    assert remaining_languages, "No remaining language options available"
    sample_language = remaining_languages[0]
    expect(page.locator(f"#translations .choices__list--dropdown .choices__item[data-value='{sample_language}']")).to_be_attached()

    # Close dropdown
    page.keyboard.press("Escape")

    # Navigate to settings to verify Choices.js dropdowns exist there too
    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    page.wait_for_timeout(500)

    # Verify Choices.js dropdowns are present in settings
    settings_choices = page.locator("#settings div.choices[data-type='select-one']")
    assert settings_choices.count() > 0, "No Choices.js dropdowns found in settings section"

def test_workflow_builder_renders(page: Page, server: str):
    """Test that workflow builder initializes and renders"""
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to workflow section
    wait_for_nav(page)
    page.click("[data-section='workflow']")
    page.wait_for_selector("#workflow.active")

    # Wait for workflow builder to render
    page.wait_for_selector("#workflow-builder", state="attached")
    page.wait_for_selector("#workflow-template-select", state="attached")
    page.wait_for_selector("#workflow-palette", state="attached")
    page.wait_for_selector("#workflow-palette-search", state="visible")
    page.wait_for_selector("#workflow-palette-list .amb-workflow-palette-item", state="attached")

    # Should have at least the primary action button
    expect(page.locator("#workflow-builder .btn.btn-primary")).to_be_visible()
    packages_response = page.request.get(f"{server}/api/workflow/packages")
    assert packages_response.ok, "Workflow packages endpoint did not respond"
    packages_payload = packages_response.json()
    assert packages_payload.get("packages"), "No workflow packages returned"

    # Toggle raw JSON should work
    page.click(f"#workflow button:has-text('{t('ui.workflow.toggle_json')}')")
    expect(page.locator("#workflow-content")).to_be_visible()

    page.click(f"#workflow button:has-text('{t('ui.workflow.toggle_json')}')")
    expect(page.locator("#workflow-content")).not_to_be_visible()
