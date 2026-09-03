from flask import Blueprint, request, jsonify

from app.chat.ai_parser import extract_filters
from app.database.query import search_inventory
from app.database.analytics import get_low_stock_items
from app.chat.answer_builder import build_answer, build_general_answer
from app.database.chat_history import save_chat
from app.database.value_matcher import normalize_filters

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    filters = extract_filters(user_message)
    filters = normalize_filters(filters)

    intent = filters.get("intent", "stock")

    if intent == "general":
        answer = build_general_answer(user_message)
        save_chat(user_message, answer)
        return jsonify({"reply": answer, "rows": []})

    if intent == "low_stock":

        data = get_low_stock_items()

        answer = build_answer(user_message, data)

        save_chat(user_message, answer)

        return jsonify({
            "reply": answer,
            "rows": data
        })

    data = search_inventory(
        style=filters.get("style"),
        colour=filters.get("colour"),
        size=filters.get("size"),
        distributor=filters.get("distributor")
    )

    answer = build_answer(user_message, data)

    save_chat(user_message, answer)

    return jsonify({
        "reply": answer,
        "rows": data
    })