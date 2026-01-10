import os
import unittest

from autometabuilder.prompt_loader import load_prompt_yaml

class TestMain(unittest.TestCase):
    def test_load_prompt_yaml(self):
        # This test assumes prompt.yml exists in the root
        if os.path.exists("prompt.yml"):
            config = load_prompt_yaml()
            self.assertIsInstance(config, dict)
            self.assertIn("messages", config)

if __name__ == '__main__':
    unittest.main()
