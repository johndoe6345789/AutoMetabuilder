"""Translation management routes."""
from __future__ import annotations

from flask import Blueprint, request

from autometabuilder.data import create_translation, delete_translation, load_metadata, load_translation, list_translations, update_translation

translations_bp = Blueprint("translations", __name__)


@translations_bp.route("/api/translation-options")
def api_translation_options() -> tuple[dict[str, dict[str, str]], int]:
    return {"translations": list_translations()}, 200


@translations_bp.route("/api/translations", methods=["POST"])
def api_create_translation() -> tuple[dict[str, str], int]:
    payload = request.get_json(force=True)
    lang = payload.get("lang")
    if not lang:
        return {"error": "lang required"}, 400
    ok = create_translation(lang)
    return ({"created": ok}, 201 if ok else 400)


@translations_bp.route("/api/translations/<lang>", methods=["GET"])
def api_get_translation(lang: str) -> tuple[dict[str, object], int]:
    if lang not in load_metadata().get("messages", {}):
        return {"error": "translation not found"}, 404
    return {"lang": lang, "content": load_translation(lang)}, 200


@translations_bp.route("/api/translations/<lang>", methods=["PUT"])
def api_update_translation(lang: str) -> tuple[dict[str, str], int]:
    payload = request.get_json(force=True)
    updated = update_translation(lang, payload)
    if not updated:
        return {"error": "unable to update"}, 400
    return {"status": "saved"}, 200


@translations_bp.route("/api/translations/<lang>", methods=["DELETE"])
def api_delete_translation(lang: str) -> tuple[dict[str, str], int]:
    deleted = delete_translation(lang)
    if not deleted:
        return {"error": "cannot delete"}, 400
    return {"deleted": True}, 200
