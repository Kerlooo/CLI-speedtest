# Python CLI SpeedTest

A small command-line tool that measures your internet connection speed (ping, download, upload) using [speedtest.net](https://www.speedtest.net/) servers.

```
Server:   Mynet (Mantova, Italy) - 104 km
Ping:     23.00 ms
Download: 94.20 Mbps
Upload:   19.85 Mbps
Elapsed:  31.42 s
```

## Requirements

- Python 3.8+
- [`speedtest-cli`](https://pypi.org/project/speedtest-cli/) (installed via `requirements.txt`)

## Installation

### Linux / macOS

```bash
git clone https://github.com/Kerlooo/CLI-speedtest.git
cd CLI-speedtest
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### Windows

```powershell
git clone https://github.com/Kerlooo/CLI-speedtest.git
cd CLI-speedtest
py -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

## Usage

With the virtual environment active:

```bash
python speed_test.py
```

### Options

| Option        | Description                                 |
|---------------|---------------------------------------------|
| `--json`      | Print results as JSON (useful for scripts)  |
| `--no-upload` | Skip the upload test for a faster run       |
| `--server ID` | Use a specific speedtest.net server         |
| `-h, --help`  | Show help                                   |

### JSON output

```bash
python speed_test.py --json
```

```json
{
  "server": {
    "id": "32003",
    "sponsor": "Mynet",
    "name": "Mantova",
    "country": "Italy",
    "distance_km": 104.45
  },
  "ping_ms": 23.0,
  "download_mbps": 94.2,
  "upload_mbps": 19.85,
  "elapsed_s": 31.42
}
```

`upload_mbps` is `null` when `--no-upload` is used.

## Notes

- Speeds are reported in megabits per second (1 Mbps = 1,000,000 bit/s), the same unit used by speedtest.net.
- The progress spinner is written to stderr, so `--json` output can be piped safely (e.g. `python speed_test.py --json | jq .download_mbps`).
- Exit codes: `0` success, `1` speedtest error (network, server not found), `130` interrupted with Ctrl+C.
