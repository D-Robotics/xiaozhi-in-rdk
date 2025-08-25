# XiaoZhi AI Voice Assistant - RDK X5

> **DiGua Robotics Team** Official RDK X5 Platform Adaptation Project

## 🎯 Project Overview

This project is a professional adaptation of XiaoZhi AI Voice Assistant for the RDK X5 embedded development board, implementing complete real-time voice interaction capabilities. Through deep optimization for ARM architecture and embedded environments, it provides stable and efficient AI voice interaction experience.

**Special Thanks** to [@huangjunsen0406](https://github.com/huangjunsen0406) for the [py-xiaozhi project](https://github.com/huangjunsen0406/py-xiaozhi) providing technical foundation support.

### ✨ Key Features

- 🚀 **Optimized for RDK X5**: Deep ARM architecture adaptation with excellent performance
- 🎙️ **Real-time Voice Interaction**: 16kHz/24kHz sampling rate with ultra-low latency
- 🔒 **End-to-End Encryption**: AES-128-CTR mode ensuring data security
- 🌐 **Dual Protocol Support**: MQTT control + UDP audio transmission
- 📱 **Simple to Use**: Space key interaction, one-click startup
- 🔧 **Single File Deployment**: No complex dependencies, quick deployment

## 🏗️ System Architecture

```
User Input ←→ Audio Processing ←→ Encrypted Transmission ←→ AI Service
    ↓              ↓                    ↓                    ↓
Space Key      Opus Codec           AES Encryption      Smart Dialog
Status Display Real-time Stream      UDP Transport      Voice Synthesis
```

## 📋 Requirements

### Hardware Requirements
- **Board**: RDK X5
- **Audio**: Microphone and speaker (ALSA supported)
- **Network**: WiFi or Ethernet connection

### Software Dependencies
- **OS**: rdkos 3.0.0+
- **Python**: 3.10+
- **Audio**: ALSA + PulseAudio

## 🚀 Quick Start

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
# Install core packages
pip3 install paho-mqtt==1.6.1
pip3 install PyAudio==0.2.11
pip3 install opuslib==3.0.1
pip3 install cryptography==41.0.7
pip3 install requests==2.31.0
```

### 3. Audio Device Configuration

```bash
# Check audio devices
aplay -l    # List playback devices
arecord -l  # List capture devices

# Test audio functionality
arecord -f cd -t wav -d 3 test.wav  # Record 3-second test
aplay test.wav                       # Play test
```

### 4. Run the Program

```bash
# Download and run
wget https://github.com/D-Robotics/xiaozhi-in-rdk/main/xiaozhi-in-rdkx5.py
python3 xiaozhi-in-rdkx5.py
```

## 🎮 Usage Guide

### Starting the Program
```bash
python3 xiaozhi-in-rdkx5.py
```

### Operation Instructions
| Action              | Key             | Description                                        |
| ------------------- | --------------- | -------------------------------------------------- |
| **Start Recording** | Hold `SPACE`    | Begin voice input, shows "🎤 Listening..."          |
| **Stop Recording**  | Release `SPACE` | End recording, wait for AI processing and response |
| **Exit Program**    | Press `q`       | Gracefully exit program and clean up resources     |

### Status Indicators
- 🔗 **Connecting Session**: Establishing connection to server
- 🎤 **Listening**: Recording your voice input
- ⏹️ **Waiting for Reply**: Processing voice and waiting for AI response
- 🔊 **Playing**: AI is responding
- ✅ **Playback Complete**: Response playback finished

## 🔧 Configuration

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

## 🛠️ Troubleshooting

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

#### Q3: High audio latency
- Use wired network connection
- Ensure system load is not high
- Check USB audio device connection stability

### Log Viewing
The program generates a `xiaozhi.log` file during runtime, containing detailed runtime information and error diagnostics.

## 📊 Performance Characteristics

- **Audio Latency**: ~80ms end-to-end latency
- **CPU Usage**: 15-25% during normal conversation
- **Memory Usage**: 45-60MB
- **Network Bandwidth**: 32kbps audio stream
- **Continuous Operation**: Supports 72-hour stable operation

## 🤝 Development & Contribution

### Acknowledgments
- **Original Project**: [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) by [@huangjunsen0406](https://github.com/huangjunsen0406)
- **Development Team**: D-Robotics Team
- **Community Support**: RDK Developer Community

### How to Contribute
1. 🐛 **Report Issues**: Submit bugs in GitHub Issues
2. 💡 **Feature Requests**: Propose improvements in Discussions
3. 🔧 **Code Contribution**: Fork the project and submit Pull Requests
4. 📖 **Documentation**: Help improve usage documentation

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🔗 Related Links

- [py-xiaozhi Original Project](https://github.com/huangjunsen0406/py-xiaozhi)
- [RDK X5 Development Board](https://developer.d-robotics.cc/)
- [DiGua Robotics Official Website](https://d-robotics.cc/)

---

**⭐ If this project helps you, please give it a Star!**

---

*Last Updated: August 25, 2025*