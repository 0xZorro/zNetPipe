import socket
import threading
import os
import time

# === Default settings ===
DEFAULT_PORT = 50000
BUFFER_SIZE = 4096
RECV_DIR = "received"

# === Runtime variables ===
target_ip = "127.0.0.1"
client_port = DEFAULT_PORT
server_port = DEFAULT_PORT
active_server_port = None
server_restart_required = False
running = True
server_running = True

# === Ensure receive directory exists ===
os.makedirs(RECV_DIR, exist_ok=True)

# === Server Thread: listens for incoming files ===
def start_server():
    global server_port, active_server_port,server_running, running
    
    try:
            
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow immediate reuse of the port after shutdown to prevent 'address already in use' errors
        server.bind(("", server_port))
        active_server_port = server_port
        server.listen(1)
        server.settimeout(1.0)  # Timeout setzen für saubere while-Schleife   

        print(f"[LISTENING] Waiting for file on port {server_port}...")  
            
        while running and server_running:
            try:
                conn, addr = server.accept()
                print(f"[CONNECTED] From {addr[0]}:{addr[1]}")

                with conn:
                    try:    
                        filename = conn.recv(BUFFER_SIZE).decode()
                        if not filename or filename == "\0":
                            print("[INFO] Empty or null-trigger received – skipping")
                            continue
                        # file receive
                        filepath = os.path.join(RECV_DIR, filename)
                        with open(filepath, "wb") as f:
                            while True:
                                data = conn.recv(BUFFER_SIZE)
                                if not data:
                                    break
                                f.write(data)
                        print(f"[RECEIVED] File saved as: {filepath}")
                    except Exception as e:
                        print(f"[ERROR] Server inner: {e}")
            except socket.timeout:
                continue  # Nach Timeout wieder in die Schleife zurück
            except Exception as e:
                print(f"[ERROR] Server outer: {e}")
                break
    except Exception as e:
        active_server_port = None
        print(f"[ERROR] Server startup: {e}")



# === CLI Thread: waits for user input ===
def start_cli():
    global target_ip, client_port, server_port, running, server_restart_required
    while running:
        try:
            cmd = input(">> ").strip()
            if cmd.startswith("target "):
                target_ip = cmd.split(" ", 1)[1]
                print(f"[SET] Target IP set to {target_ip}")
                if target_ip == "127.0.0.1":
                    print("[WARNING] Running on localhost – avoid using the same port for both instances.")
            elif cmd.startswith("port "):
                p = int(cmd.split(" ", 1)[1])
                client_port = server_port = p
                print(f"[SET] Both client and server ports set to {p}")
            elif cmd.startswith("change port server "):
                server_port = int(cmd.split(" ")[-1])
                server_restart_required = True
                print(f"[SET] Server port changed to {server_port} (A restart is required)")
                resp = input("Restart server now? (yes/no): ").strip().lower()
                if resp in ["yes", "y"]:
                    restart_server()
                    server_restart_required = False
            elif cmd.startswith("change port client "):
                client_port = int(cmd.split(" ")[-1])
                print(f"[SET] Client target port changed to {client_port}")
            elif cmd == "status":
                print(f"[STATUS]")
                print(f" Target IP       : {target_ip}")
                print(f" Client port     : {client_port}")
                print(f" Server port     : {server_port}", end="")
                if active_server_port is None:
                    print(" (not running)")
                elif server_port != active_server_port:
                    print(f" (pending, restart required; currently running on {active_server_port})")
                else:
                    print(" (active)")
                print(f" Receive dir     : {RECV_DIR}")
            elif cmd == "exit":
                print("[EXIT] Shutting down...")
                running = False
                break
            elif cmd == "help":
                print("Available commands:")
                print(" target <IP>")
                print(" port <port>                   - set both client/server port")
                print(" change port server <port>    - set only server port")
                print(" change port client <port>    - set only client port")
                print(" send <filename>")
                print(" status")
                print(" exit")
                print(" help")
            elif cmd.startswith("send "):
                filename = cmd.split(" ", 1)[1]
                if not os.path.exists(filename):
                    print(f"[ERROR] File not found: {filename}")
                    continue
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                        client.connect((target_ip, client_port))
                        client.sendall(os.path.basename(filename).encode())
                        time.sleep(0.1)               # give server time to get ready
                        with open(filename, "rb") as f:
                            while True:
                                data = f.read(BUFFER_SIZE)
                                if not data:
                                    break
                                client.sendall(data)
                        print(f"[SENT] File '{filename}' sent to {target_ip}:{client_port}")
                except Exception as e:
                    print(f"[ERROR] Send failed: {e}")
            else:
                print("[UNKNOWN COMMAND] Type 'help' to see options.")
        except Exception as e:
            print(f"[ERROR] CLI: {e}")


# === Restart the server thread with new port ===
def restart_server():
    global server_thread, server_port, active_server_port, server_running 

    print("[RESTART] Restarting server...")

    # 1. Stop old server thread by setting 'running' to False
    server_running  = False
    server_thread.join(timeout=2)

    # 2. Set running = True again so the new server can loop
    server_running  = True

    # 3. Create a new server thread
    server_thread = threading.Thread(target=start_server, daemon=True)

    # 4. Start it
    server_thread.start()

    # 5. Log and confirm
    print(f"[RESTARTED] Server is now listening on port {server_port}")




# === Start threads ===
if __name__ == "__main__":
    print("=== zNetPipe Started ===")

    # Warnung bei localhost direkt beim Start
    if target_ip == "127.0.0.1":
        print("[WARNING] Running on localhost – avoid using the same port for both instances.")
        print("          For testing, use a cross-port setup with 'change port server <X>' and 'change port client <Y>'.")

    cli_thread = threading.Thread(target=start_cli, daemon=True)
    server_thread = threading.Thread(target=start_server, daemon=True)

    server_thread.start()
    cli_thread.start()
    
    cli_thread.join()
    server_thread.join()
    print("=== zNetPipe Stopped ===")
