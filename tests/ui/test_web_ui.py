import pytest
from playwright.sync_api import Page, expect

def test_login_and_dashboard(page: Page, server: str):
    # Go to the server
    page.goto(server)
    
    # We should be prompted for basic auth
    # Playwright handles basic auth via context or by encoding it in the URL
    # or we can use the page.authenticate method
    
    # Alternative: use URL with credentials
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)
    
    # Check if we are on the dashboard
    expect(page.locator("h1")).to_contain_text("AutoMetabuilder Dashboard")
    expect(page.locator("text=Logged in as: testuser")).to_be_visible()

def test_run_bot_mock(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)
    
    # Click run button
    page.click("button:has-text('Run Bot')")
    
    # Status should change to "Bot Running..."
    expect(page.locator(".badge.bg-warning")).to_contain_text("Bot Running")
    
    # Wait for it to finish (mock takes 5 seconds)
    page.wait_for_timeout(6000)
    
    # Refresh
    page.reload()
    expect(page.locator(".badge.bg-success")).to_contain_text("Idle")

def test_update_prompt(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)
    
    # Find prompt textarea
    textarea = page.locator("textarea[name='content']").first
    original_content = textarea.input_value()
    
    new_content = original_content + "\n# Test Comment"
    textarea.fill(new_content)
    
    # Click update prompt
    page.click("button:has-text('Save Prompt')")
    
    # Verify it updated
    page.reload()
    expect(page.locator("textarea[name='content']").first).to_have_value(new_content)

def test_update_settings(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)
    
    # Add a new setting
    page.fill("input[name='new_env_key']", "TEST_SETTING")
    page.fill("input[name='new_env_value']", "test_value")
    
    page.click("button:has-text('Save Settings')")
    
    # Verify it appeared in the table
    page.reload()
    expect(page.locator("input[name='env_TEST_SETTING']")).to_have_value("test_value")

def test_all_text_inputs_have_autocomplete(page: Page, server: str):
    auth_url = server.replace("http://", "http://testuser:testpass@")
    page.goto(auth_url)
    
    # Wait for the workflow builder to render
    page.wait_for_selector("#workflow-builder")
    
    # Select all text inputs
    inputs = page.locator("input[type='text']")
    
    count = inputs.count()
    assert count > 0, "No text inputs found on the page"
    
    for i in range(count):
        input_element = inputs.nth(i)
        # Check if the 'list' attribute is present and not empty
        list_attr = input_element.get_attribute("list")
        input_name = input_element.get_attribute("name") or input_element.get_attribute("placeholder") or f"index {i}"
        assert list_attr, f"Input '{input_name}' does not have a 'list' attribute for autocomplete"
        
        # Check if the corresponding datalist exists
        datalist = page.locator(f"datalist#{list_attr}")
        expect(datalist).to_be_attached(), f"Datalist '{list_attr}' for input '{input_name}' is missing"
