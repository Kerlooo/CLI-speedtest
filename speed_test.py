import argparse
import itertools
import json
import sys
import threading
import time

import speedtest


class Spinner:
    """Animated spinner on stderr. Update `msg` to change the displayed phase."""

    def __init__(self, msg):
        self.msg = msg
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._last_len = 0

    def _write(self, text):
        # Pad with spaces to overwrite leftovers from a longer previous line
        sys.stderr.write("\r" + text.ljust(self._last_len))
        sys.stderr.flush()
        self._last_len = len(text)

    def _run(self):
        for char in itertools.cycle("-/|\\"):
            if self._stop.is_set():
                break
            self._write(f"{self.msg} {char}")
            time.sleep(0.1)
        self._write("")
        sys.stderr.write("\r")

    def __enter__(self):
        # Animate only on a real terminal, not when piped or redirected
        if sys.stderr.isatty():
            self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join()


def run_speedtest(spinner, server_id=None, upload=True):
    spinner.msg = "Connecting to speedtest.net..."
    st = speedtest.Speedtest(secure=True)

    spinner.msg = "Selecting server..."
    if server_id:
        st.get_servers([server_id])
    st.get_best_server()

    spinner.msg = "Testing download..."
    st.download()

    if upload:
        spinner.msg = "Testing upload..."
        st.upload()

    return st.results


def to_mbps(bits_per_second):
    return bits_per_second / 1_000_000


def print_results(results, elapsed, upload):
    server = results.server
    print(f"Server:   {server['sponsor']} ({server['name']}, {server['country']}) - {server['d']:.0f} km")
    print(f"Ping:     {results.ping:.2f} ms")
    print(f"Download: {to_mbps(results.download):.2f} Mbps")
    if upload:
        print(f"Upload:   {to_mbps(results.upload):.2f} Mbps")
    print(f"Elapsed:  {elapsed:.2f} s")


def print_json(results, elapsed, upload):
    server = results.server
    data = {
        "server": {
            "id": server["id"],
            "sponsor": server["sponsor"],
            "name": server["name"],
            "country": server["country"],
            "distance_km": round(server["d"], 2),
        },
        "ping_ms": round(results.ping, 2),
        "download_mbps": round(to_mbps(results.download), 2),
        "upload_mbps": round(to_mbps(results.upload), 2) if upload else None,
        "elapsed_s": round(elapsed, 2),
    }
    print(json.dumps(data, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Measure internet speed using speedtest.net.")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    parser.add_argument("--no-upload", action="store_true", help="skip the upload test")
    parser.add_argument("--server", type=int, metavar="ID", help="use a specific speedtest.net server ID")
    return parser.parse_args()


def main():
    args = parse_args()
    upload = not args.no_upload
    start_time = time.monotonic()

    try:
        with Spinner("Starting...") as spinner:
            results = run_speedtest(spinner, args.server, upload)
    except speedtest.SpeedtestException as e:
        print(f"Speedtest failed: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130

    elapsed = time.monotonic() - start_time
    if args.json:
        print_json(results, elapsed, upload)
    else:
        print_results(results, elapsed, upload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
