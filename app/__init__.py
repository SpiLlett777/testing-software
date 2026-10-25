import math
import os
import re
import secrets

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from .calculator import Calculator


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return render_template("index.html", active="home")

    @app.get("/calculator")
    def calculator():
        return render_template("calculator.html", active="calculator")

    @app.post("/api/calculate")
    def calculate():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify(error="Ожидается JSON-объект."), 400

        operation = data.get("operation")
        operations = {name: getattr(Calculator, name) for name in ("add", "subtract", "multiply", "divide")}

        if not isinstance(operation, str) or operation not in operations:
            return jsonify(error="Выберите арифметическую операцию."), 400
        try:
            values = []

            for key in ("a", "b"):
                raw = data.get(key)

                if isinstance(raw, bool) or not isinstance(raw, (str, int, float)):
                    raise ValueError

                value = float(raw.replace(",", ".") if isinstance(raw, str) else raw)

                if not math.isfinite(value) or abs(value) > 1e12:
                    raise ValueError

                values.append(value)

            result = operations[operation](*values)

            if not math.isfinite(result):
                return jsonify(error="Результат выходит за допустимый диапазон."), 400

        except (ValueError, TypeError, OverflowError):
            return jsonify(error="Введите два конечных числа от −10¹² до 10¹²."), 400
        except ZeroDivisionError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(result=result, display=format(result, ".12g"))

    @app.get("/todo")
    def todo():
        return render_template("todo.html", active="todo", buggy=request.args.get("mode") == "buggy")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None

        if request.method == "POST":
            if request.form.get("username") == "student" and request.form.get("password") == "Test123!":
                session.clear()
                session["user"] = "student"
                return redirect(url_for("account"))
            error = "Неверный логин или пароль."

        return render_template("login.html", active="login", error=error), 401 if error else 200

    @app.get("/account")
    def account():
        if "user" not in session:
            return redirect(url_for("login"))
        return render_template("account.html", active="login")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        values = {key: request.form.get(key, "").strip() for key in ("name", "email", "message")}
        errors = {}
        success = False

        if request.method == "POST":
            if not 2 <= len(values["name"]) <= 60:
                errors["name"] = "Имя должно содержать от 2 до 60 символов."

            if len(values["email"]) > 120 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", values["email"]):
                errors["email"] = "Введите корректный email."

            if not 10 <= len(values["message"]) <= 1000:
                errors["message"] = "Сообщение должно содержать от 10 до 1000 символов."

            success = not errors

        return render_template("contact.html", active="contact", values=values, errors=errors,
                               success=success), 422 if errors else 200

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", service="testing-lab", storage="none")

    return app
