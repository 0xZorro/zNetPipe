<p align="center">
  <img src="Banner.png" alt="zNetPipe" width="300"/>
</p>

# zNetPipe

**zNetPipe** is a lightweight Python tool for sending and receiving files over TCP/IP – without additional libraries, services, or frameworks. It simulates the basic functionality of `netcat`, extended with file transfer and simple command handling.

The tool allows bidirectional communication between two endpoints in the same network  – ideal for demonstrating port usage, TCP connections, and basic file handling.

---

## Features

- File transfer between two devices via TCP (without external tools like FTP or SCP)
- Simple command-line interface (commands like `send`, `status`, `change port`, `exit`)
- Two parallel threads: one receives data (server), the other waits for input (client)
- Supports local tests with `localhost`, as well as real IPs in a network
- Dynamic port change at runtime (including soft-restart of the server)

---

## Motivation

This project was created as a practical exercise in **network communication**, **socket programming**, and **port configuration under Windows**.  
The goal was to build a simple and portable tool that helps understand:

- How a TCP connection is established
- How a server continuously listens for incoming connections
- How the client builds targeted connections
- How data is exchanged over ports

By deliberately avoiding frameworks like Flask or libraries like `socketserver`, the concept remains transparent and easy to follow.

---

## Requirements

- Python 3.x (tested with 3.10 on Windows)
- Two devices in the same network (or two CMDs for local testing)
- No blocking network filter (e.g. Portmaster, Windows Firewall)

---

## Installation & Start

1. Clone the repository or download `zNetPipe.py`:
   ```bash
   git clone https://github.com/0xZorro/zNetPipe.git
   ```

2. Open two terminals (CMD, PowerShell, or terminal windows) – either on separate devices or locally.

3. Start the tool with:
   ```bash
   python zNetPipe.py
   ```

4. Both instances automatically start a listener (server) and a CLI (client).

5. ### Note on Local Testing

If you're testing **zNetPipe on a single machine**, e.g. with two opened CMD windows, consider the following:

- By default, zNetPipe uses the IP address `127.0.0.1` (localhost).
- Each instance listens on a TCP port – default is `50000`.
- On a single machine, **you cannot bind the same port twice** – the OS only allows one binding per port.

#### Solution for Local Testing (Cross-Port Setup)

Use different ports for **server** and **client** in each window, for example:

```bash
# CMD 1 (first instance)
change port server 50333
change port client 50444

# CMD 2 (second instance)
change port server 50444
change port client 50333
```

This achieves:

- Both servers listen on separate ports (`50333` and `50444`)
- Each client sends to the partner's port (a **cross-connection** setup)

#### Note:
This setup is **only needed for local tests on one machine**.  
In a real network, where programs run on two separate devices, using the same port (e.g. `50000`) is perfectly fine.

---

## Command Overview (CLI Mode)

- `send <file>`  
  Sends a file to the currently configured target host and port.

- `status`  
  Displays the current status of client target, server port, and receiving directory.

### Example Output (default setup):

```bash
>> status
[STATUS]
 Target IP       : 192.168.1.12
 Client port     : 50444
 Server port     : 50333 (active)
 Receive dir     : received
```

### Fields Explained:

- **Target IP**: IP address the client wants to send data to
- **Client port**: Port currently used by the client to connect
- **Server port**: Port configured for the server to listen on – includes status info
- **Receive dir**: Directory where incoming files are saved

### Special Cases:

#### Server port changed but not yet restarted:

```bash
>> status
[STATUS]
 Target IP       : 127.0.0.1
 Client port     : 50444
 Server port     : 50444 (pending, restart required; currently running on 50333)
 Receive dir     : received 
```

- `50444` is the newly configured port
- Server is still listening on the old port `50333`
- > Solution: Restart the server via CLIENT when prompted (`Restart server now?`)

#### Server couldn't start:

```bash
>> status
[STATUS]
 Target IP       : 127.0.0.1
 Client port     : 5000
 Server port     : 5000 (not running)
 Receive dir     : received
```

- Indicates the server **is not running** – possibly due to a port conflict
- > Solution: Set a new port using `change port server <PORT>` and restart

The status view helps identify server issues or misconfigurations at a glance.

- `change port client <PORT>`  
  Changes the client's target port for outgoing connections.

- `change port server <PORT>`  
  Sets the server's listening port. Requires optional restart.

- `change target <IP>`  
  Changes the target IP address (e.g. when testing in another network).

- `exit`  
  Gracefully shuts down the program (stops both threads).

---

## Security Notice & Limitations

**zNetPipe** was developed strictly for **educational purposes**, to teach basic TCP/IP file transfer, network communication, and socket usage.  
It is intended for learners interested in **network protocols, port management, and socket programming** – not for production environments.

### Security Risks

1. **No Authentication**
   - Anyone who knows the IP and port can connect and send files.
   - > Risk: Unauthorized access or abuse in local networks.

2. **No Encryption**
   - All data is transferred in plain text.
   - > Risk: Interception in public networks (Man-in-the-Middle).

3. **No Content Validation**
   - The receiver stores all incoming files without inspection.
   - > Risk: Malware or harmful files could be received.

4. **Open TCP Port**
   - The server constantly listens on a configured TCP port.
   - > Risk: Port scanners or bots could detect and target it.

5. **No Access Control or Logging**
   - No built-in authorization or logging system.
   - > Risk: No traceability in case of misuse.

---

## Future Enhancements

- Access control (password or pre-shared token)
- TLS or AES encryption for secure transfers
- Logging of IP, filename, and timestamp
- Antivirus check or signature validation before saving
- Auto-shutdown after timeout or transfer limit
- Optional compression or streaming support

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Author

**Created by Jose Luis Ocana**

Cybersecurity Learner | Python & C++ Tools

(GitHub: [0xZorro](https://github.com/0xZorro))  

TryHackMe: https://tryhackme.com/p/0xZorro

Contact: zorro.jose@gmx.de

---

## Contributing

Want to contribute? Awesome! Fork the repo, make your changes, and open a pull request.  
Please follow the project standards and code of conduct.

---

## Legal Notice

This tool is intended **strictly for educational and demonstrative purposes** in the context of network communication, security, and protocol learning.

It was developed to:
- understand basic TCP connection principles
- analyze port behavior, IP addressing, and data streams
- allow safe experimentation in local networks

### Warning Against Misuse:

Using this program for **unauthorized file transfers**, **intrusion attempts**, **security bypassing**, or **data exfiltration** is **strictly prohibited**.

Such actions may violate laws and can lead to legal consequences.

---

## Disclaimer

The author assumes **no responsibility or liability** for damages, data loss, abuse, or legal issues resulting from the use of this software.

Use it **at your own risk**.  
Only use it in **controlled environments and on systems you own or have permission to use**.

---

<p align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
</p>

---
