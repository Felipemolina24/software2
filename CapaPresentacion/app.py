from flask import Flask, render_template, request, jsonify
from agents.langchain_executor import invoke
from CapaDatos.models import Chat

app = Flask(__name__)
chat = Chat()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["message"]
    response = invoke(chat_history=chat, query=user_input)
    return jsonify({"message": response})


if __name__ == "__main__":
    app.run(debug=True)
