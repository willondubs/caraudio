#!/usr/bin/env python3
"""Test script for playing a specific file."""
import sys
from car_music_player import CarMusicPlayer

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_player.py <path_to_audio_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    player = CarMusicPlayer()
    
    if player.test_play_file(file_path):
        print(f"Playing {file_path}")
        try:
            while True:
                pass  # Keep running until Ctrl+C
        except KeyboardInterrupt:
            print("\nStopping playback")
    else:
        print(f"Failed to play {file_path}")

if __name__ == "__main__":
    main()