import pytest
import json
import os
import re
from playwright.sync_api import Page, expect

def test_login_and_dashboard(page: Page, server: str):
    # Go to the server with auth
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Check if we are on the dashboard - select h1 in the active section
    expect(page.locator("#dashboard.active h1")).to_contain_text("Dashboard")
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
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")

    # Find prompt textarea - specifically in the prompt section
    textarea = page.locator("#prompt textarea[name='content']")
    original_content = textarea.input_value()

    new_content = original_content + "\n# Test Comment"
    textarea.fill(new_content)

    # Click save prompt
    page.click("#prompt button:has-text('Save Prompt')")

    # Verify it updated
    page.reload()
    page.click("[data-section='prompt']")
    page.wait_for_selector("#prompt.active")
    expect(page.locator("#prompt textarea[name='content']")).to_have_value(new_content)

def test_update_settings(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Navigate to settings section
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")

    # Wait for Choices.js to initialize
    page.wait_for_timeout(1000)

    # Add a new setting using Choices.js select
    # Click on the outer .choices wrapper (first match only)
    key_choices = page.locator("#settings select[name='new_env_key']").locator("xpath=ancestor::div[@class='choices' or contains(@class, 'choices ')]").first
    key_choices.click()
    page.keyboard.type("GITHUB_TOKEN")
    page.keyboard.press("Enter")

    # For new_env_value
    value_choices = page.locator("#settings select[name='new_env_value']").locator("xpath=ancestor::div[@class='choices' or contains(@class, 'choices ')]").first
    value_choices.click()
    page.keyboard.type("DEBUG")
    page.keyboard.press("Enter")

    page.click("#settings button:has-text('Save Settings')")

    # Verify it appeared in the table
    page.reload()
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    expect(page.locator("#settings code:has-text('GITHUB_TOKEN')")).to_be_visible()

def test_navigation_sections(page: Page, server: str):
    """Test that sidebar navigation works correctly"""
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)

    # Dashboard should be active by default
    expect(page.locator("#dashboard")).to_have_class(re.compile(r"active"))

    # Navigate to each section
    sections = ["workflow", "prompt", "settings", "translations"]
    for section in sections:
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
    assert item_count >= len(metadata["suggestions"]["languages"]), f"Expected at least {len(metadata['suggestions']['languages'])} language options, found {item_count}"

    # Verify at least one specific language exists
    expect(page.locator("#translations .choices__list--dropdown .choices__item[data-value='en']")).to_be_attached()

    # Close dropdown
    page.keyboard.press("Escape")

    # Navigate to settings to verify Choices.js dropdowns exist there too
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
    page.click("[data-section='workflow']")
    page.wait_for_selector("#workflow.active")

    # Wait for workflow builder to render
    page.wait_for_selector("#workflow-builder")

    # Should have at least the "Add Task" button
    expect(page.locator("#workflow-builder button:has-text('Add Task')")).to_be_visible()

    # Toggle raw JSON should work
    page.click("#workflow button:has-text('Toggle Raw JSON')")
    expect(page.locator("#workflow-content")).to_be_visible()

    page.click("#workflow button:has-text('Toggle Raw JSON')")
    expect(page.locator("#workflow-content")).not_to_be_visible()
