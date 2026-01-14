# NVMI

**NVMI** is a lightweight, real-time NVIDIA GPU monitor for Windows, built with Python and NVML.

It provides a clean terminal-based interface inspired by `nvidia-smi`, with live updates and visual indicators.

![NVMI Live GPU Monitor](screenshots/nvmi-display-new.png)

## ✨ Features

- Live NVIDIA GPU utilization monitoring
- Memory usage (used / total)
- Real-time GPU temperature
- Power draw and enforced power limit
- **Video Encode (NVENC) utilization**
- **Video Decode (NVDEC) utilization**
- Dynamic color indicators  
  - Green → Red based on load and temperature
- Clean, single-box live terminal UI  
  (modern `nvidia-smi`–style)

## Requirements
- NVIDIA GPU
- NVIDIA drivers
- Python (for who wants to build)

## Install
```bash
pip install -r requirements.txt
pyinstaller --onefile --name nvmi nvmi.py
dist/nvmi.exe
