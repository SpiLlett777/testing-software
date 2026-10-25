# Лабораторная работа 3. Первый Selenium-тест

Цель: настроить Python, pip, selenium, webdriver-manager и pytest; открыть/закрыть браузер и проверить вход в
собственный стенд.

Установка и команды запуска — в README. `scripts/browser_smoke.py` создает Chrome, открывает `/login`, выводит адрес и
заголовок, гарантированно вызывает quit в finally. `scripts/browser.py` использует ChromeDriverManager и хранит драйвер
в игнорируемом каталоге tools/bin.

Основной тест: `tests/ui/test_forms.py::test_valid_login_and_logout`. Вводит student / Test123!, проверяет Logout и
сообщение успеха, выполняет выход и проверяет закрытие защищенной страницы. Дополнительный негативный сценарий проверяет
неправильный пароль. Изолированная сессия браузера на каждый тест исключает зависимость от предыдущего входа.

## Анализ селекторов

| Элемент      | Селектор                   | Причина стабильности                              |
|--------------|----------------------------|---------------------------------------------------|
| Логин        | id=username, name=username | Уникальный атрибут, не зависит от текста и стилей |
| Пароль       | id=password, name=password | Явно задан приложением                            |
| Кнопка входа | id=login-submit            | Не зависит от языка кнопки                        |
| Ошибка       | id=login-error             | Появляется при неверном вводе                     |
| Успех        | id=login-success           | Однозначный признак успешного входа               |
| Выход        | id=logout                  | Требуемый заданием признак авторизации            |

Не использовать абсолютный XPath по вложенности и классы оформления. Для динамически появляющихся элементов применен
WebDriverWait. Результаты реальных запусков и версии — в STATUS и artifacts; ручной анализ селекторов выполнен по
исходному HTML, а существование проверяется UI-тестами.

## Общий статус выполнения на момент сборки

# Статус на 18.09.2026

После просьбы пользователя оставить прогоны ему новые тесты не запускались. Ниже зафиксированы только уже полученные
результаты.

## Готово

- Собственный веб-стенд без БД: калькулятор, Todo (исправный и намеренно дефектный), логин/Logout, контактная форма,
  health API.
- Тест-план, чек-листы, 10 тест-кейсов калькулятора, 3 баг-репорта, анализ селекторов, матрица решений.
- Unit/серверные, Selenium Page Object и requests-тесты; Postman-коллекция с окружением; k6-скрипт; GitHub Actions YAML.
- Инструкции запуска и сборщик Markdown-отчетов с полными листингами.

## Фактические запуски

| Набор                          | Результат                                                                                                                                              | Доказательство                                                |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| Calculator: чистые unit-тесты  | 31 passed                                                                                                                                              | artifacts/lab06/unit.xml                                      |
| Серверные проверки             | 44 passed                                                                                                                                              | artifacts/lab06/unit.xml                                      |
| Selenium Chrome                | 14 passed; включает 3 проверки воспроизводимости намеренных дефектов и 2 проверки адаптивной компоновки                                                | artifacts/ui/results.xml, скриншоты artifacts/ui              |
| Публичное API, Python          | 3 passed                                                                                                                                               | artifacts/lab05/python-api.xml                                |
| Postman-коллекция через Newman | Первый прогон: 3 запроса с ожидаемыми статусами, 3 ошибки JS из-за имени data; переменная переименована в responseBody, повторный запуск не выполнялся | artifacts/lab05/newman.json содержит результат ДО исправления |
| k6, 10 VUs × 30s               | 2960 запросов, 98.47 req/s, среднее 1.06 мс, p95 2.14 мс, 0% HTTP-ошибок, 5920/5920 успешных проверок                                                  | artifacts/lab08/10vu.json                                     |
| k6, 50 VUs × 10s               | Не запускался                                                                                                                                          | Скрипт и команда готовы                                       |

UI запуск выполнен на Chrome 153.0.8010.48 / ChromeDriver 153.0.8010.52. Окружение: Windows 10, Python 3.13.7;
подробности в artifacts/environment.json. Визуально просмотрен снимок главной страницы на ширине 1440; автоматическая
проверка переполнения выполнена на 390 и 1440 для пяти страниц. Это не полноценный аудит доступности и не мобильная ЛР

7.

