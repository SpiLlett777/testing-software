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
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(Object.fromEntries(new FormData(calcForm)))
            });

            const data = await response.json();

            if (current !== generation) return;
            if (!response.ok) throw new Error(data.error || "Не удалось вычислить результат.");

            result.textContent = data.display;
        } catch (failure) {
            if (current !== generation) return;

            result.textContent = "—";
            error.textContent = failure.message === "Failed to fetch"
                ? "Сервер недоступен. Повторите попытку."
                : failure.message;
        } finally {
            if (current === generation) submit.disabled = false;
        }
    });

    document.querySelector("#clear").addEventListener("click", () => {
        generation++;
        calcForm.reset();
        result.textContent = "—";
        error.textContent = "";
        submit.disabled = false;
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
        if (
            !Array.isArray(saved) ||
            !saved.every(t => t && typeof t.id === "string" && typeof t.title === "string" && typeof t.done === "boolean")
        ) {
            throw new Error();
        }
        tasks = saved;
    } catch {
        error.textContent = "Не удалось прочитать сохраненные задачи. Начат пустой список.";
    }

    function save() {
        try {
            localStorage.setItem(key, JSON.stringify(tasks));
        } catch {
            error.textContent = "Хранилище недоступно. Изменения останутся только до закрытия страницы.";
        }
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
            check.type = "checkbox";
            check.checked = task.done;
            check.id = `task-${task.id}`;
            check.addEventListener("change", () => {
                task.done = check.checked;
                save();
            });

            const label = document.createElement("label");
            label.htmlFor = check.id;
            label.textContent = task.title;

            const remove = document.createElement("button");
            remove.className = "secondary delete-task";
            remove.textContent = "Удалить";
            remove.setAttribute("aria-label", `Удалить задачу ${task.title}`);
            remove.addEventListener("click", () => {
                // Intentional defect BUG-03: filtered index is not the original index.
                if (buggy)
                    tasks.splice(index, 1);
                else
                    tasks = tasks.filter(t => t.id !== task.id);

                save();
            });

            row.append(check, label, remove);
            list.append(row);
        });

        const emptyTasks = document.querySelector("#empty-tasks");
        emptyTasks.hidden = visible.length > 0;
        emptyTasks.textContent = tasks.length
            ? "Нет задач для выбранного фильтра."
            : "Здесь пока нет задач. Добавьте первую выше.";

        // Intentional defect BUG-02: completed tasks are counted as active.
        document.querySelector("#task-counter").textContent = `Активных: ${
            buggy ? tasks.length : tasks.filter(t => !t.done).length
        }`;
    }

    document.querySelector("#todo-form").addEventListener("submit", event => {
        event.preventDefault();
        error.textContent = "";

        const input = document.querySelector("#task-title");
        // Intentional defect BUG-01: whitespace is accepted.
        const title = buggy ? input.value : input.value.trim();

        if (!title || title.length > 120) {
            error.textContent = "Введите задачу длиной от 1 до 120 символов.";
            return;
        }

        tasks.push({
            id: crypto.randomUUID(),
            title,
            done: false
        });

        input.value = "";
        save();
        input.focus();
    });

    document.querySelectorAll("[data-filter]").forEach(button => {
        button.addEventListener("click", () => {
            filter = button.dataset.filter;
            document.querySelectorAll("[data-filter]").forEach(item => {
                item.setAttribute("aria-pressed", String(item === button));
            });
            render();
        });
    });

    document.querySelector("#reset-tasks").addEventListener("click", () => {
        tasks = [];
        error.textContent = "";
        save();
    });

    render();
}
