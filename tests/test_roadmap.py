import os
import unittest
from src.autometabuilder.roadmap_utils import is_mvp_reached, update_roadmap

class TestRoadmap(unittest.TestCase):
    def setUp(self):
        # Backup original ROADMAP.md if it exists
        self.original_content = None
        if os.path.exists("ROADMAP.md"):
            with open("ROADMAP.md", "r", encoding="utf-8") as f:
                self.original_content = f.read()

    def tearDown(self):
        # Restore original ROADMAP.md
        if self.original_content is not None:
            with open("ROADMAP.md", "w", encoding="utf-8") as f:
                f.write(self.original_content)
        elif os.path.exists("ROADMAP.md"):
            os.remove("ROADMAP.md")

    def test_is_mvp_reached_true(self):
        content = """
# Roadmap
## Phase 3: Advanced Automation (MVP)
- [x] Item 1
- [x] Item 2
"""
        update_roadmap(content)
        self.assertTrue(is_mvp_reached())

    def test_is_mvp_reached_false_unchecked(self):
        content = """
# Roadmap
## Phase 3: Advanced Automation (MVP)
- [x] Item 1
- [ ] Item 2
"""
        update_roadmap(content)
        self.assertFalse(is_mvp_reached())

    def test_is_mvp_reached_false_no_items(self):
        content = """
# Roadmap
## Phase 3: Advanced Automation (MVP)
No items here
"""
        update_roadmap(content)
        self.assertFalse(is_mvp_reached())

    def test_is_mvp_reached_case_insensitive(self):
        content = """
# Roadmap
## Phase 3: (mvp)
- [x] Done
"""
        update_roadmap(content)
        self.assertTrue(is_mvp_reached())

    def test_is_mvp_reached_with_other_sections(self):
        content = """
# Roadmap
## Phase 1
- [x] Done

## Phase 3 (MVP)
- [ ] Not done

## Phase 4
- [x] Done
"""
        update_roadmap(content)
        self.assertFalse(is_mvp_reached())

    def test_is_mvp_reached_no_section(self):
        content = """
# Roadmap
## Phase 1
- [x] Done
"""
        update_roadmap(content)
        self.assertFalse(is_mvp_reached())

    def test_is_mvp_reached_multiple_mvp_markers(self):
        # Should probably pick the first one or behave consistently
        content = """
# Roadmap
## Phase 3 (MVP)
- [x] Done

## Phase 5 (MVP)
- [ ] Not done
"""
        update_roadmap(content)
        # Current logic picks the first match
        self.assertTrue(is_mvp_reached())

    def test_is_mvp_reached_not_in_header(self):
        content = """
# Roadmap
## Phase 1
This is not (MVP) but it mentions it.
- [x] Done
"""
        update_roadmap(content)
        # Should be False because (MVP) is not in a header
        self.assertFalse(is_mvp_reached())
