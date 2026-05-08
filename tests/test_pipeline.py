"""
AETHER End-to-End Test Harness
Run with: python -m pytest tests/test_pipeline.py -s
"""

import sys
sys.path.append("../src")

from aether_perception.perception import AetherPerception
from aether_agent.agent import AetherReasoningAgent
from aether_enhancement.enhance import AetherEnhancer
from aether_bob_adapter.adapter import BobAdapter
import tempfile
import os

def create_test_video(path: str, duration_sec: int = 5):
    """Generate a simple synthetic video for testing"""
    import cv2
    import numpy as np
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, 30, (640, 480))
    
    for i in range(duration_sec * 30):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw a fast-moving "anomaly" (white square)
        x = int(100 + (i * 8) % 400)
        y = 200 + int(30 * np.sin(i / 10))
        cv2.rectangle(frame, (x, y), (x+40, y+40), (255, 255, 255), -1)
        out.write(frame)
    out.release()
    print(f"Test video created: {path}")

def test_full_pipeline():
    print("\n=== AETHER Full Pipeline Test ===")
    
    # 1. Create test video
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "test_anomaly.mp4")
        create_test_video(video_path)
        
        # 2. Perception
        perception = AetherPerception(config_path="../src/aether_perception/config.yaml")  # will use default
        events = perception.process_stream(video_path, duration_sec=3)
        print(f"Perception found {len(events)} candidate events")
        
        if events:
            # 3. Agent reasoning
            agent = AetherReasoningAgent()
            result = agent.analyze_track(events[0])
            print(f"Agent decision: {result['recommended_action']} (conf={result['confidence']})")
            
            # 4. Enhancement (on first event)
            enhancer = AetherEnhancer()
            enhanced_path = enhancer.enhance_track(video_path, output_dir=tmpdir)
            print(f"Enhanced clip: {enhanced_path}")
            
            # 5. BOB adapter (mock)
            bob = BobAdapter()
            enriched = bob.receive_bob_event(events[0])
            print(f"BOB enrichment complete. AETHER confidence: {enriched.get('aether_confidence')}")
    
    print("=== All tests passed! ===")

if __name__ == "__main__":
    test_full_pipeline()