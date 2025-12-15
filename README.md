# NurseryCall

A lightweight, self-hosted call system for church nursery / kids ministry environments.  
Designed to run on the same Mac as ProPresenter and display active call numbers on tablets or phones.

---

<img width="2984" height="1094" alt="NurseryCall Screenshot" src="https://github.com/user-attachments/assets/19938c51-fa2f-42e5-ba6d-7ffab0501cfa" />

<img width="338" height="177" alt="Bildschirmfoto 2025-12-15 um 17 20 42" src="https://github.com/user-attachments/assets/551f1412-77e6-41b3-872b-a4fa26009714" />

---

## ✨ Features

### 🔔 Live Call Display

* Send child call numbers (e.g. **R22**, **K5**) directly to ProPresenter
* Tablets update instantly and show all active calls
* Calls can be removed with a single tap
* No need for the ProPresenter operator to click anything
* Optional sound feedback for success / error

---

### 👶 Dynamic Group Management

* Create, edit, and delete groups in the Admin Panel
* Each group has:
  * **Name** (e.g. “Little Sharks”)
  * **Prefix** (e.g. “R”)
  * **Button Style** (1–10 predefined gradient styles)
* Index page automatically updates to show all active groups
* No hard-coded groups in the client

---

### 🎨 Simple & Beautiful UI

* Clean gradient background
* Large, touch-friendly buttons
* Clear active-call tiles with matching group colors
* Optimized for iPads and Android tablets

---

### 🖥 Admin Panel

* Tabs: **Live**, **Settings**, **Groups**
* Live overview of all active calls
* Remove individual calls or clear all
* Test ProPresenter connection
* Edit ProPresenter host, port and message UUID
* Fully dynamic group management

---

### 🔌 ProPresenter Auto-Port Detection

* ProPresenter changes its API port frequently
* The server automatically detects the *actual* ProPresenter API port
* Scans the range **1000–50000** only when needed
* Saves the correct port permanently
* Never overwrites a working port
* No downtime when ProPresenter restarts

---

### 💾 Persistent Storage

* `config.json`
  * ProPresenter connection
  * Message UUID
  * Group definitions
* `state.json`
  * List of currently active calls
* Both files are updated automatically

---

### 🧱 Fully Offline-Capable

* No cloud dependencies
* Runs entirely on the ProPresenter Mac
* Tablets connect via local LAN / WiFi

---

### 🌎 Multi-Language Support

* Client and Admin UI support multiple languages
* Translations are stored in external JSON files
* No rebuild or code changes required to add a new language
* Language is selected via URL parameter
* Automatic fallback to default language if a translation is missing

**Example languages:**
* German (`de`)
* English (`en`)

Additional languages can be added by placing a new JSON file in `/i18n`.

---

### 🧭 Group Preselection via URL (Perfect for QR Codes)

* Clients can preselect a specific children’s group using a URL parameter
* Useful for:
  * Dedicated tablets per group
  * QR codes at check-in desks
  * Fixed devices in specific rooms
* No manual group selection required

---

## 🛠 Requirements

* macOS (same machine running ProPresenter)
* Python 3.9+
* ProPresenter 7 with an active **Message** (With token named "Nachricht") <- this part is important
* Local network (LAN / WiFi) for tablets

---


## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone <your_repo_url>
   cd NurseryCall
   ```

2. **Install dependencies:**

   ```bash
   pip3 install requests
   ```

3. **Run the server manually (for testing):**

   ```bash
   python3 server_v2.py
   ```

   The server starts at:

   ```
   http://localhost:8080
   ```

4. **Open the Client UI:**

   ```
   http://<Mac-IP>:8080/
   ```

5. **Open the Admin Panel:**

   ```
   http://<Mac-IP>:8080/admin
   ```

---

## 🔧 Startup on macOS (LaunchAgent)

1. Copy the provided `.plist` into:

   ```
   ~/Library/LaunchAgents/
   ```

2. Load it:

   ```bash
   launchctl load ~/Library/LaunchAgents/church.nurserycall.server.plist
   ```

3. Start the service:

   ```bash
   launchctl start church.nurserycall.server
   ```

After this, the server starts **automatically when the Mac boots**.

---

## 🧩 Configuration (config.json)

Example:

```json
{
  "PP_HOST": "localhost",
  "PP_PORT": 20562,
  "MESSAGE_UUID": "YOUR-UUID-HERE",
  "GROUPS": [
    { "name": "Rasselbande", "prefix": "R", "style": 1 },
    { "name": "Königskinder", "prefix": "K", "style": 2 }
  ]
}
```

All values can be updated via the Admin Panel.

## ✉️ Setup in Propresenter

Set up a message with your preferred theme.
Then: Create a token called "Nachricht" and add that to the message details.

---
## 🌎 Language Selection
The language is selected using a URL parameter.

Examples:

* http://YOUR-IP-ADRESS:8080/?lang=en
* http://YOUR-IP-ADRESS:8080/?lang=de

How it works

The client loads translations from:
/i18n/<lang>.json
If the file does not exist or is invalid:
The UI falls back to German
Static default texts remain visible
If no language is specified, the browser language is used as fallback

---

## 👶 Group Preselection via URL
Clients can automatically preselect a group using the group prefix.

Example:

http://YOUR-IP-ADRESS:8080/?group=R

This will:
* Load the client UI
* Automatically select the group with prefix R
* Highlight the corresponding group button

### Combine Language + Group
* http://YOUR-IP-ADRESS:8080/?lang=en&group=K

This is ideal for:
* QR codes per group
* Tablets permanently assigned to one kids group
* Volunteers with minimal interaction

### 🧾 Example: QR Code Setup
Tablet for the KingsKids group (prefix K) in English:
* http://YOUR-IP-ADRESS:8080/?lang=en&group=K
Scan once → bookmark → ready to use.

---

## 🔍 Troubleshooting

### Cannot connect to ProPresenter?

* Check ProPresenter’s network settings
* Ensure ProPresenter is running
* Try using “Test Connection” in Admin Panel
* The server auto-fixes incorrect ports

### Calls not showing?

* Check WiFi connection
* Refresh the page
* Look at server logs:

  ```bash
  tail -f server_error.log
  ```

### Admin shows no groups?

* Your config.json may be missing the `"GROUPS"` field
* Saving once in Admin regenerates defaults

---

## 📄 License

MIT License

---

## ❤️ Credits

Built for a real-world church environment.
Optimized for clarity, reliability, and ease of use.
