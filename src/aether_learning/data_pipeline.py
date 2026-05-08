"""
AETHER Continuous Learning Data Pipeline
Privacy-first system that turns real-world usage into continuous model & prompt improvement.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid

class ContinuousLearningPipeline:
    def __init__(self, storage_path: str = "learning_data"):
        self.storage = Path(storage_path)
        self.storage.mkdir(exist_ok=True)
        self.datasets_dir = self.storage / "datasets"
        self.datasets_dir.mkdir(exist_ok=True)
        print("[AETHER Learning Pipeline] Initialized (privacy-first mode)")

    def ingest_event(self, event: Dict, user_consent: bool = False, feedback: Optional[Dict] = None):
        """
        Ingest a detection event from any deployed AETHER instance.
        Only stores if user has given explicit consent.
        """
        if not user_consent:
            print("[Learning] Event discarded — no user consent")
            return None

        # Anonymize
        anonymized = self._anonymize_event(event)
        
        # Attach feedback if provided
        if feedback:
            anonymized["user_feedback"] = feedback  # e.g. {"thumbs": "up", "notes": "clear non-ballistic maneuver"}

        # Store
        event_id = str(uuid.uuid4())
        filepath = self.storage / f"events/{event_id}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(anonymized, f, indent=2)

        print(f"[Learning] Event {event_id} ingested for future fine-tuning")
        return event_id

    def _anonymize_event(self, event: Dict) -> Dict:
        """Remove or hash PII while preserving scientific value"""
        anon = event.copy()
        
        # Hash location to grid (preserves regional patterns without exact coords)
        if "location" in anon:
            lat = anon["location"].get("lat", 0)
            lon = anon["location"].get("lon", 0)
            grid = f"{round(lat, 1)}_{round(lon, 1)}"
            anon["location_grid"] = grid
            del anon["location"]
        
        # Remove camera_id, replace with hash
        if "camera_id" in anon:
            anon["camera_hash"] = hashlib.sha256(anon["camera_id"].encode()).hexdigest()[:12]
            del anon["camera_id"]
        
        return anon

    def create_fine_tuning_dataset(self, min_events: int = 500, version: str = None) -> str:
        """
        Curate a high-quality dataset from collected events for model fine-tuning.
        """
        version = version or datetime.now().strftime("v%Y%m%d")
        dataset_path = self.datasets_dir / f"fine_tuning_{version}.jsonl"
        
        events = list(self.storage.glob("events/*.json"))
        if len(events) < min_events:
            print(f"[Learning] Not enough events yet ({len(events)}/{min_events})")
            return None

        high_quality = []
        for event_file in events:
            with open(event_file) as f:
                event = json.load(f)
            
            # Only include events with strong signals (user feedback or high confidence + multi-station confirmation)
            if event.get("user_feedback", {}).get("thumbs") == "up" or \
               (event.get("aether_confidence", 0) > 85 and event.get("multi_station_confirmed")):
                high_quality.append(event)

        with open(dataset_path, "w") as f:
            for event in high_quality:
                f.write(json.dumps(event) + "\n")

        print(f"[Learning] Created fine-tuning dataset: {dataset_path} ({len(high_quality)} high-quality examples)")
        return str(dataset_path)

    def trigger_meta_agent_improvement(self):
        """Notify the Meta-Agent that new data is available for an improvement cycle"""
        print("[Learning] Triggering Meta-Agent improvement cycle with new data...")
        # In real system: send message to Meta-Agent or update a shared state file
        return True

    def get_stats(self) -> Dict:
        return {
            "total_events_collected": len(list(self.storage.glob("events/*.json"))),
            "datasets_available": len(list(self.datasets_dir.glob("*.jsonl"))),
            "last_dataset": max(self.datasets_dir.glob("*.jsonl"), default=None)
        }