"""Record reproducible environment details without account names or secrets."""
import importlib.metadata
import json
import platform
import subprocess
import sys
from pathlib import Path


def main():
    packages = ("Flask", "waitress", "pytest", "selenium", "webdriver-manager", "requests")
    data = {"python": sys.version, "os": platform.platform(), "machine": platform.machine(), "packages": {name: importlib.metadata.version(name) for name in packages}, "server": {"host": "127.0.0.1", "port": 5000, "threads": 8}}
    if platform.system() == "Windows":
        command = "[PSCustomObject]@{CPU=(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name); LogicalProcessors=[Environment]::ProcessorCount; RAM_GiB=[Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)} | ConvertTo-Json"
        data["hardware"] = json.loads(subprocess.check_output(["powershell", "-NoProfile", "-Command", command], text=True))
    for name in ("chrome", "k6"):
        path = Path(f"artifacts/{name}-tool.json")
        if path.exists():
            data[name] = json.loads(path.read_text(encoding="utf-8"))
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/environment.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
