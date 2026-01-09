import os
import re
import logging

logger = logging.getLogger("autometabuilder")

def update_roadmap(content: str):
    """Update ROADMAP.md with new content."""
    with open("ROADMAP.md", "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("ROADMAP.md updated successfully.")


def is_mvp_reached() -> bool:
    """Check if the MVP section in ROADMAP.md is completed."""
    if not os.path.exists("ROADMAP.md"):
        return False
    
    with open("ROADMAP.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find the MVP section
    mvp_match = re.search(r"## .*?\(MVP\)(.*?)##", content, re.DOTALL | re.IGNORECASE)
    if not mvp_match:
        # Try finding it if it's the last section
        mvp_match = re.search(r"## .*?\(MVP\)(.*)", content, re.DOTALL | re.IGNORECASE)
    
    if not mvp_match:
        return False
    
    mvp_section = mvp_match.group(1)
    # Check if there are any unchecked items [ ]
    if "[ ]" in mvp_section:
        return False
    
    # If there are checked items [x], and no unchecked items, we consider it reached
    if "[x]" in mvp_section:
        return True
        
    return False
