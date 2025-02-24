import speedtest
import time
import threading
import sys
import itertools

def spinner(msg, stop_event):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])
    while not stop_event.is_set():
        sys.stdout.write("\r" + msg + " " + next(spinner_cycle))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + msg + " completed!\n")
    sys.stdout.flush()

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024
    upload_speed = st.upload() / 1024 / 1024
    ping = st.results.ping
    return download_speed, upload_speed, ping

def main():
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=("Running speedtest...", stop_event))
    start_time = time.time()
    spinner_thread.start()
    download_speed, upload_speed, ping = run_speedtest()
    stop_event.set()
    spinner_thread.join()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nDownload: {download_speed:.2f} Mbps")
    print(f"Upload:   {upload_speed:.2f} Mbps")
    print(f"Ping:     {ping:.2f} ms")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()