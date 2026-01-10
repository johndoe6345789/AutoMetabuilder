import os
import unittest

from autometabuilder.roadmap_utils import is_mvp_reached, update_roadmap


class TestRoadmap(unittest.TestCase):
    def setUp(self):
        self.original_content = None
        if os.path.exists("ROADMAP.md"):
            with open("ROADMAP.md", "r", encoding="utf-8") as f:
                self.original_content = f.read()

    def tearDown(self):
        if self.original_content is not None:
            with open("ROADMAP.md", "w", encoding="utf-8") as f:
                f.write(self.original_content)
        elif os.path.exists("ROADMAP.md"):
            os.remove("ROADMAP.md")

    def assert_mvp(self, content: str, expected: bool) -> None:
        update_roadmap(content)
        self.assertEqual(is_mvp_reached(), expected)

    def test_is_mvp_reached_cases(self):
        cases = [
            (
                "mvp_all_checked",
                "# Roadmap\n## Phase 3: Advanced Automation (MVP)\n- [x] Item 1\n- [x] Item 2\n",
                True,
            ),
            (
                "mvp_unchecked",
                "# Roadmap\n## Phase 3: Advanced Automation (MVP)\n- [x] Item 1\n- [ ] Item 2\n",
                False,
            ),
            (
                "mvp_no_items",
                "# Roadmap\n## Phase 3: Advanced Automation (MVP)\nNo items here\n",
                False,
            ),
            (
                "mvp_case_insensitive",
                "# Roadmap\n## Phase 3: (mvp)\n- [x] Done\n",
                True,
            ),
            (
                "mvp_with_other_sections",
                "# Roadmap\n## Phase 1\n- [x] Done\n\n## Phase 3 (MVP)\n- [ ] Not done\n\n## Phase 4\n- [x] Done\n",
                False,
            ),
            (
                "mvp_no_section",
                "# Roadmap\n## Phase 1\n- [x] Done\n",
                False,
            ),
            (
                "mvp_multiple_markers_first_true",
                "# Roadmap\n## Phase 3 (MVP)\n- [x] Done\n\n## Phase 5 (MVP)\n- [ ] Not done\n",
                True,
            ),
            (
                "mvp_not_in_header",
                "# Roadmap\n## Phase 1\nThis is not (MVP) but it mentions it.\n- [x] Done\n",
                False,
            ),
        ]

        for name, content, expected in cases:
            with self.subTest(name=name):
                self.assert_mvp(content, expected)
