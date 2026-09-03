from flask import Flask, render_template
from app.chat.routes import chat_bp

flask_app = Flask(__name__)

flask_app.register_blueprint(chat_bp)

@flask_app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    flask_app.run(debug=True)