Первоначальные попытки скачивания драйвера блокировались сетевыми ограничениями; после загрузки из официального
источника весь UI-набор прошел. В API-прогоне был warning записи pytest cache, который не повлиял на проверки.
Нагрузочный прогон выполнялся одновременно с частью служебных операций на той же машине; это нужно учитывать при
интерпретации малых задержек.

## Остается выполнить для сдачи

- Ручной прогон чек-листов и исследовательская сессия ЛР 2; заполнение фактических результатов. Автотесты не выданы за
  ручную работу.
- Проверка исправленной коллекции, запуск через Postman Collection Runner и сохранение результатов.
- Второй профиль k6 и сравнение двух результатов (`python -m scripts.summarize_load`).
- Публикация публичного GitHub-репозитория и подтверждение успешного GitHub Actions run.
- Титульные листы и оформление отчетов по требованиям преподавателя.
- ЛР 7 — мобильное приложение — вне текущего веб-этапа.

Дополнительная утилита Newman использует зависимости, для которых npm сообщил 19 уязвимостей даже в установленной 6.2.2.
Она не подключена к веб-приложению и нужна только для необязательного CLI-прогона коллекции. Основной путь ЛР 5 — импорт
коллекции в Postman. Автоматические несовместимые обновления зависимостей не применялись.

## Приложение. Листинги исходного кода

### app/ __init__.py

SHA-256: `0b52ae19421ac3e4211c9725a45245f1c82bd41f837656798ad0c9de73eaf363`

```python
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
        return render_template("contact.html", active="contact", values=values, errors=errors, success=success), 422 if errors else 200

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", service="testing-lab", storage="none")

    return app

```

### app/calculator.py

SHA-256: `b40683fd2600f7c1a00086f720c2caf33fa16e9fe6b859fe428c5e70c269f6f9`

```python
"""Pure business logic shared by the web calculator and unit tests."""
import math


class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль запрещено.")
        return a / b

    @staticmethod
    def is_prime_number(n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Ожидается целое число.")
        if n < 2:
            return False
        return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))

```

### run.py

SHA-256: `8dc8d9b79b8fba815b5645a14f1e26b52713ee2d834200166e853592106cc263`

```python
import argparse
from waitress import serve
from app import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Локальный учебный стенд")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    print(f"Учебный стенд: http://127.0.0.1:{args.port}", flush=True)
    serve(create_app(), host="127.0.0.1", port=args.port, threads=8)

```

### app/static/style.css

SHA-256: `64263e362c7457250264b34521bb1324bf397586f71fb8efe037fbb81edf3886`

