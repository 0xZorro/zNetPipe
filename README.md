# zNetPipe

**zNetPipe** ist ein leichtgewichtiges Python-Tool zum Senden und Empfangen von Dateien über TCP/IP – ohne zusätzliche Bibliotheken, Dienste oder Frameworks. Es simuliert die grundlegende Funktionsweise von `netcat`, erweitert um Dateitransfer und einfache Kommandoverarbeitung. 

Das Tool erlaubt bidirektionale Kommunikation zwischen zwei Endpunkten im selben Netzwerk oder über das Internet – ideal zur Veranschaulichung von Portnutzung, TCP-Verbindungen und einfachem File-Handling.

---

## Features

- Dateiübertragung zwischen zwei Geräten via TCP (ohne externe Tools wie FTP oder SCP)
- Einfache Kommandozeile zur Steuerung (Befehle wie `send`, `status`, `change port`, `exit`)
- Zwei parallele Threads: Ein Thread empfängt Daten (Server), der andere wartet auf Eingabe (Client)
- Unterstützt lokale Tests mit `localhost`, aber auch echte IPs im Netzwerk
- Dynamische Portänderung während der Laufzeit (inkl. Soft-Restart des Servers)

---

## Motivation

Dieses Projekt entstand als praktische Übung zum Thema **Netzwerkkommunikation**, **Socket-Programmierung** und **Portkonfiguration unter Windows**.  
Ziel war es, ein verständliches und portables Werkzeug zu entwickeln, mit dem man auf einfache Weise lernen kann:

- Wie eine TCP-Verbindung aufgebaut wird
- Wie ein Server dauerhaft auf Anfragen wartet
- Wie der Client gezielt Verbindungen aufbaut
- Wie der Datenaustausch über Ports abläuft

Durch den bewussten Verzicht auf Frameworks wie Flask oder Bibliotheken wie `socketserver` bleibt das Konzept transparent und nachvollziehbar.

---

## Voraussetzungen

- Python 3.x (getestet mit 3.10 unter Windows)
- Zwei Geräte im selben Netzwerk (oder zwei CMDs für lokalen Test)
- Kein blockierender Netzfilter (z. B. Portmaster, Windows-Firewall)

---

## Installation & Start

1. Repository klonen oder `zNetPipe.py` herunterladen:
   ```bash
   git clone https://github.com/0xZorro/zNetPipe.git
   ```

2. Öffne zwei Terminals (CMD, PowerShell oder Terminalfenster) – jeweils auf einem Gerät oder lokal.

3. Starte das Tool mit:
   ```bash
   python zNetPipe.py
   ```

4. Beide Instanzen starten automatisch einen Listener (Server) und eine CLI (Client).

5. ### Hinweis zu lokalen Tests

Wenn du **zNetPipe auf einem einzelnen Rechner testen möchtest**, z. B. mit zwei geöffneten CMD-Fenstern, beachte bitte Folgendes:

- Standardmäßig verwendet zNetPipe die IP-Adresse `127.0.0.1` (localhost).
- Beim Start lauscht jede Instanz auf einem TCP-Port – z. B. standardmäßig Port `50000`.
- Auf einem einzelnen Rechner darf jedoch **nicht zweimal derselbe Port belegt werden**, da der Betriebssystem-Socket nur eine Bindung pro Port erlaubt.

####  Lösung für lokale Tests (Cross-Port Setup)

Verwende in den beiden Fenstern unterschiedliche Ports für **Server** und **Client**, zum Beispiel:

```bash
# CMD 1 (erste Instanz)
change port server 50333
change port client 50444

# CMD 2 (zweite Instanz)
change port server 50444
change port client 50333
```

Damit erreichst du:

- Beide Server lauschen auf getrennten Ports (`50333` und `50444`)
- Jeder Client sendet gezielt an den Partnerport (eine sogenannte **Cross-Verbindung**)

#### Hinweis:
Dieses Setup ist **nur bei Tests auf einem einzelnen Gerät notwendig**.  
In einem echten Netzwerk, bei dem sich die Programme auf zwei unterschiedlichen Rechnern befinden, kann derselbe Port (z. B. `50000`) problemlos für beide Seiten verwendet werden.

---

## Befehlsübersicht (CLI-Modus)

- `send <datei>`  
  Sendet eine Datei an den aktuell gesetzten Zielhost und Port.

- `status`  
Zeigt den aktuellen Status von Client-Ziel, Server-Port und Empfängerpfad.

### Beispielausgabe im Terminal (Standardbetrieb):

```bash
>> status
[STATUS]
 Target IP       : 192.168.1.12
 Client port     : 50444
 Server port     : 50333 (active)
 Receive dir     : received
```

### Felder im Überblick:

- **Target IP**: IP-Adresse, an die der Client Daten senden will
- **Client port**: Port, über den der Client aktuell Verbindungen aufbaut
- **Server port**: Der konfigurierte Port, auf dem der Server lauscht – mit Statusanzeige
- **Receive dir**: Verzeichnis, in dem empfangene Dateien gespeichert werden


### Besondere Fälle:

#### Server-Port geändert, aber noch nicht neu gestartet:

```bash
>> status
[STATUS]
 Target IP       : 127.0.0.1
 Client port     : 50444
 Server port     : 50444 (pending, restart required; currently running on 50333)
 Receive dir     : received
```

