"""
Roadmap utilities - compatibility module that wraps workflow plugins.

This module provides backward-compatible functions for roadmap operations
by calling the underlying workflow plugin implementations.
"""
import os
import re
import logging

logger = logging.getLogger("autometabuilder")


def is_mvp_reached() -> bool:
    """Check if the MVP section in ROADMAP.md is completed."""
    if not os.path.exists("ROADMAP.md"):
        return False
    
    with open("ROADMAP.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find the header line containing (MVP)
    header_match = re.search(r"^## .*?\(MVP\).*?$", content, re.MULTILINE | re.IGNORECASE)
    if not header_match:
        return False
    
    # Get the position of the header
    start_pos = header_match.end()
    
    # Find the next header starting from start_pos
    next_header_match = re.search(r"^## ", content[start_pos:], re.MULTILINE)
    if next_header_match:
        mvp_section = content[start_pos : start_pos + next_header_match.start()]
    else:
        mvp_section = content[start_pos:]
    
    # Check if there are any unchecked items [ ]
    if "[ ]" in mvp_section:
        return False
    
    # If there are checked items [x], and no unchecked items, we consider it reached
    if "[x]" in mvp_section:
        return True
        
    return False


def update_roadmap(content: str):
    """Update ROADMAP.md with new content."""
    with open("ROADMAP.md", "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("ROADMAP.md updated successfully.")