```css
:root{font-family:Segoe UI,Arial,sans-serif;color:#17243c;background:#f3f6fb;font-size:16px;line-height:1.55;--blue:#2357dc;--muted:#59677d;--line:#dce3ee}
*{box-sizing:border-box}body{margin:0}a{color:var(--blue);text-underline-offset:4px}button,input,select,textarea{font:inherit}button,a,input,select,textarea{outline-offset:4px}button:focus-visible,a:focus-visible{outline:3px solid #e79721}button{cursor:pointer;border:1px solid var(--blue);background:var(--blue);color:white;border-radius:8px;padding:11px 20px;font-weight:600}button:hover{filter:brightness(.94)}button:disabled{opacity:.6;cursor:wait}.secondary{background:white;color:#27364e;border-color:#cbd5e4}.sidebar{position:fixed;inset:0 auto 0 0;width:250px;background:#13213a;color:#b8c5da;padding:38px 24px;display:flex;flex-direction:column}.brand{color:white;text-decoration:none;font-weight:800;font-size:38px;letter-spacing:-2px}.brand span{display:block;font-size:14px;font-weight:400;letter-spacing:1px;color:#b8c5da}.nav-label{font-size:12px;letter-spacing:1.5px;margin-top:58px}.sidebar nav{display:grid;gap:8px}.sidebar nav a{color:#cfdaeb;text-decoration:none;padding:13px 12px;border-radius:7px;font-size:15px}.sidebar nav a span{margin-right:13px;font-size:12px;opacity:.65}.sidebar nav a[aria-current]{background:#2d4470;color:white;box-shadow:inset 3px 0 #88b1ff}.sidebar-foot{margin-top:auto;font-size:13px;line-height:1.8}.sidebar-foot strong{font-weight:400;color:white}.workspace{margin-left:250px}header{height:80px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;padding:0 5%;font-size:12px;letter-spacing:1px}.badge,.tag{display:inline-block;border-radius:5px;padding:4px 9px;font-size:12px;background:#e9effe;color:#234dae;letter-spacing:.2px}.badge{background:white;border:1px solid var(--line);color:#59677d}main{max-width:1200px;margin:auto;padding:45px 5% 60px;min-height:calc(100vh - 140px)}.eyebrow{font-size:12px;font-weight:700;color:var(--blue);letter-spacing:2px;margin:0 0 14px}h1{font-size:clamp(30px,3.3vw,44px);line-height:1.17;letter-spacing:-1.4px;margin:0 0 18px}h2{font-size:22px;line-height:1.3;margin:18px 0 10px;letter-spacing:-.4px}.lead{max-width:650px;color:var(--muted);margin:0 0 30px}.modules{display:grid;grid-template-columns:1fr 1fr;gap:20px}.module{display:block;padding:26px 28px;background:white;border:1px solid var(--line);border-radius:12px;text-decoration:none;color:inherit;transition:transform .15s,border-color .15s}.module:hover{transform:translateY(-3px);border-color:#829de4}.module-top{display:flex;justify-content:space-between;align-items:center}.module-number{font-size:28px;font-weight:300;color:#7588aa}.module p{color:var(--muted);margin:0 0 24px}.module-link{color:var(--blue);font-size:14px;font-weight:600}.info-strip{display:flex;gap:24px;align-items:center;padding:23px 0;margin-top:18px;border-bottom:1px solid var(--line);font-size:14px;flex-wrap:wrap}.info-strip a{margin-left:auto}.two-col{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:32px;align-items:start}.panel{background:white;border:1px solid var(--line);border-radius:12px;padding:28px;min-width:0}.panel>h2{margin-top:0;margin-bottom:24px}.notes{padding:15px 4px;color:var(--muted)}.notes h2{color:#17243c}.notes ul{padding-left:20px}.notes li{margin:12px 0}label{display:block;font-size:14px;font-weight:600;margin:16px 0 7px}input:not([type=checkbox]),select,textarea{width:100%;border:1px solid #b6c3d7;border-radius:7px;padding:11px 12px;background:#fff;color:#17243c;min-width:0}textarea{resize:vertical}input:focus,textarea:focus,select:focus{outline:2px solid #7298f1;border-color:var(--blue)}form>button{margin-top:20px}.actions{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap}.result{background:#edf3ff;border-radius:9px;padding:20px;margin-top:25px}.result span{display:block;font-size:12px;letter-spacing:1px;color:var(--muted)}output{font-size:32px;overflow-wrap:anywhere}.error{color:#b42336;font-size:14px;margin:8px 0}.error:empty{display:none}.success{background:#e5f5ed;border:1px solid #93cdb1;color:#145c3a;padding:15px;border-radius:8px}.muted{color:var(--muted);font-weight:400;font-size:14px}.mode-bar{display:flex;gap:16px;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:20px;font-size:14px}.warning{background:#fff0d1;color:#805300}.inline{display:flex;gap:12px}.list-toolbar{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:15px;padding:24px 0 12px;font-size:14px}.filters{display:flex;gap:6px;flex-wrap:wrap}.filter{background:white;border-color:var(--line);color:var(--muted);font-size:14px;padding:7px 12px}.filter[aria-pressed=true]{background:#edf3ff;border-color:#8ba9ef;color:#234dae}.task-list{list-style:none;margin:0 0 20px;padding:0}.task-list li{display:flex;gap:12px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line)}.task-list input{width:20px;height:20px;accent-color:var(--blue)}.task-list label{margin:0;flex:1;overflow-wrap:anywhere;min-width:0}.task-list li.done label{text-decoration:line-through;color:var(--muted)}.task-list button{font-size:13px;padding:6px 10px}.empty{text-align:center;color:var(--muted);padding:35px 10px}code{font-family:Consolas,monospace;background:#e9eef7;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}footer{padding:20px 5%;border-top:1px solid var(--line);color:var(--muted);font-size:12px}.skip{position:fixed;top:-100px;left:10px;background:white;z-index:10;padding:10px}.skip:focus{top:10px}
@media(max-width:900px){.sidebar{width:210px;padding:28px 15px}.workspace{margin-left:210px}.two-col{grid-template-columns:1fr}.notes{padding-top:0}.modules{gap:14px}.module{padding:20px}}
@media(max-width:640px){.sidebar{position:static;width:auto;padding:18px}.brand{font-size:27px;letter-spacing:-1px;display:flex;align-items:center;gap:18px}.brand span{font-size:12px}.nav-label,.sidebar-foot{display:none}.sidebar nav{display:flex;overflow-x:auto;gap:6px;margin-top:16px}.sidebar nav a{white-space:nowrap;font-size:14px;padding:9px}.sidebar nav a span{display:none}.workspace{margin:0}header{height:58px;font-size:10px}main{padding:30px 5%}.modules{grid-template-columns:1fr}h1{font-size:32px}.panel{padding:20px}.inline{flex-wrap:wrap}.inline button{width:100%}.info-strip{gap:10px}.info-strip a{margin-left:0}.badge{font-size:11px}}

```

