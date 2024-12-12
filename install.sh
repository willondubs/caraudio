#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-pygame python3-evdev alsa-utils

# Create directories
mkdir -p /home/williew/music
mkdir -p /home/williew/logs

# Copy files
cp -r car_music_player /home/williew/
cp main.py /home/williew/
cp requirements.txt /home/williew/
chmod +x /home/williew/main.py

# Install Python packages
python3 -m pip install -r requirements.txt

# Set up systemd service
sudo tee /etc/systemd/system/car-music.service << EOF
[Unit]
Description=Car Music Player
After=multi-user.target sound.target
Wants=sound.target

[Service]
Type=simple
User=williew
WorkingDirectory=/home/williew
ExecStart=/usr/bin/python3 /home/williew/main.py
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1
Environment=SDL_AUDIODRIVER=alsa

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
sudo chown -R williew:williew /home/williew/music
sudo chown -R williew:williew /home/williew/logs
sudo usermod -a -G audio williew
sudo usermod -a -G input williew

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable car-music.service
sudo systemctl restart car-music.service

# Show status
echo "Installation complete. Checking service status..."
sudo systemctl status car-music.service