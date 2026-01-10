import unittest
import os
import json
from autometabuilder import load_messages

class TestMetadata(unittest.TestCase):
    def test_metadata_exists(self):
        metadata_path = os.path.join("..", "autometabuilder", "metadata.json")
        self.assertTrue(os.path.exists(metadata_path))
        
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            self.assertIn("tools_path", metadata)
            self.assertIn("workflow_path", metadata)
            self.assertIn("messages", metadata)

    def test_load_messages_with_metadata(self):
        # Test default language (en)
        messages = load_messages()
        self.assertIsInstance(messages, dict)
        self.assertIn("sdlc_context_label", messages)

if __name__ == '__main__':
    unittest.main()
