# 小智AI语音助手 - RDK X5

> **地瓜机器人团队** 官方RDK X5平台适配项目  

## 🎯 项目简介

本项目是小智AI语音助手在RDK X5嵌入式开发板上的专业适配版本，实现了完整的实时语音交互功能。通过针对ARM架构和嵌入式环境的深度优化，提供了稳定、高效的AI语音交互体验。

**特别感谢** [@huangjunsen0406](https://github.com/huangjunsen0406) 的 [py-xiaozhi项目](https://github.com/huangjunsen0406/py-xiaozhi) 提供的技术基础支持。

### ✨ 核心特性

- 🚀 **专为RDK X5优化**: ARM架构深度适配，性能卓越
- 🎙️ **实时语音交互**: 16kHz/24kHz采样率，超低延迟处理
- 🔒 **端到端加密**: AES-128-CTR模式保障数据安全
- 🌐 **双协议支持**: MQTT控制 + UDP音频传输
- 📱 **简单易用**: 空格键交互，一键启动
- 🔧 **单文件部署**: 无复杂依赖，快速部署

## 🏗️ 系统架构

```
用户交互 ←→ 音频处理 ←→ 加密传输 ←→ AI服务
    ↓           ↓          ↓         ↓
 空格键控制   Opus编解码   AES加密    智能对话
 状态显示    实时流处理    UDP传输    语音合成
```

## 📋 环境要求

### 硬件要求
- **开发板**: RDK X5
- **音频**: 麦克风和扬声器
- **网络**: WiFi或以太网连接

### 软件依赖
- **系统**: rdkos 3.0.0+
- **Python**: 3.10+
- **音频库**: ALSA + PulseAudio

## 🚀 快速开始

### 1. 系统准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装系统依赖
sudo apt install python3 python3-pip python3-dev build-essential -y
sudo apt install libasound2-dev portaudio19-dev libopus-dev -y
sudo apt install alsa-utils pulseaudio-utils -y
```

### 2. 安装Python依赖

```bash
# 安装核心依赖包
pip3 install paho-mqtt==1.6.1
pip3 install PyAudio==0.2.11
pip3 install opuslib==3.0.1
pip3 install cryptography==41.0.7
pip3 install requests==2.31.0
```

### 3. 音频设备配置

```bash
# 检查音频设备
aplay -l    # 查看播放设备
arecord -l  # 查看录制设备

# 测试音频功能
arecord -f cd -t wav -d 3 test.wav  # 录制3秒测试
aplay test.wav                       # 播放测试
```

### 4. 运行程序

```bash
# 下载并运行
wget https://github.com/D-Robotics/xiaozhi-in-rdk/main/xiaozhi-in-rdkx5.py
python3 xiaozhi-in-rdkx5.py
```

## 🎮 使用指南

### 启动程序
```bash
python3 xiaozhi-in-rdkx5.py
```

### 操作说明
| 操作         | 按键         | 说明                            |
| ------------ | ------------ | ------------------------------- |
| **开始录音** | 按住 `SPACE` | 开始语音输入，显示"🎤 倾听中..." |
| **结束录音** | 松开 `SPACE` | 结束录音，等待AI处理和回复      |
| **退出程序** | 按 `q`       | 优雅退出程序，清理所有资源      |

### 状态提示
- 🔗 **连接会话**: 建立与服务器的连接
- 🎤 **倾听中**: 正在录制您的语音
- ⏹️ **等待回复**: 处理语音并等待AI回复
- 🔊 **播放中**: AI正在回复
- ✅ **播放完成**: 回复播放结束

## 🔧 配置说明

### 服务器配置
程序会自动从服务器获取MQTT连接配置，无需手动配置。

### 音频参数
- **录音采样率**: 16kHz
- **播放采样率**: 24kHz  
- **音频格式**: Opus压缩
- **缓冲区大小**: 960帧 (60ms延迟)

### 设备信息
程序会自动收集以下设备信息用于服务器识别：
- MAC地址（设备唯一标识）
- 内存容量和可用空间
- 存储容量信息

## 🛠️ 故障排除

### 常见问题

#### Q1: 程序启动时提示音频设备错误
```bash
# 解决方案
# 1. 检查音频设备权限
sudo usermod -a -G audio $USER

# 2. 重启音频服务
pulseaudio -k && pulseaudio --start

# 3. 检查设备连接
lsusb | grep -i audio
```

#### Q2: 网络连接失败
```bash
# 解决方案
# 1. 检查网络连接
ping api.tenclass.net

# 2. 检查防火墙设置
sudo ufw allow 8883/tcp

# 3. 查看详细日志
tail -f xiaozhi.log
```

#### Q3: 音频延迟过大
- 使用有线网络连接
- 确保系统负载不高
- 检查USB音频设备连接稳定性

### 日志查看
程序运行时会生成 `xiaozhi.log` 日志文件，包含详细的运行信息和错误诊断。

## 📊 性能特性

- **音频延迟**: 约80ms端到端延迟
- **CPU占用**: 正常对话15-25%
- **内存占用**: 45-60MB
- **网络带宽**: 32kbps音频流
- **连续运行**: 支持72小时稳定运行

## 🤝 开发贡献

### 致谢
- **原始项目**: [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) by [@huangjunsen0406](https://github.com/huangjunsen0406)
- **开发团队**: 地瓜机器人团队
- **社区支持**: RDK开发者社区

### 贡献方式
1. 🐛 **提交问题**: 在GitHub Issues中报告bug
2. 💡 **功能建议**: 在Discussions中提出改进建议
3. 🔧 **代码贡献**: Fork项目并提交Pull Request
4. 📖 **文档改进**: 帮助完善使用文档

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 🔗 相关链接

- [py-xiaozhi原始项目](https://github.com/huangjunsen0406/py-xiaozhi)
- [RDK X5开发板官网](https://developer.d-robotics.cc/)
- [地瓜机器人官网](https://d-robotics.cc/)

---

**⭐ 如果这个项目对您有帮助，请给个Star支持！**

---

*最后更新: 2025年8月25日*