### app/static/app.js

SHA-256: `f3f5c784ae01ae3b4f3f1c0da1526aeb9b58eca1ed50f98e121b29f86375835a`

```javascript
"use strict";
const calcForm = document.querySelector("#calculator-form");
if (calcForm) {
  let generation = 0;
  const result = document.querySelector("#result");
  const error = document.querySelector("#calculator-error");
  const submit = document.querySelector("#calculate");
  calcForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const current = ++generation;
    error.textContent = "";
    result.textContent = "…";
    submit.disabled = true;
    try {
      const response = await fetch("/api/calculate", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(Object.fromEntries(new FormData(calcForm)))});
      const data = await response.json();
      if (current !== generation) return;
      if (!response.ok) throw new Error(data.error || "Не удалось вычислить результат.");
      result.textContent = data.display;
    } catch (failure) {
      if (current !== generation) return;
      result.textContent = "—";
      error.textContent = failure.message === "Failed to fetch" ? "Сервер недоступен. Повторите попытку." : failure.message;
    } finally {
      if (current === generation) submit.disabled = false;
    }
  });
  document.querySelector("#clear").addEventListener("click", () => {
    generation++;
    calcForm.reset(); result.textContent = "—"; error.textContent = ""; submit.disabled = false;
    document.querySelector("#number-a").focus();
  });
}

const todo = document.querySelector("#todo-app");
if (todo) {
  const buggy = todo.dataset.buggy === "true";
  const key = `tasks-${buggy ? "buggy" : "fixed"}-v1`;
  const error = document.querySelector("#todo-error");
  let tasks = [];
  let filter = "all";
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    if (!Array.isArray(saved) || !saved.every(t => t && typeof t.id === "string" && typeof t.title === "string" && typeof t.done === "boolean")) throw new Error();
    tasks = saved;
  } catch { error.textContent = "Не удалось прочитать сохраненные задачи. Начат пустой список."; }
  function save() {
    try { localStorage.setItem(key, JSON.stringify(tasks)); }
    catch { error.textContent = "Хранилище недоступно. Изменения останутся только до закрытия страницы."; }
    render();
  }
  function render() {
    const list = document.querySelector("#task-list");
    list.replaceChildren();
    const visible = tasks.filter(t => filter === "all" || (filter === "done" ? t.done : !t.done));
    visible.forEach((task, index) => {
      const row = document.createElement("li");
      row.className = task.done ? "done" : "";
      row.dataset.id = task.id;
      const check = document.createElement("input");
      check.type = "checkbox"; check.checked = task.done; check.id = `task-${task.id}`;
      check.addEventListener("change", () => { task.done = check.checked; save(); });
      const label = document.createElement("label");
      label.htmlFor = check.id; label.textContent = task.title;
      const remove = document.createElement("button");
      remove.className = "secondary delete-task"; remove.textContent = "Удалить";
      remove.setAttribute("aria-label", `Удалить задачу ${task.title}`);
      remove.addEventListener("click", () => {
        // Intentional defect BUG-03: filtered index is not the original index.
        if (buggy) tasks.splice(index, 1);
        else tasks = tasks.filter(t => t.id !== task.id);
        save();
      });
      row.append(check, label, remove); list.append(row);
    });
    document.querySelector("#empty-tasks").hidden = visible.length > 0;
    document.querySelector("#empty-tasks").textContent = tasks.length ? "Нет задач для выбранного фильтра." : "Здесь пока нет задач. Добавьте первую выше.";
    // Intentional defect BUG-02: completed tasks are counted as active.
    document.querySelector("#task-counter").textContent = `Активных: ${buggy ? tasks.length : tasks.filter(t => !t.done).length}`;
  }
  document.querySelector("#todo-form").addEventListener("submit", event => {
    event.preventDefault(); error.textContent = "";
    const input = document.querySelector("#task-title");
    // Intentional defect BUG-01: whitespace is accepted.
    const title = buggy ? input.value : input.value.trim();
    if (!title || title.length > 120) { error.textContent = "Введите задачу длиной от 1 до 120 символов."; return; }
    tasks.push({id: crypto.randomUUID(), title, done: false}); input.value = ""; save(); input.focus();
  });
  document.querySelectorAll("[data-filter]").forEach(button => button.addEventListener("click", () => {
    filter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    render();
  }));
  document.querySelector("#reset-tasks").addEventListener("click", () => { tasks = []; error.textContent = ""; save(); });
  render();
}

```

