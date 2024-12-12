"""Main player module."""
import time
import json
import logging
from pathlib import Path
import threading
from .audio import AudioManager
from .playlist import PlaylistManager
from .keyboard import KeyboardManager

class CarMusicPlayer:
    def __init__(self):
        self._setup_logging()
        self.logger.info("Initializing Car Music Player")
        
        try:
            self._init_components()
            self.keyboard = KeyboardManager(self._handle_prev,
                                         self._handle_play_pause,
                                         self._handle_next)
            self.logger.info("Car Music Player initialized successfully")
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            raise

    def _setup_logging(self):
        log_dir = Path("/home/williew/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "player.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CarPlayer')

    def _init_components(self):
        # Set up paths and components
        self.music_dir = Path('/home/williew/music')
        self.state_file = Path('/home/williew/player_state.json')
        self.intro_file = self.music_dir / 'intro.wav'
        
        self.audio = AudioManager()
        self.playlist_manager = PlaylistManager(self.music_dir)
        
        # Load playlist and state
        self.playlist = self.playlist_manager.load_playlist()
        self.current_index = 0
        self.playing = False
        self._load_state()

    def _load_state(self):
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_index = state.get('index', 0)
                    self.playing = state.get('playing', False)
                    self.logger.info(f"Loaded state: index={self.current_index}, playing={self.playing}")
        except Exception as e:
            self.logger.error(f"Error loading state: {e}")

    def _save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'index': self.current_index,
                    'playing': self.playing
                }, f)
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")

    def play_current(self):
        if not self.playlist:
            self.logger.warning("No music files found")
            return
            
        if 0 <= self.current_index < len(self.playlist):
            current_track = self.playlist[self.current_index]
            if self.audio.play_file(current_track):
                self.playing = True
                self._save_state()
            else:
                self._handle_next()

    def _handle_prev(self):
        self.logger.info("Previous track")
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_current()

    def _handle_next(self):
        self.logger.info("Next track")
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_current()

    def _handle_play_pause(self):
        if self.playing:
            self.logger.info("Pause")
            self.audio.pause()
            self.playing = False
        else:
            self.logger.info("Resume")
            self.audio.unpause()
            self.playing = True
        self._save_state()

    def test_play_file(self, file_path):
        """Test function to play a specific file."""
        self.logger.info(f"Test playing file: {file_path}")
        return self.audio.play_file(Path(file_path))

    def run(self):
        self.logger.info("Starting player")
        
        # Play intro if available
        if self.intro_file.exists():
            self.logger.info("Playing intro")
            self.audio.play_file(self.intro_file)
            while self.audio.is_playing():
                time.sleep(0.1)
        
        # Start playback
        self.playing = True  # Auto-start playback
        self.play_current()
        
        # Main loop
        try:
            while True:
                if self.playing and not self.audio.is_playing():
                    self._handle_next()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.logger.info("Shutting down")
            self._save_state()
            self.audio.cleanup()