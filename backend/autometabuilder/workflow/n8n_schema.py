"""N8N workflow schema types and validation."""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union


class N8NPosition:
    """Canvas position [x, y]."""
    
    @staticmethod
    def validate(value: Any) -> bool:
        return (
            isinstance(value, list) and 
            len(value) == 2 and 
            all(isinstance(v, (int, float)) for v in value)
        )


class N8NConnectionTarget:
    """Connection target specification."""
    
    @staticmethod
    def validate(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        return (
            "node" in value and isinstance(value["node"], str) and
            "type" in value and isinstance(value["type"], str) and
            "index" in value and isinstance(value["index"], int) and value["index"] >= 0
        )


class N8NNode:
    """N8N workflow node specification."""
    
    @staticmethod
    def validate(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        required = ["id", "name", "type", "typeVersion", "position"]
        if not all(key in value for key in required):
            return False
        if not isinstance(value["id"], str) or not value["id"]:
            return False
        if not isinstance(value["name"], str) or not value["name"]:
            return False
        if not isinstance(value["type"], str) or not value["type"]:
            return False
        if not isinstance(value["typeVersion"], (int, float)) or value["typeVersion"] < 1:
            return False
        if not N8NPosition.validate(value["position"]):
            return False
        return True


class N8NWorkflow:
    """N8N workflow specification."""
    
    @staticmethod
    def validate(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        required = ["name", "nodes", "connections"]
        if not all(key in value for key in required):
            return False
        if not isinstance(value["name"], str) or not value["name"]:
            return False
        if not isinstance(value["nodes"], list) or len(value["nodes"]) < 1:
            return False
        if not isinstance(value["connections"], dict):
            return False
        return all(N8NNode.validate(node) for node in value["nodes"])
