# NurseryCall

A lightweight, self-hosted call system for church nursery / kids ministry environments.
Designed to run on the same Mac as ProPresenter and display active call numbers on tablets or phones.

---

<img width="2730" height="1116" alt="Bildschirmfoto 2025-12-15 um 12 56 22" src="https://github.com/user-attachments/assets/38f4ce2b-d199-4705-b852-57475ecb7aa7" />


## ✨ Features

### 🔔 Live Call Display

* Send child call numbers (e.g. **R22**, **K5**) to ProPresenter
* Tablets update instantly and show all active calls
* Calls can be removed with a single tap
* No need for the ProPresenter operator to click anything
* Optional sound feedback for success/error

### 👶 Dynamic Group Management

* Create, edit, and delete groups in the Admin Panel
* Each group has:

  * **Name** (e.g. “Little Sharks”)
  * **Prefix** (e.g. “s”)
  * **Button Style** (1–10 predefined gradient styles)
* Index page automatically updates to show all active groups
* No hard-coded groups in the client

### 🎨 Simple & Beautiful UI

* Gradient background
* Large responsive buttons
* Clear active-call tiles with matching group colors
* Ideal for iPads or Android tablets

### 🖥 Admin Panel

* Tabs: **Live**, **Settings**, **Groups**
* Manage connected clients
* Test ProPresenter connection
* Edit ProPresenter host, port and message UUID
* Live preview of active calls
* Manage all groups dynamically

### 🔌 ProPresenter Auto-Port Detection

* ProPresenter changes its API port frequently
* The server automatically detects the *real* PP port
* Scans **range 1000–50000** only when needed
* Saves the correct port permanently
* Never overwrites with a wrong port
* No downtime when PP restarts

### 💾 Persistent Storage

* `config.json`: ProPresenter connection + groups
* `state.json`: list of currently active calls
* Both updated automatically

### 🧱 Fully Offline-Capable

* No cloud dependencies
* Runs entirely on your ProPresenter Mac
* Tablets connect over local network

---

## 🛠 Requirements

* macOS (same machine running ProPresenter)
* Python 3.9+
* ProPresenter 7 with an active **Message** configured
* LAN/WiFi connection for tablets

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
