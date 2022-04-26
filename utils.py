import os
import re

from flask import Flask, request


def check_hangul(text):
    text = text.strip()
    return re.compile(r"[ㄱ-ㅣ가-힇]").search(text) is not None


def process_access_token(auth_handler):
    print(f" * URL: \n   {auth_handler.get_authorization_url()}")

    app = Flask(__name__)

    @app.route("/")
    def root():
        params = request.args.to_dict()
        auth_handler.get_access_token(params["oauth_verifier"])
        request.environ.get("werkzeug.server.shutdown")()

    app.run()
    os.system("cls")
