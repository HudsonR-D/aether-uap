# AETHER — Autonomous Anomalous Event Tracker & High-fidelity Evidence Recorder

**Any camera or stream → Real-time detection → Crisp, scientifically useful evidence. Open source.**

AETHER is the open-source agent that turns **any camera or video stream** into a scientific-grade UAP / anomalous sky phenomenon detection and evidence-capture system.

We solve the "crisp video problem" by combining:
- NVIDIA DeepStream for high-performance perception
- Google Gemini / Vertex AI for agentic reasoning
- Modern super-resolution & enhancement
- First-class integration with existing projects like BOB

**Plus one revolutionary feature**: AETHER is **self-improving**. A dedicated Meta-Agent continuously analyzes real-world performance, proposes improvements, tests them safely in an isolated sandbox, and only promotes changes that measurably improve results — with full checkpoints and automatic rollback.

## 🚀 Quick Start

```bash
git clone https://github.com/aether-uap/aether-uap.git
cd aether-uap
docker compose up
```

> **Note**: This is currently a rapid prototype (v0.9.0). Full production deployment guide and pre-built Docker images coming in v1.0.

## Key Features (v1.1 — Self-Improving)

- **Universal ingestion** — RTSP, USB, HTTP, WebRTC, YouTube, drone feeds + BOB adapter
- **Tiered anomaly detection** — Extremely low false positives with rich justification
- **Crisp evidence** — Automatic super-resolution + deblur on high-confidence tracks
- **Agentic reasoning** — Google Gemini-powered decisions with explainability
- **Multi-station ready** — Built for network triangulation from day one
- **One-click deployment** — Docker Compose + Jetson / Raspberry Pi 5 support
- **Self-Improving Core** — Meta-Agent + Sandbox Tester + Continuous Learning Pipeline + automatic checkpoints & rollback

## The Self-Improving Vision

AETHER doesn’t just detect anomalies — it **gets better every week** through real-world usage:

1. Deployed instances (with user consent) send anonymized, high-signal events back to the project.
2. The Meta-Agent analyzes performance and proposes improvements (better thresholds, refined prompts, new model fine-tunes).
3. Every proposed change is tested in an isolated sandbox against regression tests and real data.
4. Only improvements that clearly help are promoted — with full versioned checkpoints and automatic rollback if anything goes wrong.
5. The community can contribute improvement proposals via pull requests.

This makes AETHER one of the first truly **living, self-evolving open-source scientific instruments**.

## Documentation

- [Architecture](./docs/ARCHITECTURE.md) — Now includes Self-Improving Layer
- [Detection Criteria](./docs/CRITERIA.md)
- [Implementation Prompts](./prompts/PROMPTS.md)
- [Meta-Agent Prompt](./prompts/META_AGENT_PROMPT.md) — Use this to improve the Meta-Agent itself

## Open Source Status

**Phase 0–1 complete** (May 2026)

We are currently finalizing the self-improving infrastructure. Once complete, we will:

- Open the repository publicly
- Publish the full technical architecture and Meta-Agent prompt
- Launch a call for contributors (especially hardware testers, prompt engineers, and UAP researchers)
- Submit to the Google for Startups AI Agents Challenge 2026

**Want to be part of the first wave?** Star the repo and join the discussion when it opens.

## Project Status

**Phase 0 complete** — Architecture & criteria locked (May 2026)

**Current phase**: Core perception pipeline generation

## Contributing

We welcome contributors of all skill levels. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT License — see [LICENSE](./LICENSE)

## Vision

In 2026 we have the technology to capture **clear, verifiable, scientifically useful** UAP evidence at scale.  
AETHER exists to make that happen — openly, transparently, and collaboratively.

---

**Built with ❤️ for truth-seeking and scientific discovery.**