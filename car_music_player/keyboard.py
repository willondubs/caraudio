"""Keyboard input handling module."""
import evdev
import logging
import threading

class KeyboardManager:
    def __init__(self, prev_callback, play_pause_callback, next_callback):
        self.logger = logging.getLogger('CarPlayer')
        self.prev_callback = prev_callback
        self.play_pause_callback = play_pause_callback
        self.next_callback = next_callback
        
        self._setup_keyboard()
        self._start_keyboard_thread()
        
    def _setup_keyboard(self):
        """Find and setup USB keyboard."""
        try:
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                if "sayo" in device.name.lower():
                    self.keyboard = device
                    self.logger.info(f"Found keyboard: {device.name}")
                    return
            raise RuntimeError("USB keyboard not found")
        except Exception as e:
            self.logger.error(f"Error setting up keyboard: {e}")
            raise
            
    def _keyboard_loop(self):
        """Handle keyboard events."""
        try:
            for event in self.keyboard.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    keyevent = evdev.categorize(event)
                    if keyevent.keystate == keyevent.key_up:
                        key_name = keyevent.keycode
                        if isinstance(key_name, list):
                            key_name = key_name[0]
                            
                        if key_name == 'KEY_LEFT':
                            self.prev_callback()
                        elif key_name == 'KEY_RIGHT':
                            self.next_callback()
                        elif key_name == 'KEY_ENTER':
                            self.play_pause_callback()
        except Exception as e:
            self.logger.error(f"Error in keyboard loop: {e}")
            
    def _start_keyboard_thread(self):
        """Start keyboard monitoring in a separate thread."""
        keyboard_thread = threading.Thread(target=self._keyboard_loop)
        keyboard_thread.daemon = True
        keyboard_thread.start()