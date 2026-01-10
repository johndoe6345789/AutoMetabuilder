from playwright.sync_api import Page, expect

from autometabuilder.metadata_loader import load_metadata
from .helpers import wait_for_nav


def test_choices_dropdowns_exist(page: Page, server: str):
    page.goto(server)
    wait_for_nav(page)
    page.click("[data-section='translations']")
    page.wait_for_selector("#translations.active")
    page.wait_for_timeout(1000)

    choices_elements = page.locator("#translations [data-choices]")
    count = choices_elements.count()
    assert count > 0, "No Choices.js elements found in translations section"

    choices_wrapper = page.locator("#translations div.choices[data-type='select-one']").first
    expect(choices_wrapper).to_be_visible()


def test_autocomplete_values_from_json(page: Page, server: str):
    metadata = load_metadata()

    page.goto(server)
    wait_for_nav(page)
    page.click("[data-section='translations']")
    page.wait_for_selector("#translations.active")
    page.wait_for_timeout(1000)

    choices_wrapper = page.locator("#translations div.choices[data-type='select-one']").first
    choices_wrapper.click()
    page.wait_for_timeout(500)

    dropdown_items = page.locator("#translations .choices__list--dropdown .choices__item")
    item_count = dropdown_items.count()
    available_languages = set(metadata["suggestions"]["languages"])
    existing_languages = set(metadata.get("messages", {}).keys())
    expected_count = len(available_languages - existing_languages)
    assert item_count >= expected_count, f"Expected at least {expected_count} language options, found {item_count}"

    remaining_languages = sorted(available_languages - existing_languages)
    assert remaining_languages, "No remaining language options available"
    sample_language = remaining_languages[0]
    expect(page.locator(f"#translations .choices__list--dropdown .choices__item[data-value='{sample_language}']")).to_be_attached()

    page.keyboard.press("Escape")

    wait_for_nav(page)
    page.click("[data-section='settings']")
    page.wait_for_selector("#settings.active")
    page.wait_for_timeout(500)

    settings_choices = page.locator("#settings div.choices[data-type='select-one']")
    assert settings_choices.count() > 0, "No Choices.js dropdowns found in settings section"
