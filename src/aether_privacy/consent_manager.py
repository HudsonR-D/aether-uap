"""
AETHER Privacy & Consent Manager
Handles user consent, anonymization, and data contribution settings for deployed instances.
"""

from enum import Enum
from typing import Dict, Optional
import json
from pathlib import Path

class ConsentLevel(Enum):
    NONE = "none"                    # No data shared
    ANONYMIZED_EVENTS = "events"     # Only anonymized high-signal events
    FULL_WITH_FEEDBACK = "full"      # Events + user thumbs up/down + optional notes

class ConsentManager:
    def __init__(self, config_path: str = "privacy_config.json"):
        self.config_path = Path(config_path)
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict:
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "consent_level": ConsentLevel.NONE.value,
            "contribute_to_improvement": False,
            "share_location_grid": True,
            "last_updated": None
        }

    def set_consent(self, level: ConsentLevel, contribute: bool = True):
        self.settings["consent_level"] = level.value
        self.settings["contribute_to_improvement"] = contribute
        self.settings["last_updated"] = str(__import__("datetime").datetime.now())
        
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f, indent=2)
        
        print(f"[Privacy] Consent updated to: {level.value}")

    def can_share_event(self, event: Dict) -> bool:
        if self.settings["consent_level"] == ConsentLevel.NONE.value:
            return False
        return True

    def get_anonymization_level(self) -> str:
        return self.settings.get("consent_level", "none")

    def show_consent_ui(self):
        """Simple CLI consent UI — in production this becomes a nice web dashboard page"""
        print("\n" + "="*50)
        print("AETHER Privacy & Data Contribution Settings")
        print("="*50)
        print("AETHER can improve itself using real-world data from users like you.")
        print("All data is heavily anonymized. You are always in control.\n")
        
        print("Current setting:", self.settings["consent_level"])
        print("\nOptions:")
        print("1. No data sharing (recommended for maximum privacy)")
        print("2. Share only anonymized high-signal events (helps improve the system)")
        print("3. Share events + your thumbs up/down feedback (maximum help to the project)")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            self.set_consent(ConsentLevel.NONE)
        elif choice == "2":
            self.set_consent(ConsentLevel.ANONYMIZED_EVENTS)
        elif choice == "3":
            self.set_consent(ConsentLevel.FULL_WITH_FEEDBACK)
        else:
            print("Invalid choice. Keeping current setting.")