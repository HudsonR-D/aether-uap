# AETHER — Anomaly Detection Criteria (v1.0)

**Approved: 2026-05-08**

## 1. Philosophy

AETHER prioritizes **scientific utility** over sensationalism. We aim for:
- Extremely low false-positive rate on public alerts
- High recall on genuinely anomalous events
- Rich, standardized metadata that enables downstream research
- Transparent, auditable decision-making (every flag includes justification)

We use a **layered, confidence-scored pipeline** so cheap, deterministic filters run first.

## 2. Tiered Detection System

### Tier 1 — Instant Reject (Deterministic, <5ms)
These events are discarded with zero further processing.

- Correlates with public ADS-B / Mode S / flight tracking (OpenSky, ADSBexchange, etc.)
- Matches known satellite, ISS, or Starlink pass predictions (using current TLEs)
- Classic meteor/fireball signature (high speed + predictable parabolic arc + short duration)
- Obvious lens flare, sensor bloom, rain/snow streak, bug on lens (via light intensity + motion vector analysis)

### Tier 2 — Kinematic Red Flags (Core Engine)
Primary source of candidates.

**Speed thresholds** (adjustable per camera altitude profile):
- Sustained ground speed > 300 m/s below 3 km AGL
- Sustained > Mach 1.5 above 10 km AGL
- Instantaneous velocity change > 50 m/s in < 0.5 s

**Acceleration / Maneuver thresholds**:
- Lateral or vertical acceleration > 5 g sustained for > 1 s
- Direction change > 35° with turning radius inconsistent with conventional aircraft
- Hover + sudden acceleration > 3 g (no visible rotors or propulsion signature)

**Non-ballistic behaviors**:
- Right-angle turns at constant speed
- Zigzag or corkscrew patterns without aerodynamic explanation
- Rapid vertical ascent/descent from surface (> 50 m/s vertical)
- “Falling leaf” or spiraling descent inconsistent with debris
- Formation flying or coordinated swarm behavior without corresponding ADS-B

### Tier 3 — Contextual & Multi-Modal
- No navigation or anti-collision light patterns matching FAA/EASA standards or timing
- Absence of contrail or visible engine exhaust in clear conditions
- Thermal/IR signature mismatch (if IR camera available):
  - Too cold for jet aircraft at altitude
  - Too hot for high-altitude balloon
  - No exhaust plume consistent with propulsion
- Apparent size vs. estimated distance inconsistency (using known references in frame)
- Operation during weather conditions where conventional traffic is normally grounded (icing, heavy turbulence, etc.)
- Geographic anomaly (active inside restricted airspace, no-fly zones, or military operating areas with zero correlating traffic)

### Tier 4 — Agentic Reasoning Layer (LLM / Gemini)
Final high-confidence gate.

The agent receives:
- Full kinematic history (position, velocity, acceleration vectors over time)
- Cropped video track (original + enhanced)
- Local “normal sky” baseline model for that specific camera/location/time-of-day
- External context (weather, known launches, NOTAMs, exercises)
- Visual attributes (shape, lights, surface features if resolvable)

**Output**:
- UAP Confidence Score: 0–100
- Plain-English justification (1–3 sentences)
- Recommended action (record high-res clip, request multi-station confirmation, alert human reviewer, discard)

## 3. False Positive Reduction Strategy

1. **Hierarchical filtering** — 95%+ of tracks die in Tier 1 or 2
2. **Per-camera baseline learning** — First 7–14 days of operation builds a location-specific “normal traffic” model
3. **Active learning loop** — User thumbs-up/down on borderline events improves local + global models
4. **Multi-station confirmation** — Events > 80% confidence require corroboration from ≥2 independent stations before public/high-visibility alert
5. **Human review queue** — Anything 65–85% confidence goes to optional human review (with rich context)
6. **Explainability** — Every flagged event includes full reasoning trace

## 4. Edge Cases & Known Challenges (Explicitly Handled)

- Large bird flocks or drone swarms (kinematic + visual signature matching)
- High-altitude balloons (party, scientific, weather) — predictable slow drift + thermal profile
- Chinese lanterns, flares, fireworks, model rockets
- Military exercises / known drone operations (via public NOTAM cross-reference)
- Extreme low-light sensor noise or heat haze
- Partial occlusions (clouds, trees, power lines, buildings)
- Lens artifacts in wide-angle / fisheye cameras
- Starlink “train” passes during early deployment phases

## 5. Event Metadata Schema (v1.0)

Every candidate event produces a standardized JSON record:

```json
{
  "event_id": "aether-20260508-uuid",
  "timestamp_utc": "2026-05-08T12:34:56.789Z",
  "camera_id": "station-001",
  "location": { "lat": 39.1234, "lon": -76.5678, "alt_m": 245 },
  "track": {
    "duration_s": 12.4,
    "max_speed_mps": 487,
    "max_accel_g": 8.2,
    "maneuver_type": "right_angle_turn",
    "non_ballistic": true
  },
  "confidence": 87,
  "justification": "Sustained 8.2g lateral acceleration with instantaneous 42° direction change. No ADS-B. No thermal exhaust. Shape inconsistent with known aircraft.",
  "media": {
    "original_clip": "s3://aether-events/2026/05/08/station-001/event-uuid-original.mp4",
    "enhanced_clip": "s3://aether-events/2026/05/08/station-001/event-uuid-enhanced.mp4",
    "thumbnail": "..."
  },
  "context": {
    "adsb_match": false,
    "satellite_pass": false,
    "weather": "clear",
    "nearby_stations": ["station-007", "station-012"]
  },
  "version": "aether-criteria-v1.0"
}
```

## 6. Versioning & Evolution

- Criteria are versioned (`v1.0`, `v1.1`, …)
- Major changes require community discussion + migration guide
- Local models can be fine-tuned per station while global criteria remain standardized

---

**Status**: Approved for implementation.  
**Next**: Architecture document + code generation prompts.