"""Download portable tools from official publishers into the project only."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import zipfile
import requests

DEST = Path("tools/bin")


def download(url):
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    return response


def extract_binary(url, filename):
    archive = zipfile.ZipFile(io.BytesIO(download(url).content))
    matches = [name for name in archive.namelist() if name.endswith("/" + filename)]
    if len(matches) != 1:
        raise ValueError(f"Expected one {filename} in publisher archive")
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / filename).write_bytes(archive.read(matches[0]))
    print(f"Saved {DEST / filename}")


def chrome():
    version = subprocess.check_output(["powershell", "-NoProfile", "-Command", "(Get-Item 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe').VersionInfo.ProductVersion"], text=True).strip()
    build = ".".join(version.split(".")[:3])
    # Same official Chrome for Testing metadata, served by the repository's raw endpoint.
    metadata = download("https://raw.githubusercontent.com/GoogleChromeLabs/chrome-for-testing/gh-pages/latest-patch-versions-per-build-with-downloads.json").json()
    entry = metadata["builds"][build]
    url = next(item["url"] for item in entry["downloads"]["chromedriver"] if item["platform"] == "win64")
    extract_binary(url, "chromedriver.exe")
    return {"chrome": version, "chromedriver": entry["version"], "source": url}


def k6():
    release = download("https://github.com/grafana/k6/releases/latest")
    version = release.url.rstrip("/").split("/")[-1]
    if not version.startswith("v") or not all(c.isdigit() or c == "." for c in version[1:]):
        raise ValueError("Unexpected k6 release tag")
    url = f"https://github.com/grafana/k6/releases/download/{version}/k6-{version}-windows-amd64.zip"
    extract_binary(url, "k6.exe")
    return {"k6": version, "source": url}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tool", choices=["chrome", "k6"])
    args = parser.parse_args()
    result = chrome() if args.tool == "chrome" else k6()
    Path("artifacts").mkdir(exist_ok=True)
    Path(f"artifacts/{args.tool}-tool.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