### requirements.txt

SHA-256: `05b055cad237ae3212058d5a2f632537c5bc4a0a6b4d67927778fd11382dd4f8`

```text
Flask==3.1.3
waitress==3.0.2

```

### requirements-dev.txt

SHA-256: `c91ce27370688b171fe6d98243a3351c7e10ae687ff951be1ee0f6df37eb5e9a`

```text
-r requirements.txt
pytest==9.1.1
selenium==4.49.0
webdriver-manager==4.1.2
requests==2.34.2

```

### app/templates/account.html

SHA-256: `c0c252a2ab4ace4437e0974bf18d95f6f78962fab6ee2c88f54f1b58c05b4871`

```html
{% extends 'base.html' %}{% block title %}Личный кабинет{% endblock %}
{% block content %}<p class="eyebrow">МОДУЛЬ 03 / АВТОРИЗАЦИЯ</p><h1 id="welcome">Добро пожаловать, student!</h1><section class="panel"><p id="login-success" class="success">Вход выполнен успешно.</p><p>Защищенная страница доступна до выхода из сессии.</p><form action="/logout" method="post"><button id="logout">Logout</button></form></section>{% endblock %}

```

### app/templates/base.html

SHA-256: `f0e8567f7161f6bb1ebc417a074bae2e6798c6b1c7ab487bd33920a5e8ca13bb`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Учебный стенд для лабораторных работ по тестированию ПО">
  <title>{% block title %}Практикум{% endblock %} · Тестирование ПО</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <script defer src="{{ url_for('static', filename='app.js') }}"></script>
</head>
<body>
  <a class="skip" href="#main">К содержимому</a>
  <aside class="sidebar">
    <a class="brand" href="/">ТПО<span>Практикум / 01</span></a>
    <p class="nav-label">РАБОЧЕЕ ПРОСТРАНСТВО</p>
    <nav aria-label="Основная навигация">
      {% for key, path, label, number in [('home','/','Обзор','00'),('calculator','/calculator','Калькулятор','01'),('todo','/todo','Список задач','02'),('login','/login','Вход в систему','03'),('contact','/contact','Контактная форма','04')] %}
      <a href="{{ path }}" {% if active == key %}aria-current="page"{% endif %}><span>{{ number }}</span>{{ label }}</a>
      {% endfor %}
    </nav>
    <div class="sidebar-foot">Учебный стенд<br><strong>Локально. Без базы данных.</strong></div>
  </aside>
  <div class="workspace">
    <header><span>ПОЛИТЕХ / ТЕСТИРОВАНИЕ ПО</span><span class="badge">Веб-практикум</span></header>
    <main id="main">{% block content %}{% endblock %}</main>
    <footer>Требования → сценарии → проверка → результат</footer>
  </div>
</body>
</html>

```

### app/templates/calculator.html

SHA-256: `09cbc7e014f216ea84cda2f2d3e23700b4a9381c1d4c5ba2efe573c50510cd1b`

```html
{% extends 'base.html' %}{% block title %}Калькулятор{% endblock %}
{% block content %}
<p class="eyebrow">МОДУЛЬ 01 / ЛР 1 И 6</p><h1>Калькулятор</h1><p class="lead">Два числа, четыре операции. Результат вычисляется на сервере.</p>
<div class="two-col"><section class="panel"><h2>Вычисление</h2>
<form id="calculator-form" novalidate>
<label for="number-a">Первое число</label><input id="number-a" name="a" inputmode="decimal" placeholder="Например, 12.5" autocomplete="off">
<label for="operation">Операция</label><select id="operation" name="operation"><option value="add">+ Сложение</option><option value="subtract">− Вычитание</option><option value="multiply">× Умножение</option><option value="divide">÷ Деление</option></select>
<label for="number-b">Второе число</label><input id="number-b" name="b" inputmode="decimal" placeholder="Например, 2" autocomplete="off">
<div class="actions"><button id="calculate" type="submit">Вычислить</button><button id="clear" type="button" class="secondary">Очистить</button></div>
</form><div class="result" aria-live="polite"><span>РЕЗУЛЬТАТ</span><output id="result">—</output></div><p id="calculator-error" class="error" role="alert"></p>
</section><aside class="notes"><span class="tag">Условия проверки</span><h2>Начните с простого</h2><p>Проверьте положительные и отрицательные числа, дроби и ноль.</p><ul><li>Дробный разделитель: точка или запятая.</li><li>Диапазон ввода: от −10¹² до 10¹².</li><li>Результат: до 12 значащих цифр.</li><li>Очистка сбрасывает числа, операцию и результат.</li></ul></aside></div>
{% endblock %}

