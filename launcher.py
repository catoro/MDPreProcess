"""
Entry point for the bundled .app — starts uvicorn in a background thread
then opens the browser. Keeps running until the window is closed.
"""
import sys
import os
import threading
import time
import webbrowser

# When running from a PyInstaller bundle, resources are in sys._MEIPASS
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    # Set cwd so StaticFiles can find the 'static' folder
    os.chdir(BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = 8765


def run_server():
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, log_level="warning")


if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # Wait until the server is ready
    import urllib.request
    for _ in range(20):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/")
            break
        except Exception:
            time.sleep(0.3)

    webbrowser.open(f"http://127.0.0.1:{PORT}/")

    # Keep the process alive
    t.join()
