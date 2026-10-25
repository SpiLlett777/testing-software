import argparse
from waitress import serve
from app import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Локальный учебный стенд")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    print(f"Учебный стенд: http://127.0.0.1:{args.port}", flush=True)
    serve(create_app(), host="127.0.0.1", port=args.port, threads=8)