```

### app/templates/contact.html

SHA-256: `2a5be025dafc85a08641992676f423c2eace59515093a7571f6b5d0cb22100c6`

```html
{% extends 'base.html' %}{% block title %}Контактная форма{% endblock %}
{% block content %}<p class="eyebrow">МОДУЛЬ 04 / ЛР 4</p><h1>Контактная форма</h1><p class="lead">Проверьте валидные данные и сообщения об ошибках.</p><div class="two-col"><section class="panel">
{% if success %}<p id="contact-success" class="success" role="status">Форма успешно отправлена.</p>{% endif %}
<form id="contact-form" method="post" novalidate>
{% for key, label in [('name','Имя'),('email','Email'),('message','Сообщение')] %}
<label for="{{ key }}">{{ label }} <span class="muted">(обязательно)</span></label>
{% if key == 'message' %}<textarea id="{{ key }}" name="{{ key }}" rows="5" aria-describedby="{{ key }}-error" aria-invalid="{{ 'true' if errors.get(key) else 'false' }}">{{ values[key] }}</textarea>{% else %}<input id="{{ key }}" name="{{ key }}" type="{{ 'email' if key == 'email' else 'text' }}" value="{{ values[key] }}" aria-describedby="{{ key }}-error" aria-invalid="{{ 'true' if errors.get(key) else 'false' }}">{% endif %}
<p id="{{ key }}-error" class="error" {% if errors.get(key) %}role="alert"{% endif %}>{{ errors.get(key, '') }}</p>
{% endfor %}<button id="contact-submit">Отправить</button></form></section><aside class="notes"><span class="tag">Правила заполнения</span><h2>Три обязательных поля</h2><ul><li>Имя: от 2 до 60 символов.</li><li>Email: адрес с @ и точкой в домене, не более 120 символов.</li><li>Сообщение: от 10 до 1000 символов.</li></ul><p>Пробелы по краям удаляются. Это учебная форма: письма не отправляются, данные не сохраняются.</p></aside></div>{% endblock %}

```

### app/templates/index.html

SHA-256: `18f0ace88958e1269d61e151ecf51008f3366797ecd16fc188c3fdbbfe72c2aa`

```html
{% extends 'base.html' %}
{% block content %}
<p class="eyebrow">ЛАБОРАТОРНЫЕ РАБОТЫ</p>
<h1>От сценария<br>к проверенному результату.</h1>
<p class="lead">Четыре модуля для ручного тестирования и автоматизации. Выберите объект и начните проверку.</p>
<div class="modules">
  {% for n, title, desc, labs, path in [('01','Калькулятор','Арифметика, граничные значения и обработка ошибок.','ЛР 1 · ЛР 6','/calculator'),('02','Список задач','Сценарии, фильтры и поиск намеренных дефектов.','ЛР 2','/todo'),('03','Вход в систему','Учебная авторизация и первый Selenium-тест.','ЛР 3','/login'),('04','Контактная форма','Валидация полей и Page Object.','ЛР 4','/contact')] %}
  <a class="module" href="{{ path }}"><div class="module-top"><span class="module-number">{{ n }}</span><span class="tag">{{ labs }}</span></div><h2>{{ title }}</h2><p>{{ desc }}</p><span class="module-link">Открыть модуль ↗</span></a>
  {% endfor %}
</div>
<div class="info-strip"><strong>API для нагрузки</strong><code>GET /api/health</code><a href="/api/health">Посмотреть ответ ↗</a></div>
{% endblock %}

