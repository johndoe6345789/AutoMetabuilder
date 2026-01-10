from playwright.sync_api import Page, expect

from .helpers import t, wait_for_nav


def test_workflow_builder_renders(page: Page, server: str):
    page.goto(server)
    wait_for_nav(page)
    page.click("[data-section='workflow']")
    page.wait_for_selector("#workflow.active")

    page.wait_for_selector("#workflow-builder", state="attached")
    page.wait_for_selector("#workflow-template-select", state="attached")
    page.wait_for_selector("#workflow-palette", state="attached")
    page.wait_for_selector("#workflow-palette-search", state="visible")
    page.wait_for_selector("#workflow-palette-list .amb-workflow-palette-item", state="attached")

    expect(page.locator("#workflow-builder .btn.btn-primary")).to_be_visible()
    packages_response = page.request.get(f"{server}/api/workflow/packages")
    assert packages_response.ok, "Workflow packages endpoint did not respond"
    packages_payload = packages_response.json()
    assert packages_payload.get("packages"), "No workflow packages returned"

    page.click(f"#workflow button:has-text('{t('ui.workflow.toggle_json')}')")
    expect(page.locator("#workflow-content")).to_be_visible()

    page.click(f"#workflow button:has-text('{t('ui.workflow.toggle_json')}')")
    expect(page.locator("#workflow-content")).not_to_be_visible()
