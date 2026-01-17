# audio_player.py - Audio Playback for Sheldon Rover
# Now uses cached clips with TTS fallback

from config import DEBUG
from audio_cache import AudioCache


class AudioPlayer:
    """
    Audio player that uses pre-generated clips when available,
    falls back to TTS when not.
    """
    
    def __init__(self):
        """Initialize audio player with clip cache."""
        self.cache = AudioCache()
        
        if DEBUG:
            clips = self.cache.list_clips()
            if clips:
                print(f"[AUDIO] Loaded {len(clips)} cached clips")
            else:
                print("[AUDIO] No cached clips found, using TTS fallback")
    
    def speak(self, text: str, event: str = None, tier: int = 0):
        """
        Speak the given text.
        
        If event/tier is provided and a cached clip exists, play it.
        Otherwise, fall back to TTS.
        
        Args:
            text: The text to speak (used for TTS fallback)
            event: Optional event name for clip lookup
            tier: Optional tier for clip lookup
        """
        # Try to play cached clip
        if event and self.cache.has_clip(event, tier):
            self.cache.play(event, tier, text_fallback=text)
        else:
            # No cached clip, use TTS
            self._speak_tts(text)
    
    def _speak_tts(self, text: str):
        """Speak using system TTS."""
        print(f"🔊 {text}")
        
        try:
            # Try MicroPython first
            from machine import Pin
            # On ESP32, would use external TTS or skip
            pass
        except ImportError:
            # Desktop: use system TTS
            import subprocess
            import shutil
            
            if shutil.which("say"):
                try:
                    subprocess.run(['say', text], check=True)
                except subprocess.CalledProcessError:
                    pass  # TTS failed, already printed
    
    def stop(self):
        """Stop current playback."""
        pass


# =============================================================================
# Factory Function (for backwards compatibility)
# =============================================================================

def create_audio_player(backend: str = "auto") -> AudioPlayer:
    """
    Create an audio player.
    
    Args:
        backend: "auto" (recommended), "cache", or "tts"
        
    Returns:
        AudioPlayer instance
    """
    return AudioPlayer()
