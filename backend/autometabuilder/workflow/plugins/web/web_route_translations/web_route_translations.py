"""Workflow plugin: translation API routes blueprint."""
from flask import Blueprint, jsonify, request
from autometabuilder.utils import load_metadata


def run(runtime, _inputs):
    """Create and return the translations routes blueprint."""
    translations_bp = Blueprint("translations", __name__)
    
    @translations_bp.route("/api/translation-options")
    def api_translation_options():
        from autometabuilder.data import list_translations
        return jsonify({"translations": list_translations()}), 200
    
    @translations_bp.route("/api/translations", methods=["POST"])
    def api_create_translation():
        from autometabuilder.data import create_translation
        payload = request.get_json(force=True)
        lang = payload.get("lang")
        if not lang:
            return jsonify({"error": "lang required"}), 400
        ok = create_translation(lang)
        return jsonify({"created": ok}), (201 if ok else 400)
    
    @translations_bp.route("/api/translations/<lang>", methods=["GET"])
    def api_get_translation(lang):
        from autometabuilder.data import load_translation
        if lang not in load_metadata().get("messages", {}):
            return jsonify({"error": "translation not found"}), 404
        return jsonify({"lang": lang, "content": load_translation(lang)}), 200
    
    @translations_bp.route("/api/translations/<lang>", methods=["PUT"])
    def api_update_translation(lang):
        from autometabuilder.data import update_translation
        payload = request.get_json(force=True)
        updated = update_translation(lang, payload)
        if not updated:
            return jsonify({"error": "unable to update"}), 400
        return jsonify({"status": "saved"}), 200
    
    @translations_bp.route("/api/translations/<lang>", methods=["DELETE"])
    def api_delete_translation(lang):
        from autometabuilder.data import delete_translation
        deleted = delete_translation(lang)
        if not deleted:
            return jsonify({"error": "cannot delete"}), 400
        return jsonify({"deleted": True}), 200
    
    # Store in runtime context and return
    runtime.context["translations_bp"] = translations_bp
    return {"result": translations_bp, "blueprint_path": "translations_bp"}
