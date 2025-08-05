# GooglePhish 🛡️🎣

GooglePhish is a **phishing simulation tool** designed for **educational purposes**, **ethical penetration testing**, and **security awareness training**. It sets up a local fake Google login page and tunnels it using **ngrok** to simulate real-world phishing scenarios. Captured credentials are stored in a local **SQL database** for analysis and demonstration purposes.

⚠️ **Disclaimer**  
This tool is intended **ONLY** for **ethical hacking**, **red team exercises**, **security research**, and **educational demonstrations**. Unauthorized usage against individuals or organizations is illegal and unethical. The developer is **not responsible for any misuse** of this project.

---

## 🧑‍💻 Features
- Local fake **Google login page**.
- Ngrok tunnel to expose to the internet.
- Logs credentials into a **SQLite database**.
- Simple and modular codebase for learning purposes.
- CLI-based server setup.

---

## 🛠️ Requirements
- Python 3.x
- Flask
- SQLite3
- Ngrok account (for tunnels)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/googlephish.git
cd googlephish
python app.py
