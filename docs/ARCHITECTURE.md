# AETHER Architecture (v1.0)

**Approved: 2026-05-08**

## 1. Vision & Goals

**AETHER** turns any camera or video stream into a scientific-grade UAP/UAP-adjacent detection and evidence-capture system.

**Core Goals**:
- Highest possible detection quality with minimal false positives
- “Crisp evidence” — high-fidelity, enhanced, metadata-rich recordings
- Extremely easy deployment (one-click on consumer + edge hardware)
- Full backward/forward compatibility via **BOB Adapter**
- Open source, community-driven, scientifically credible
- Built for the Google for Startups AI Agents Challenge 2026 and future agentic AI events

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AETHER v1.0                               │
├─────────────────────────────────────────────────────────────────┤
│  Ingestion Layer          │  Universal connectors + BOB Adapter │
├─────────────────────────────────────────────────────────────────┤
│  Perception Layer         │  NVIDIA DeepStream (YOLO + Tracking)│
├─────────────────────────────────────────────────────────────────┤
│  Enhancement Layer        │  Super-resolution + Deblur (on track)│
├─────────────────────────────────────────────────────────────────┤
│  Reasoning / Agent Layer  │  Google Gemini + Vertex AI Agent    │
│                           │  (or local LLM fallback)            │
├─────────────────────────────────────────────────────────────────┤
│  Context Fusion Layer     │  ADS-B, satellites, weather, baseline│
├─────────────────────────────────────────────────────────────────┤
│  Storage & Output Layer   │  Rich JSON + high-quality MP4 + UI  │
├─────────────────────────────────────────────────────────────────┤
│  Orchestration & Deploy   │  Docker Compose + Jetson / RPi support│
├─────────────────────────────────────────────────────────────────┤
│  Self-Improving Layer     │  Meta-Agent + Sandbox Tester + Checkpoints │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. Camera/Stream → Ingestion
2. Ingestion → Perception (DeepStream) → raw tracks
3. Raw tracks → Enhancement (only on promising candidates)
4. Enhanced track + context → Reasoning Agent (Gemini)
5. Agent decision → Storage + Alerts + optional multi-station fusion

---

## Self-Improving Layer (New in v1.1+)

AETHER is designed to **continuously improve itself** after open-source release.

### Meta-Agent Responsibilities
- Monitors real-world performance (false positives, user feedback, detection quality)
- Proposes improvements (new rules, prompt tweaks, model fine-tunes)
- Creates **checkpoints** before every change
- Runs proposed changes through **isolated sandbox testing**
- Only promotes changes that measurably improve performance
- Automatic rollback on regression

### Key Components
- `src/aether_meta/meta_agent.py` — Core self-improvement loop
- `sandbox/sandbox_tester.py` — Safe testing environment
- `checkpoints/` — Versioned backups with full state

### Safety & Governance
- All improvements require sandbox validation
- Human review gate for major changes (initially)
- Full audit trail of every accepted/rejected improvement
- Community can contribute improvement proposals via PRs

This makes AETHER one of the first truly **self-evolving open-source scientific instruments**.

## 3. Layer Breakdown

### 3.1 Ingestion Layer
- **Supported sources**: RTSP, ONVIF, USB webcams, HTTP MJPEG, WebRTC, YouTube Live, drone streams
- **BOB Adapter** (critical):
  - Consumes BOB detection events in real time (via webhook or shared queue)
  - Re-processes BOB tracks through AETHER’s full pipeline (reasoning + enhancement)
  - Optionally pushes enriched events back to BOB users or shared dashboard
- Hot-swappable configuration via YAML

### 3.2 Perception Layer (NVIDIA DeepStream Core)
- **Primary model**: Fine-tuned YOLOv10 or RT-DETR (sky-optimized)
- **Tracker**: ByteTrack (or custom SORT variant)
- **Multi-stream support**: Up to 8–16 concurrent 1080p/4K streams on Jetson Orin
- Generated almost entirely via **NVIDIA DeepStream Coding Agents** (Claude Code + reusable Skills)

