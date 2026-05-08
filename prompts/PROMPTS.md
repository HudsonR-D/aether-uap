# AETHER — Exact Implementation Prompts (v1.0)

**Copy-paste these directly** into the respective AI coding agents.

---

## 1. NVIDIA DeepStream Coding Agent — Core Perception Pipeline

**Prompt for NVIDIA DeepStream Coding Agent (Claude Code + Skills or equivalent):**

```
You are an expert NVIDIA DeepStream engineer. Create a complete, production-ready DeepStream 7.x Python pipeline for AETHER (open-source UAP sky monitoring agent).

Requirements:
- Ingest multiple RTSP/USB/HTTP streams from a YAML config file
- Use YOLOv10 or RT-DETR model (provide ONNX export instructions if needed)
- Primary inference + ByteTrack or custom SORT tracking
- Output: NvDsMeta with bounding boxes, track IDs, confidence, class
- Add custom post-processing plugin that calculates:
  - Instantaneous and average speed (using camera calibration if available)
  - Acceleration and direction change
  - Basic kinematic flags (high speed, high accel, non-ballistic)
- Multi-stream support (at least 4–8 concurrent 1080p streams)
- GStreamer pipeline with nvinfer, nvtracker, nvdsosd, and file sink for candidate clips
- Clean, well-commented Python code using the official DeepStream Python bindings
- Include a simple config.yaml example with 2–3 sample RTSP sources
- Add logging and basic performance metrics (FPS per stream)

Generate the full project structure:
aether-perception/
├── main.py
├── config.yaml
├── deepstream_app.py
├── custom_postprocess.py
├── requirements.txt
└── README.md

Make it ready to run with `python main.py --config config.yaml` on a Jetson or desktop with NVIDIA GPU + DeepStream SDK installed.
```

---

## 2. Google Gemini / Vertex AI Agent Builder — Reasoning Layer + Tool Calling

**Prompt for Google Gemini (or Vertex AI Agent Builder / ADK):**

```
You are building the "Reasoning Agent" for AETHER, an open-source UAP detection system.

Create a production-grade multimodal agent using Google Gemini 2.x + tool calling.

The agent must:
1. Accept input: 
   - JSON track data (position history, velocity, acceleration, duration, maneuver_type)
   - Cropped video clip (or base64 frames)
   - Camera metadata (location, orientation, calibration)
   - External context (ADS-B match? satellite pass? weather?)

2. Tools it must be able to call:
   - check_adsb(track_data)
   - predict_satellite_pass(lat, lon, time)
   - get_weather(lat, lon, time)
   - query_local_baseline(camera_id, time_of_day)

3. Output structured JSON:
   {
     "confidence": 0-100,
     "justification": "1-3 sentence clear explanation",
     "recommended_action": "record_high_res | request_multi_station | human_review | discard",
     "reasoning_trace": "step-by-step internal reasoning"
   }

4. Use few-shot examples for:
   - Clear commercial airliner (low confidence)
   - High-speed non-ballistic object with no ADS-B (high confidence)
   - Large bird flock (medium confidence, explain why)

5. Make the agent explainable and conservative — prefer false negatives over false positives on public alerts.

Generate:
- Full agent definition (system prompt + tool schemas)
- Example Python code using google-generativeai or Vertex AI SDK
- Prompt templates for different confidence thresholds
- Evaluation rubric for the agent

This agent will run after the DeepStream perception layer and before final event storage.
```

---

## 3. Enhancement Module — Super-Resolution Trigger

**Prompt for any coding agent (Claude, Gemini, Cursor, etc.):**

```
Create a modular "Enhancement Module" for AETHER.

When a high-confidence track is detected, the module must:
1. Extract the track bounding box history from the DeepStream metadata
2. Crop the relevant video segment (with padding)
3. Run state-of-the-art video super-resolution + motion deblur
   - Recommended models: Real-ESRGAN (video), BasicVSR++, or latest open video enhancement models
   - Support both CPU and GPU (CUDA) execution
4. Stabilize the cropped track (remove camera shake)
5. Save two outputs:
   - enhanced_track.mp4 (high quality, 2–4× resolution)
   - thumbnail.jpg (best frame)
6. Return metadata: enhancement_model_used, processing_time, quality_metrics (if possible)

Make it:
- Standalone Python package (`aether_enhancement/`)
- Configurable via YAML (model choice, upscale factor, GPU/CPU)
- Triggered only on events with confidence > 65 (configurable)
- Efficient — only process the track region, not the full frame
- Include a simple CLI: `python enhance.py --input original_clip.mp4 --track track.json --output enhanced/`

Provide full code + requirements.txt + example usage.
```

---

## 4. BOB Adapter Scaffold

**Prompt for any coding agent:**

```
Create the **BOB Adapter** module for AETHER.

Purpose: Allow seamless interoperability between AETHER and the existing open-source BOB (Universal Object Tracker) project.

Requirements:
- Real-time ingestion of BOB detection events (via REST webhook or shared message queue / Redis / MQTT)
- Parse BOB track data (bounding boxes, timestamps, camera info)
- Re-process BOB tracks through AETHER’s full pipeline:
  - Perception (if needed)
  - Enhancement module
  - Reasoning Agent (Gemini)
- Enrich the original BOB event with:
  - AETHER confidence score + justification
  - Enhanced video clip
  - Standardized AETHER metadata JSON
- Optional: Push enriched events back to BOB users (webhook or shared dashboard format)
- Support both "pull" (poll BOB API) and "push" (webhook receiver) modes
- Configuration via YAML (BOB endpoint, API key if needed, processing mode)

Generate complete scaffold:
aether_bob_adapter/
├── adapter.py
├── config.yaml.example
├── webhook_server.py
├── enricher.py
├── requirements.txt
└── README.md (with setup instructions and migration guide for existing BOB users)

Make it production-ready, well-documented, and easy to run alongside an existing BOB installation.
```

---

**How to use these prompts:**

1. Copy the exact block for the component you want to build first.
2. Paste into the target AI (NVIDIA coding agent, Claude, Gemini, Cursor, etc.).
3. Iterate on the output until it runs cleanly.
4. Commit the generated code into the `src/` or appropriate folder.

---

**Status**: All prompts ready for immediate use.  
**Next**: Start generating code with Prompt #1 (NVIDIA DeepStream core pipeline).

---

*These prompts were carefully engineered for maximum quality and minimal iteration.*