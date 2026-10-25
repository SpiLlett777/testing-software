import json
from pathlib import Path


def main():
    folder = Path("artifacts/lab08")
    rows = []
    for name in ("10vu", "50vu"):
        data = json.loads((folder / f"{name}.json").read_text(encoding="utf-8"))
        metrics = data["metrics"]
        reqs = metrics["http_reqs"]["values"]
        duration = metrics["http_req_duration"]["values"]
        errors = metrics["http_req_failed"]["values"]["rate"]
        checks = metrics["checks"]["values"]["rate"]
        rows.append(f"| {name} | {reqs['count']} | {reqs['rate']:.2f} | {duration['avg']:.2f} | {duration['p(95)']:.2f} | {errors * 100:.2f}% | {checks * 100:.2f}% |")
    text = "# Фактические результаты k6\n\n| Профиль | Запросов | req/s | Среднее, мс | p95, мс | HTTP-ошибки | Успешные проверки |\n| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(rows)
    text += "\n\nДанные прочитаны из JSON k6 без ручной подстановки. Сравнивать req/s и задержки, а не только общее число запросов: длительность прогонов различается. Условия: один локальный компьютер, Waitress 8 потоков, пауза 0.1 с на итерацию. Это короткие прогоны, не длительное испытание устойчивости.\n"
    (folder / "analysis.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
