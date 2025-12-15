import json, os, socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import requests

CONFIG_FILE = "config.json"
STATE_FILE = "state.json"

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
    else:
        cfg = {}

    if "PP_HOST" not in cfg:
        cfg["PP_HOST"] = "localhost"
    if "PP_PORT" not in cfg:
        cfg["PP_PORT"] = 20562
    if "MESSAGE_UUID" not in cfg:
        cfg["MESSAGE_UUID"] = ""
    if "GROUPS" not in cfg:
        cfg["GROUPS"] = [
            {"name":"Rasselbande","prefix":"R","style":1},
            {"name":"Königskinder","prefix":"K","style":2}
        ]
    return cfg


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


# ---------------------------------------------------------
# STATE
# ---------------------------------------------------------
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"active": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)



# ---------------------------------------------------------
# ULTRA PORT SCAN
# ---------------------------------------------------------

def pp_port_is_valid(port):
    """Prüfen, ob ein Port wirklich ein ProPresenter-Port ist."""
    try:
        url = f"http://localhost:{port}/v1/messages"
        r = requests.get(url, timeout=0.3)
        if r.status_code in (200, 204, 207):
            try:
                _ = r.json()
                return True
            except:
                return False
        return False
    except:
        return False


def scan_for_pp_port(current_port):
    """
    Ultra-PortScan:
    - Nur nutzen, wenn aktueller Port fehlgeschlagen ist.
    - Range: 1000–50000
    - Sofortiger Abbruch, wenn ein gültiger Port gefunden wird.
    """

    print("[PortFix] Connection failed — starting scan...")

    # 1) Nachbarports zuerst
    for p in range(max(1000, current_port - 20), min(50001, current_port + 21)):
        if pp_port_is_valid(p):
            print(f"[PortFix] PP found on port {p} — saved.")
            return p

    # 2) Schneller Check aller offenen Ports
    try:
        with os.popen("lsof -iTCP -sTCP:LISTEN -nP") as proc:
            lines = proc.read().splitlines()
        for line in lines:
            if "TCP" in line:
                parts = line.split()
                for part in parts:
                    if ":" in part:
                        try:
                            cand = int(part.split(":")[-1])
                            if 1000 <= cand <= 50000:
                                if pp_port_is_valid(cand):
                                    print(f"[PortFix] PP found on port {cand} — saved.")
                                    return cand
                        except:
                            pass
    except:
        pass

    # 3) Vollscan (1000–50000)
    for port in range(1000, 50001):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.02)
        if s.connect_ex(("localhost", port)) == 0:
            if pp_port_is_valid(port):
                print(f"[PortFix] PP found on port {port} — saved.")
                s.close()
                return port
        s.close()

    print("[PortFix] No valid PP port found — keeping existing port.")
    return None



# ---------------------------------------------------------
# PRO PRESENTER
# ---------------------------------------------------------
def trigger_message(num_string):
    cfg = load_config()
    url = f"http://{cfg['PP_HOST']}:{cfg['PP_PORT']}/v1/message/{cfg['MESSAGE_UUID']}/trigger"
    payload = [{"name": "Nachricht", "text": {"text": num_string}}]
    try:
        r = requests.post(url, json=payload, timeout=2)
        return r.status_code
    except:
        return 0


def clear_message(num):
    cfg = load_config()
    url = f"http://{cfg['PP_HOST']}:{cfg['PP_PORT']}/v1/message/{cfg['MESSAGE_UUID']}/clear"
    try:
        r = requests.get(url, timeout=2)
        return r.status_code
    except:
        return 0