```

### app/templates/login.html

SHA-256: `ca6fb90c2a09634e344b26329af671e0d2e486e080d65acd66bad5a3ce6b9bab`

```html
{% extends 'base.html' %}{% block title %}Вход{% endblock %}
{% block content %}<p class="eyebrow">МОДУЛЬ 03 / ЛР 3</p><h1>Вход в систему</h1><p class="lead">Страница для проверки авторизации и стабильных селекторов.</p>
<div class="two-col"><section class="panel"><h2>Учебная учетная запись</h2><form method="post" novalidate><label for="username">Логин</label><input id="username" name="username" autocomplete="username"><label for="password">Пароль</label><input id="password" name="password" type="password" autocomplete="current-password"><button id="login-submit">Войти</button></form>{% if error %}<p id="login-error" class="error" role="alert">{{ error }}</p>{% endif %}</section><aside class="notes"><span class="tag">Тестовые данные</span><h2>Доступ к стенду</h2><p>Логин: <code>student</code><br>Пароль: <code>Test123!</code></p><p>После входа откроется личный кабинет с кнопкой Logout.</p></aside></div>{% endblock %}

```

### app/templates/todo.html

SHA-256: `cdc0f6873a7884b121d76fb675ed67032395046232489c0e36c656f849b19695`

```html
{% extends 'base.html' %}{% block title %}Список задач{% endblock %}
{% block content %}
<p class="eyebrow">МОДУЛЬ 02 / ЛР 2</p><h1>Список задач</h1><p class="lead">Добавляйте задачи, отмечайте выполненные и проверяйте фильтры.</p>
<div class="mode-bar"><span class="tag {{ 'warning' if buggy else '' }}">{{ 'С намеренными дефектами' if buggy else 'Исправный режим' }}</span><a id="switch-mode" href="/todo{{ '' if buggy else '?mode=buggy' }}">{{ 'Открыть исправный режим' if buggy else 'Открыть режим с дефектами' }} ↗</a></div>
<section class="panel" id="todo-app" data-buggy="{{ 'true' if buggy else 'false' }}">
<form id="todo-form" novalidate><label for="task-title">Новая задача</label><div class="inline"><input id="task-title" name="title" maxlength="120" placeholder="Что нужно сделать?" autocomplete="off"><button id="add-task">Добавить</button></div></form>
<p id="todo-error" class="error" role="alert"></p><div class="list-toolbar"><div class="filters" aria-label="Фильтр задач"><button class="filter" data-filter="all" aria-pressed="true">Все</button><button class="filter" data-filter="active" aria-pressed="false">Активные</button><button class="filter" data-filter="done" aria-pressed="false">Выполненные</button></div><span id="task-counter" aria-live="polite"></span></div>
<ul id="task-list" class="task-list"></ul><p id="empty-tasks" class="empty">Здесь пока нет задач. Добавьте первую выше.</p><button id="reset-tasks" class="secondary">Сбросить список</button>
</section><p class="muted">Задачи сохраняются в этом браузере. У каждого режима отдельный список.</p>
{% endblock %}

```

### scripts/browser.py

SHA-256: `c2d6702a0011a5af26185cbd3782261f0bafa57ec96fa1c5011e89e21408012b`

```python
"""One WebDriver factory used by lab 3's script and pytest fixtures."""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager


