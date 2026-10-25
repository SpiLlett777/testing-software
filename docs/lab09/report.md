# Лабораторная работа 9. GitHub Actions

Подготовлен `.github/workflows/run-tests.yml`: push, pull_request и workflow_dispatch; runner Ubuntu; Python 3.13;
установка зависимостей; pytest unit+UI; выгрузка artifacts при любом исходе. Временный сервер для UI запускает pytest
fixture. ChromeDriver подбирается webdriver-manager. Публичные API-тесты запускаются отдельным job при
workflow_dispatch, чтобы зависимость от чужого сервиса не делала каждый push нестабильным.

## Действия для выполнения работы

1. Создать **публичный** пустой репозиторий в своем GitHub-аккаунте.
2. Проверить `.gitignore`: не включать .venv, tools/bin, учетные данные и реальные секреты.
3. Из корня проекта выполнить команды, заменив OWNER/REPOSITORY реальными значениями:

```powershell
git init
git add .
git commit -m "Add testing lab application and automated tests"
git branch -M main
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

4. Открыть Actions, дождаться выполнения workflow. При ошибке изучить лог, исправить причину, сделать новый commit/push.
5. Сохранить ссылку на успешный run, commit SHA, скриншот зеленого статуса и скачать test-results.

Эта инструкция рассчитана на каталог без существующего Git-репозитория. Если репозиторий/remote уже есть, использовать
его, не переинициализировать и не переписывать историю.

## Фактический статус

YAML подготовлен. Публикация и запуск на GitHub не выполнялись; ссылка на реальный успешный run отсутствует. Локальные
результаты не являются доказательством завершения ЛР 9.