# ---------------------------------------------------------
# HTTP SERVER
# ---------------------------------------------------------
class Nuserver(BaseHTTPRequestHandler):

    def _safe_write(self, data: bytes):
        try:
            self.wfile.write(data)
        except:
            pass

    def _send_json(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self._safe_write(json.dumps(data).encode("utf-8"))
        except:
            pass

    def _send_html(self, filename):
        try:
            with open(filename, "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self._safe_write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self._safe_write(b"Not Found")



    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # STATIC FILES
        if path.startswith("/sounds/") or path.startswith("/images/") or path.startswith("/i18n/"):
            local_path = path.lstrip("/")

            if os.path.exists(local_path) and os.path.isfile(local_path):
                self.send_response(200)

                if local_path.endswith(".mp3"):
                    self.send_header("Content-Type", "audio/mpeg")
                elif local_path.endswith(".png"):
                    self.send_header("Content-Type", "image/png")
                elif local_path.endswith(".json"):
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                else:
                    self.send_header("Content-Type", "application/octet-stream")

                self.end_headers()

                try:
                    with open(local_path, "rb") as f:
                        self._safe_write(f.read())
                except:
                    pass
            else:
                self.send_error(404)
            return



        # MAIN
        if path in ["/", "/index.html", "/index2.html"]:
            self._send_html("index2.html")
            return

        if path in ["/admin", "/admin.html"]:
            self._send_html("admin.html")
            return


        # STATE (mit Ultra-PortFix)
        if path == "/state":
            cfg = load_config()
            ok = False
            try:
                r = requests.get(
                    f"http://localhost:{cfg['PP_PORT']}/v1/messages",
                    timeout=0.4
                )
                ok = r.status_code in (200, 204, 207)
            except:
                ok = False

            if not ok:
                new_port = scan_for_pp_port(cfg["PP_PORT"])
                if new_port is not None:
                    cfg["PP_PORT"] = new_port
                    save_config(cfg)
                    ok = True

            state = load_state()
            state["connection"] = "ok" if ok else "fail"
            self._send_json(state)
            return


        # CONFIG
        if path == "/config":
            self._send_json(load_config())
            return

        # TEST CONNECTION
        if path == "/test_connection":
            cfg = load_config()
            try:
                url = f"http://localhost:{cfg['PP_PORT']}/v1/messages"
                r = requests.get(url, timeout=0.4)
                self._send_json({"ok": r.status_code in (200,204,207)})
            except:
                self._send_json({"ok": False})
            return

        # GROUPS
        if path == "/groups":
            self._send_json({"groups": load_config()["GROUPS"]})
            return

        # DEFAULT 404
        self.send_response(404)
        self.end_headers()



    # ---------------------------------------------------------
    # POST
    # ---------------------------------------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # ADD
        if path == "/add":
            num = query.get("num", [""])[0]
            state = load_state()
            if num and num not in state["active"]:
                state["active"].append(num)
                save_state(state)
                trigger_message(",".join(state["active"]))
            self._send_json({"active": state["active"]})
            return

        # REMOVE
        if path == "/remove":
            num = query.get("num", [""])[0]
            state = load_state()
            if num in state["active"]:
                state["active"].remove(num)
                save_state(state)
                if state["active"]:
                    trigger_message(",".join(state["active"]))
                else:
                    clear_message(num)
            self._send_json({"active": state["active"]})
            return

        # CLEAR
        if path == "/clear":
            save_state({"active": []})
            clear_message("ALL")
            self._send_json({"active": []})
            return

        # SAVE CONFIG
        if path == "/save_config":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
                cfg = load_config()
                cfg.update(data)
                save_config(cfg)
                self._send_json({"ok": True})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # SAVE GROUPS
        if path in ["/save_groups", "/groups/save"]:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
                groups = data.get("groups", data)  # fallback
                cfg = load_config()
                cfg["GROUPS"] = groups
                save_config(cfg)
                self._send_json({"ok": True})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # DEFAULT 404
        self.send_response(404)
        self.end_headers()



# ---------------------------------------------------------
# SERVER START
# ---------------------------------------------------------
if __name__ == "__main__":
    port = 8080
    server = ThreadingHTTPServer(("0.0.0.0", port), Nuserver)
    print(f"Server läuft auf http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server beendet.")
