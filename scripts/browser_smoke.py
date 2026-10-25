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
