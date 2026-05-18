File: SKILLS.md
Markdown# AETHER Skills & Capabilities

**Welcome to AETHER** — the open-source, self-improving UAP/UFO detection & evidence system.

This document is written as if you’re a new team member joining the project. It tells you everything you need to know to get started and operate the system effectively.

---

## 🎯 Core Purpose

AETHER turns **any camera or video stream** into a smart, always-on sky monitoring station that:
- Detects anomalous objects in real time
- Filters out normal objects (planes, birds, Starlink, balloons, etc.)
- Automatically enhances footage for maximum clarity
- Learns and improves itself over time
- Produces scientifically useful, high-quality evidence

---

## 🚀 Quick Start Skills (Day 1)

### 1. Deploy AETHER
```bash
git clone https://github.com/HudsonR-D/aether-uap.git
cd aether-uap
docker compose up --build -d
Everything (perception engine, reasoning agent, dashboard, and self-improving Meta-Agent) will start automatically.
2. Connect Your First Video Feed / Camera
Option A — RTSP Camera (Recommended)

Copy config.yaml.example to config.yaml
Add your camera:

YAMLsources:
  backyard_cam:
    type: rtsp
    url: rtsp://username:password@192.168.1.100:554/stream1
    location: "Denver, CO - Backyard"
    orientation: "North-East"

Restart the perception service:

Bashdocker compose restart perception
Option B — USB Webcam
YAMLsources:
  usb_cam:
    type: usb
    device: /dev/video0
Option C — YouTube or HTTP Stream
YAMLsources:
  public_stream:
    type: http
    url: https://www.youtube.com/watch?v=...

🛠️ Core Skills You Can Use Immediately
Detection & Tracking

Watch the sky 24/7 and flag anything unusual
Only alert on objects faster than 300 m/s or showing non-ballistic movement
Automatically ignore all commercial aircraft using live ADS-B data

Crisp Evidence Generation

Automatically run super-resolution + stabilization on promising tracks
Save high-quality video clips with rich metadata (JSON)
Generate best-frame thumbnails for quick review

Self-Improvement

The Meta-Agent continuously reviews performance
It proposes improvements, tests them safely in a sandbox, and only deploys if they’re better
Give feedback on events (👍 / 👎) — the system gets smarter from your input

Multi-Camera & Collaboration

Add as many cameras as your hardware supports
Automatic triangulation when multiple stations see the same object


Daily Operations (New Team Member Checklist)

Check the Dashboard
Open http://localhost:8080 (or your server IP)
Review Recent Events
High-confidence detections show:
Confidence score (0–100)
Plain-English justification
Enhanced video clip

Give Feedback
Use 👍 or 👎 on events — this directly trains the system.
Monitor Self-Improvement
Occasionally check the Meta-Agent logs to see what it’s optimizing.


Advanced Skills

Tune detection sensitivity through natural language or config
Add new anomaly types by extending docs/CRITERIA.md
Integrate with existing BOB installations using the built-in adapter
Run services individually without Docker (see README.md)


How to Talk to AETHER (Natural Language)
The reasoning agent understands plain English. Examples:

“Be more strict on false positives during daytime”
“Prioritize objects that hover then accelerate rapidly”
“Only create public alerts on confidence > 85”


Need Help?

Check the docs/ folder
Open an issue on GitHub
The system is built to be easy to extend and improve
You are now ready to operate AETHER.
Connect a camera → let it run → watch it get smarter every week.
Welcome to the team. 🛸
