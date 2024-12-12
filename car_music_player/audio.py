"""Audio playback handling module."""
import pygame
import logging
from pathlib import Path

class AudioManager:
    def __init__(self):
        self.logger = logging.getLogger('CarPlayer')
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
    def play_file(self, file_path):
        """Play a single audio file."""
        try:
            self.logger.info(f"Loading audio file: {file_path}")
            pygame.mixer.music.load(str(file_path))
            self.logger.info("Starting playback")
            pygame.mixer.music.play()
            return True
        except Exception as e:
            self.logger.error(f"Error playing {file_path}: {e}")
            return False
            
    def pause(self):
        pygame.mixer.music.pause()
        
    def unpause(self):
        pygame.mixer.music.unpause()
        
    def is_playing(self):
        return pygame.mixer.music.get_busy()
        
    def cleanup(self):
        pygame.mixer.quit()