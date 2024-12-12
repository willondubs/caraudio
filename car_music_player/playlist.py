"""Playlist management module."""
from pathlib import Path
import logging

class PlaylistManager:
    def __init__(self, music_dir):
        self.logger = logging.getLogger('CarPlayer')
        self.music_dir = Path(music_dir)
        
    def load_playlist(self):
        """Load all music files from directory."""
        playlist = []
        self.logger.info(f"Scanning directory: {self.music_dir}")
        
        for file in self.music_dir.glob('**/*'):
            if file.suffix.lower() in ['.mp3', '.flac']:
                playlist.append(str(file))
                
        self.logger.info(f"Found {len(playlist)} music files")
        return sorted(playlist)