- `50444` ist der neue konfigurierte Port
- Der Server läuft aber noch auf dem alten Port `50333`
- > Lösung: Starte den Server über das CLI neu (`Restart server now?` nach Portwechsel)


#### Server konnte beim Start nicht gestartet werden:

```bash
>> status
[STATUS]
 Target IP       : 127.0.0.1
 Client port     : 5000
 Server port     : 5000 (not running)
 Receive dir     : received
```

- Das bedeutet, der Server **ist aktuell nicht aktiv** – z. B. wegen Portkonflikt
- > Lösung: Wähle einen anderen Port mit `change port server <PORT>` und starte den Server neu


Die Statusanzeige hilft dabei, jederzeit zu erkennen, ob der Server korrekt läuft oder Konfigurationsprobleme bestehen.

- `change port client <PORT>`  
  Ändert den Zielport des Clients für ausgehende Verbindungen.

- `change port server <PORT>`  
  Setzt den Port des Servers. Erfordert optionalen Neustart.

- `change target <IP>`  
  Ändert die Zieladresse (z. B. bei Tests in anderem Netzwerk).

- `exit`  
  Beendet das Programm sauber (stoppt beide Threads).

---

## Sicherheitshinweise & Einschränkungen

**zNetPipe** wurde ausschließlich zu **Lernzwecken** entwickelt, um ein grundlegendes Verständnis von Netzwerkkommunikation, Portnutzung und Dateitransfer über TCP/IP zu vermitteln.  
Es richtet sich an Einsteiger in den Bereichen **Socket-Programmierung, Protokolle und Netzwerktechnik** – nicht an produktive Umgebungen.

### Sicherheitsrisiken dieses Programms

1. **Keine Authentifizierung**
   - Jeder, der die IP-Adresse und den Port kennt, kann sich verbinden und eine Datei senden.
   - > Gefahr: Unbefugter Zugriff oder Missbrauch im lokalen Netz.

2. **Keine Verschlüsselung**
   - Die übertragenen Daten werden im Klartext übermittelt.
   - > Gefahr: In öffentlichen Netzwerken können Inhalte mitgeschnitten (Man-in-the-Middle) werden.

3. **Keine Prüfung empfangener Inhalte**
   - Empfänger speichert jede Datei ohne Prüfung oder Filter.
   - > Gefahr: Malware oder gefährliche Dateien könnten unbemerkt empfangen werden.

4. **Offener TCP-Port**
   - Der Serverprozess horcht dauerhaft auf einem konfigurierten Port.
   - > Gefahr: Portscanner oder automatisierte Angreifer könnten offene Ports erkennen und angreifen.

5. **Keine Zugriffskontrolle oder Logging**
   - Es gibt keine Mechanismen zur Authentifizierung, Autorisierung oder Protokollierung.
   - > Gefahr: Kein Nachweis bei Missbrauch möglich.
---

## Zukünftige Erweiterungen (Ideen)

- Einführung einer Zugangskontrolle (z. B. Passwort oder Token)
- TLS-Verschlüsselung oder AES für sichere Übertragungen
- Logging von Absender-IP, Dateigröße und Zeitpunkt
- Virenprüfung oder Signaturvalidierung vor dem Speichern
- Zeitgesteuerter Shutdown oder Übertragungslimits
- Kompression großer Dateien oder Streaming-Modus

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.  
Details siehe [LICENSE](LICENSE).

---

## Autor

**Created by Jose Luis Ocana**

Cybersecurity Learner | Python & C++ Tools

(GitHub: [0xZorro](https://github.com/0xZorro))  

TryHackMe: https://tryhackme.com/p/0xZorro

Contact: zorro.jose@gmx.de

---

## Beiträge

Du möchtest mithelfen? Super! Forke das Projekt, nimm Änderungen vor und stelle einen Pull Request.  
Achte bitte darauf, den Verhaltenskodex und die Projektstandards einzuhalten.

---

## Rechtlicher Hinweis

Dieses Tool dient **ausschließlich zu Bildungs- und Demonstrationszwecken** im Bereich Netzwerkkommunikation, Sicherheit und Protokollverständnis.

Die Software wurde entwickelt, um:
- grundlegende Prinzipien der TCP-Kommunikation zu verstehen,
- das Verhalten von Ports, IP-Adressen und Dateiströmen zu analysieren,
- sowie eigene Experimente im lokalen Netzwerk durchzuführen.

### Warnung vor Missbrauch:

Die Verwendung dieses Programms für **nicht autorisierte Datenübertragungen**, **Eindringen in fremde Systeme**, **Umgehung von Sicherheitsmaßnahmen** oder **jegliche Form von Datenexfiltration** ist **strengstens untersagt**.

Solche Aktivitäten verstoßen gegen geltendes Recht und können strafrechtlich verfolgt werden.

---

## Haftungsausschluss

Der Autor übernimmt **keinerlei Verantwortung oder Haftung** für Schäden, Datenverluste, Missbrauch oder rechtliche Konsequenzen, die aus der Nutzung dieser Software resultieren.

Die Nutzung erfolgt **auf eigene Gefahr**.  
Bitte setze dieses Tool **ausschließlich in kontrollierten Testumgebungen** ein – mit Geräten, auf die du legitimen Zugriff hast.

---