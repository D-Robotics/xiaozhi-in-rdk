English | [简体中文](./README_cn.md)

# XiaoZhi AI Voice Assistant - RDK Series

> **D-Robotics Team** Official RDK Series Platform Adaptation Project

## Project Overview

This project is a professional adaptation of XiaoZhi AI Voice Assistant for RDK series embedded development boards, implementing complete real-time voice interaction capabilities. Through deep optimization for ARM architecture and embedded environments, it provides stable and efficient AI voice interaction experience.

**Supported Boards**: RDK X3 / RDK X5 / RDK S100

**Special Thanks** to [@huangjunsen0406](https://github.com/huangjunsen0406) for the [py-xiaozhi project](https://github.com/huangjunsen0406/py-xiaozhi) providing technical foundation support.

### Key Features

- **Full RDK Series Support**: Optimized for RDK X3/X5/S100 with deep ARM architecture adaptation
- **Real-time Voice Interaction**: 16kHz/24kHz sampling rate with ultra-low latency
- **End-to-End Encryption**: AES-128-CTR mode ensuring data security
- **Dual Protocol Support**: MQTT control + UDP audio transmission
- **YOLOv8 Object Detection**: MCP protocol integration, AI-callable vision capabilities
- **Simple to Use**: Space key interaction, one-click startup
- **Dual Camera Support**: USB/MIPI camera switching

## System Architecture

```
User Input ←→ Audio Processing ←→ Encrypted Transmission ←→ AI Service
    ↓              ↓                    ↓                    ↓
Space Key      Opus Codec           AES Encryption      Smart Dialog
Status Display Real-time Stream      UDP Transport      Voice Synthesis
```

## Requirements

### Hardware Requirements
- **Board**: RDK X3 / RDK X5 / RDK S100
- **Audio Device (Recommended)**: USB microphone and USB speaker
  - RDK X5 onboard audio interface is also supported (requires default device configuration)
- **Network**: WiFi or Ethernet connection

### Software Dependencies
- **OS**: rdkos 3.0.0+
- **Python**: 3.10+
- **Audio**: ALSA + PulseAudio

## Quick Start

### 1. System Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install python3 python3-pip python3-dev build-essential -y
sudo apt install libasound2-dev portaudio19-dev libopus-dev -y
sudo apt install alsa-utils pulseaudio-utils -y
```

### 2. Install Python Dependencies

```bash
# Install all dependencies (automatically install latest versions)
pip3 install -r requirements.txt
```

### 3. Audio Device Configuration

**USB audio devices are recommended** for the best experience. If you need to use RDK X5 onboard audio interface, configure the default device as follows.

#### Check Audio Devices

```bash
# List playback devices
aplay -l

# List capture devices
arecord -l
```

#### Configure Default Audio Device (Optional)

If you're using RDK X5 onboard audio or need to change the default device, edit the ALSA configuration file:

```bash
# Edit configuration file
nano ~/.asoundrc
```

Add the following content (adjust card numbers based on your actual devices):

```bash
# Set default playback device to card 1, capture device to card 0
pcm.!default {
    type asym
    playback.pcm "plughw:1,0"    # Playback - supports auto conversion
    capture.pcm "plughw:0,0"     # Capture - supports auto conversion
}

# Control device
ctl.!default {
    type hw
    card 1
}
```

Verify configuration:

```bash
# Check default device
aplay -l | grep default

# Test audio functionality
arecord -f cd -t wav -d 3 test.wav  # Record 3-second test
aplay test.wav                       # Play test

# If recorded audio has no sound, adjust microphone volume
alsamixer  # Press F4 to select capture device, use arrow keys to adjust volume
# Or use command line:
amixer sset Capture 80%  # Set capture volume to 80%
```

### 4. Run the Program

**Voice Assistant Only:**
```bash
python3 xiaozhi-in-rdk.py
```

**Voice Assistant + YOLOv8 Detection (Recommended):**

Two separate terminals are required:

```bash
# Terminal 1: Start XiaoZhi main program (foreground, supports space key interaction)
python3 xiaozhi-in-rdk.py
```

```bash
# Terminal 2: Start MCP service
source /opt/tros/humble/setup.bash
export MCP_ENDPOINT=ws://your-server:8765
export CAM_TYPE=usb  # or mipi
python3 mcp_pipe.py
```

## Usage Guide

### Basic Operations
| Action              | Key             | Description                                        |
| ------------------- | --------------- | -------------------------------------------------- |
| **Start Recording** | Hold `SPACE`    | Begin voice input, shows "🎤 Listening..."          |
| **Stop Recording**  | Release `SPACE` | End recording, wait for AI processing and response |
| **Exit Program**    | Press `q`       | Gracefully exit program and clean up resources     |

### Status Indicators
- **Connecting Session**: Establishing connection to server
- **Listening**: Recording your voice input
- **Waiting for Reply**: Processing voice and waiting for AI response
- **Playing**: AI is responding
- **Playback Complete**: Response playback finished

### YOLOv8 Object Detection (MCP Service)

After enabling the MCP service, AI can control YOLOv8 object detection through the following tools. Supports all RDK boards (X3/X5/S100).

#### YOLOv8 Available Tools
1. **start_yolov8_detection(camera_type)** - Start YOLOv8 detection service
2. **stop_yolov8_detection()** - Stop YOLOv8 detection service
3. **get_yolov8_status()** - Query YOLOv8 running status
4. **restart_yolov8_detection(camera_type)** - Restart YOLOv8 service
5. **switch_camera(camera_type)** - Switch camera

#### Preview URL
After starting YOLOv8 detection service, you can view the real-time detection stream at:
- **Local preview**: `http://127.0.0.1:8000`
- **LAN preview**: `http://<wlan0_IP_address>:8000`

The service automatically detects wlan0 connection status and displays the corresponding preview URL:
- ✅ wlan0 connected: Shows `🎥 Preview URL: http://192.168.x.x:8000`
- ⚠️ wlan0 disconnected: Shows `⚠️ wlan0 not connected, Preview URL: http://127.0.0.1:8000`

#### Voice Control Examples

```
👤 User: "Start YOLOv8 object detection"
🤖 XiaoZhi: "Okay, starting YOLOv8 detection service..."
       YOLOv8 detection service started successfully (camera: usb)
       🎥 Preview URL: http://192.168.1.100:8000
       [AI calls: start_yolov8_detection("usb")]

👤 User: "Stop YOLOv8 detection"
🤖 XiaoZhi: "YOLOv8 detection has been stopped"
       [AI calls: stop_yolov8_detection()]

👤 User: "What's the YOLOv8 detection status?"
🤖 XiaoZhi: "YOLOv8 object detection is running, uptime 120 seconds"
       [AI calls: get_yolov8_status()]
```

## Configuration

### Server Configuration
The program automatically retrieves MQTT connection configuration from the server, no manual configuration needed.

### Audio Parameters
- **Recording Sample Rate**: 16kHz
- **Playback Sample Rate**: 24kHz  
- **Audio Format**: Opus compression
- **Buffer Size**: 960 frames (60ms latency)

### Device Information
The program automatically collects the following device information for server identification:
- MAC address (unique device identifier)
- Memory capacity and available space
- Storage capacity information

## Troubleshooting

### Common Issues

#### Q1: Audio device error on startup
```bash
# Solutions
# 1. Check audio device permissions
sudo usermod -a -G audio $USER

# 2. Restart audio service
pulseaudio -k && pulseaudio --start

# 3. Check device connection
lsusb | grep -i audio
```

#### Q2: Network connection failure
```bash
# Solutions
# 1. Check network connection
ping api.tenclass.net

# 2. Check firewall settings
sudo ufw allow 8883/tcp

# 3. View detailed logs
tail -f xiaozhi.log
```

#### Q3: Input overflow error
```bash
# Issue: Microphone buffer overflow
# Solution: Program automatically skips overflowed frames

# If occurs frequently, try:
# 1. Reduce system load
# 2. Use better USB audio device
# 3. Check CPU usage
htop
```

#### Q4: High audio latency
- Use wired network connection
- Ensure system load is not high
- Check USB audio device connection stability

#### Q5: MCP service cannot start
```bash
# Check if MCP_ENDPOINT is set
echo $MCP_ENDPOINT

# Set MCP endpoint
export MCP_ENDPOINT=ws://your-server:8765
```

#### Q6: TROS environment not found

**Install TROS on RDK S100:**
```bash
# Update package sources
sudo apt update

# Install TROS
sudo apt install tros-humble
```

**Configure TROS environment:**
```bash
# Source TROS environment
source /opt/tros/humble/setup.bash

# Set permanently
echo "source /opt/tros/humble/setup.bash" >> ~/.bashrc
```

### Log Viewing
The program generates a `xiaozhi.log` file during runtime, containing detailed runtime information and error diagnostics.

## Development & Contribution

### Acknowledgments
- **Original Project**: [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) by [@huangjunsen0406](https://github.com/huangjunsen0406)
- **Development Team**: D-Robotics Team
- **Community Support**: RDK Developer Community

### How to Contribute
1. **Report Issues**: Submit bugs in GitHub Issues
2. **Feature Requests**: Propose improvements in Discussions
3. **Code Contribution**: Fork the project and submit Pull Requests
4. **Documentation**: Help improve usage documentation

## License

This project is licensed under the [MIT License](LICENSE).

## Related Links

- [py-xiaozhi Original Project](https://github.com/huangjunsen0406/py-xiaozhi)
- [RDK Series Development Boards](https://developer.d-robotics.cc/)
- [DiGua Robotics Official Website](https://d-robotics.cc/)

---

**⭐ If this project helps you, please give it a Star!**

---

*Last Updated: October 15, 2025*
