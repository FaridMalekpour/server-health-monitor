# Server Health Monitor

## 🚀 Overview
Server Health Monitor is a **lightweight monitoring tool** that tracks system performance and sends alerts via **Telegram, Slack, or Webhooks** when resource usage crosses a defined threshold.

## 🔧 Features
- ✅ Monitor **CPU, RAM, Disk, and Network usage**
- ✅ Set **custom alerts** for high resource consumption
- ✅ Send notifications via **Telegram, Slack, or Email**
- ✅ Simple **CLI interface** for setup & usage
- ✅ Easy deployment via **Docker or Python script**

## 📦 Installation
### Prerequisites
- Python 3.8+
- `pip install -r requirements.txt`

### Clone the Repository
```bash
git clone https://github.com/FaridMalekpour/server-health-monitor.git
cd server-health-monitor
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage (The app is not ready to use yet)
### Run the Monitor
```bash
python monitor.py
```

### CLI Options
```bash
python monitor.py --cpu --ram --disk
```

## ⚙️ Configuration
Edit the `config.json` file to set alert thresholds and notification preferences.

## 📡 API Endpoints (Planned)
| Method | Endpoint | Description |
|--------|------------|-------------|
| GET | `/status` | Get system health stats |
| GET | `/docs` | Get API docs in Swagger |
| POST | `/set_alerts` | Configure alert thresholds |

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
🔧 **Work in Progress** - More features coming soon!