def create_browser(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=ru")
    driver_path = os.environ.get("CHROMEDRIVER")
    if not driver_path and Path("tools/bin/chromedriver.exe").exists():
        driver_path = str(Path("tools/bin/chromedriver.exe").resolve())
    if not driver_path:
        driver_path = ChromeDriverManager(cache_manager=DriverCacheManager(root_dir="tools/bin")).install()
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.set_page_load_timeout(30)
    return driver

```

### scripts/browser_smoke.py

SHA-256: `6a5883fca20e213b79867c815045777a9ad07e0fd0271e9e9d85530ff808576f`

```python
import argparse
from scripts.browser import create_browser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:5000/login")
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    browser = create_browser(headless=not args.headed)
    try:
        browser.get(args.url)
        print(f"Opened: {browser.current_url}\nTitle: {browser.title}")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()

```

### tests/conftest.py

SHA-256: `1b325add053e8a89f94e9d4d9da66f5126d4b4baed73835093e350de26eaa715`

```python
from pathlib import Path
import hashlib
import re
import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


def pytest_addoption(parser):
    parser.addoption("--run-ui", action="store_true", help="Run Selenium Chrome tests")
    parser.addoption("--run-api", action="store_true", help="Run tests against public JSONPlaceholder")
    parser.addoption("--headed", action="store_true", help="Show Chrome window")


def pytest_collection_modifyitems(config, items):
    for item in items:
        for marker, option in (("ui", "--run-ui"), ("api", "--run-api")):
            if marker in item.keywords and not config.getoption(option):
                item.add_marker(pytest.mark.skip(reason=f"Enable with {option}"))


@pytest.fixture
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test-only-key"})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def base_url():
    server = make_server("127.0.0.1", 0, create_app({"TESTING": True, "SECRET_KEY": "ui-test-key"}), threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()


@pytest.fixture
def browser(request):
    from scripts.browser import create_browser
    driver = create_browser(headless=not request.config.getoption("--headed"))
    folder = Path("artifacts/ui")
    folder.mkdir(parents=True, exist_ok=True)
    yield driver
    try:
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.originalname or request.node.name)
        suffix = hashlib.sha256(request.node.nodeid.encode()).hexdigest()[:8]
        driver.save_screenshot(str(folder / f"{name}-{suffix}.png"))
    finally:
        driver.quit()

```

### tests/ui/pages/base_page.py

SHA-256: `867c6025875416cc2d989d2a97a55ba7a475a1f53ce0ea79af3b78ab2f1a7ea3`

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path):
        self.driver.get(self.base_url + path)
        return self

    def element(self, element_id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, element_id)))

    def fill(self, element_id, value):
        element = self.element(element_id)
        element.clear()
        element.send_keys(value)

    def click(self, element_id):
        self.wait.until(EC.element_to_be_clickable((By.ID, element_id))).click()

```

### tests/ui/pages/login_page.py

SHA-256: `1f05840982d4b5b7538960f1ea6d4333f562ead78ce0f4c1ff5a53bdd86e83a9`

```python
from .base_page import BasePage


class LoginPage(BasePage):
    def visit(self):
        return self.open("/login")

    def login(self, username="student", password="Test123!"):
        self.fill("username", username)
        self.fill("password", password)
        self.click("login-submit")
        return self

```

### tests/ui/test_forms.py

SHA-256: `ae122fdca1a044e2ac63cf87eac1bdc4893b6b7e5c166c3b5563184d35df7c07`

```python
import pytest
from selenium.webdriver.common.by import By
from tests.ui.pages.contact_page import ContactPage
from tests.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_valid_login_and_logout(browser, base_url):
    page = LoginPage(browser, base_url).visit().login()
    assert page.element("logout").text == "Logout"
    assert page.element("login-success").text == "Вход выполнен успешно."
    page.click("logout")
    page.element("username")
    browser.get(base_url + "/account")
    assert browser.current_url.endswith("/login")


def test_invalid_login(browser, base_url):
    page = LoginPage(browser, base_url).visit().login(password="wrong")
    assert page.element("login-error").text == "Неверный логин или пароль."
    assert not browser.find_elements(By.ID, "logout")


def test_contact_success(browser, base_url):
    page = ContactPage(browser, base_url).visit().submit("Иван", "ivan@example.com", "Проверка контактной формы")
    assert page.element("contact-success").text == "Форма успешно отправлена."


@pytest.mark.parametrize("field,name,email,message,error", [
    ("name", "", "ivan@example.com", "Тестовое сообщение", "Имя должно содержать от 2 до 60 символов."),
    ("email", "Иван", "", "Тестовое сообщение", "Введите корректный email."),
    ("email", "Иван", "bad-email", "Тестовое сообщение", "Введите корректный email."),
    ("message", "Иван", "ivan@example.com", "", "Сообщение должно содержать от 10 до 1000 символов."),
])
def test_contact_invalid(browser, base_url, field, name, email, message, error):
    page = ContactPage(browser, base_url).visit().submit(name, email, message)
    assert page.error(field) == error
    assert not browser.find_elements(By.ID, "contact-success")

```

### tests/ui/pages/contact_page.py

SHA-256: `beea4de109e5fd3d8342248c2acfd87e87a7fe94f198b261ee43fdddd197c49f`

```python
from .base_page import BasePage


class ContactPage(BasePage):
    def visit(self):
        return self.open("/contact")

    def submit(self, name, email, message):
        for key, value in (("name", name), ("email", email), ("message", message)):
            self.fill(key, value)
        self.click("contact-submit")
        return self

    def error(self, field):
        return self.element(f"{field}-error").text

```