**Key plugins** (custom):
- Sky-specific post-processing (altitude-aware filtering)
- Motion vector analysis for Tier 1/2 kinematic checks

### 3.3 Enhancement Layer
Triggered only on Tier 2+ candidates:
- Video super-resolution (Real-ESRGAN / latest open models)
- Motion deblur + stabilization
- Optional secondary high-res crop from PTZ camera (if available)
- Output: “crisp” track clip ready for agent review and archival

### 3.4 Reasoning / Agent Layer (The “Brain”)
**Primary**: Google Gemini 2.x + Vertex AI Agent Builder (or ADK)
**Fallback**: Local Llama-3.1-405B / Gemma-2 / Claude 3.5 via API

**Agent capabilities**:
- Multimodal input (video track + JSON kinematics + context)
- Tool calling (ADS-B lookup, satellite predictor, weather API)
- Structured output (confidence score + justification + recommended action)
- Explainability (full reasoning trace stored with event)

This layer is explicitly designed to be **agentic** and perfect for Google’s AI Agents Challenge.

### 3.5 Context Fusion Layer
- Public ADS-B APIs (OpenSky, etc.)
- Satellite pass prediction (Skyfield / current TLEs)
- Weather API (OpenWeatherMap or local)
- Per-camera learned “normal sky” baseline model (updated daily)
- Optional: NOTAMs, military exercise calendars, launch schedules

### 3.6 Storage & Output Layer
- **Events DB**: PostgreSQL + TimescaleDB (time-series optimized)
- **Media**: S3-compatible object storage (high-quality MP4 + thumbnails)
- **Standardized schema**: See CRITERIA.md
- **Dashboard**: Modern web UI (Gradio or custom React) showing live tracks, confidence heatmaps, event history
- **Alerts**: Webhooks, Discord/Telegram/Slack, email, optional central aggregation server

### 3.7 Orchestration & Deployment
- **Primary**: Docker Compose (single `docker-compose up`)
- **Edge targets**: NVIDIA Jetson Orin / AGX, Raspberry Pi 5 + Hailo-8L, Intel NUC
- **Cloud option**: GCP (Vertex AI) or AWS with GPU instances
- One-click install scripts for common hardware

## 4. BOB Connectivity (First-Class Citizen)

**Design principle**: Never abandon existing BOB users.

**Implementation**:
- Dedicated `bob_adapter/` module
- Real-time ingestion of BOB events (REST + WebSocket)
- Full re-processing through AETHER perception + agent layers
- Optional “enrichment” output back to BOB format
- Migration path documented: “Run AETHER alongside BOB → gradually replace perception layer”

This gives the community immediate value while we modernize the stack.

## 5. Security, Privacy & Ethics
- All processing can run **fully locally** (no cloud required)
- No video uploaded unless user explicitly enables central aggregation
- Clear data retention policies (user-configurable)
- Transparent confidence scoring and reasoning (no black box)
- Designed for scientific collaboration, not surveillance

## 6. Extensibility
- Plugin system for new detectors, trackers, or reasoning agents
- Custom criteria via YAML + prompt templates
- Easy addition of new data sources (radar, acoustic, etc. in future versions)

## 7. Alignment with Roadmap

| Phase | Focus                          | Key Deliverables                     |
|-------|--------------------------------|--------------------------------------|
| 0     | Design                         | This doc + CRITERIA.md               |
| 1     | Core Pipeline                  | DeepStream pipeline (NVIDIA agents)  |
| 2     | Agentic Brain                  | Gemini agent + full criteria         |
| 3     | Crisp + Hardening              | Enhancement + FP reduction           |
| 4     | Polish & Challenge             | Dashboard + Google Agents Challenge entry |
| 5     | Community                      | Open source + BOB integration push   |

---

**Status**: Locked for Phase 1 implementation.  
**Next immediate actions**: Create GitHub repository + generate first code via exact prompts.

---

*This architecture was designed for maximum scientific credibility, ease of deployment, and long-term community ownership.*