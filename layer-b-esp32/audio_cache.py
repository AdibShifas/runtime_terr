# audio_cache.py - Audio Caching System for Sheldon Rover
# Loads and plays pre-generated audio clips from files

import os
import json
import random

# Try to import for ESP32 (MicroPython)
try:
    from machine import Pin, I2S
    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

from config import DEBUG

# Get the directory where this file is located
BASE_DIR = os.path.dirname(__file__) if '__file__' in dir() else '.'


class AudioCache:
    """
    Manages pre-generated audio clips.
    
    Clip naming convention:
        {EVENT}_{TIER}_{VARIANT}.mp3
        e.g., COLLISION_2_1.mp3 = Collision event, tier 2, variant 1
    
    Usage:
        cache = AudioCache()
        cache.play("COLLISION", tier=2)
    """
    
    def __init__(self, clips_dir: str = None, manifest_path: str = None):
        """
        Initialize audio cache.
        
        Args:
            clips_dir: Directory containing audio clips
            manifest_path: Path to clip_manifest.json
        """
        if clips_dir is None:
            clips_dir = os.path.join(BASE_DIR, 'audio', 'clips')
        if manifest_path is None:
            manifest_path = os.path.join(BASE_DIR, 'audio', 'clip_manifest.json')
        
        self.clips_dir = clips_dir
        self.manifest = {}
        self.available_clips = {}  # {clip_id: full_path}
        self.fallback_tts = True
        
        self._load_manifest(manifest_path)
        self._scan_clips()
        
        if DEBUG:
            print(f"[AUDIO_CACHE] Loaded {len(self.available_clips)} clips from {clips_dir}")

    def _load_manifest(self, manifest_path: str):
        """Load clip manifest from JSON file."""
        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)
                self.manifest = data.get('clips', {})
                self.fallback_tts = data.get('fallback_tts', True)
                
                if DEBUG:
                    print(f"[AUDIO_CACHE] Loaded manifest with {len(self.manifest)} entries")
        except (OSError, IOError, json.JSONDecodeError) as e:
            if DEBUG:
                print(f"[AUDIO_CACHE] No manifest found: {e}")
            self.manifest = {}

    def _scan_clips(self):
        """Scan clips directory and build available clips index."""
        self.available_clips = {}
        
        try:
            if not os.path.exists(self.clips_dir):
                if DEBUG:
                    print(f"[AUDIO_CACHE] Clips directory not found: {self.clips_dir}")
                return
            
            for filename in os.listdir(self.clips_dir):
                if filename.endswith(('.mp3', '.wav', '.ogg')):
                    # Map manifest entries to files
                    for clip_id, manifest_filename in self.manifest.items():
                        if manifest_filename == filename:
                            full_path = os.path.join(self.clips_dir, filename)
                            self.available_clips[clip_id] = full_path
                    
                    # Also allow direct filename matching (without extension)
                    clip_id = os.path.splitext(filename)[0].upper()
                    full_path = os.path.join(self.clips_dir, filename)
                    if clip_id not in self.available_clips:
                        self.available_clips[clip_id] = full_path
                        
        except OSError as e:
            if DEBUG:
                print(f"[AUDIO_CACHE] Error scanning clips: {e}")

    def get_clip_path(self, event: str, tier: int = 0, variant: int = None) -> str:
        """
        Get path to audio clip for given event and tier.
        
        Args:
            event: Event name (e.g., "COLLISION")
            tier: Intensity tier (0, 1, or 2)
            variant: Optional variant number, random if not specified
            
        Returns:
            Full path to clip file, or None if not found
        """
        # Try with specific variant
        if variant is not None:
            clip_id = f"{event}_{tier}_{variant}"
            if clip_id in self.available_clips:
                return self.available_clips[clip_id]
        
        # Try to find any variant for this event/tier
        matching_clips = []
        prefix = f"{event}_{tier}"
        
        for clip_id, path in self.available_clips.items():
            if clip_id.startswith(prefix):
                matching_clips.append(path)
        
        # Also try just event_tier (no variant suffix)
        simple_id = f"{event}_{tier}"
        if simple_id in self.available_clips:
            matching_clips.append(self.available_clips[simple_id])
        
        if matching_clips:
            return random.choice(matching_clips)
        
        # Fallback: try just the event name
        if event in self.available_clips:
            return self.available_clips[event]
        
        return None

    def has_clip(self, event: str, tier: int = 0) -> bool:
        """Check if a clip exists for the given event and tier."""
        return self.get_clip_path(event, tier) is not None

    def list_clips(self) -> list:
        """List all available clip IDs."""
        return list(self.available_clips.keys())

    def play(self, event: str, tier: int = 0, text_fallback: str = None):
        """
        Play audio clip for event/tier.
        
        Args:
            event: Event name
            tier: Intensity tier
            text_fallback: Text to speak if no clip found (uses TTS)
        """
        clip_path = self.get_clip_path(event, tier)
        
        if clip_path:
            self._play_file(clip_path)
        elif text_fallback and self.fallback_tts:
            self._speak_tts(text_fallback)
        elif DEBUG:
            print(f"[AUDIO_CACHE] No clip for {event}_{tier}")

    def _play_file(self, path: str):
        """Play an audio file."""
        if DEBUG:
            print(f"[AUDIO_CACHE] Playing: {path}")
        
        if IS_MICROPYTHON:
            # ESP32: Use I2S or external player
            # TODO: Implement based on hardware (DFPlayer, I2S, etc.)
            print(f"🔊 [Would play: {os.path.basename(path)}]")
        else:
            # Desktop: Use system command
            import subprocess
            try:
                # macOS
                subprocess.run(['afplay', path], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Linux
                    subprocess.run(['mpg123', '-q', path], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(f"🔊 [Would play: {os.path.basename(path)}]")

    def _speak_tts(self, text: str):
        """Fallback: use TTS to speak text."""
        if DEBUG:
            print(f"[AUDIO_CACHE] TTS fallback: {text}")
        
        print(f"🔊 {text}")
        
        if not IS_MICROPYTHON:
            import subprocess
            try:
                # macOS
                subprocess.run(['say', text], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass  # No TTS available
