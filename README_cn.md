[English](./README.md) | 简体中文
# 小智AI语音助手 - RDK系列

> **地瓜机器人团队** 官方RDK系列平台适配项目

## 项目简介

本项目是小智AI语音助手在RDK系列嵌入式开发板上的专业适配版本，实现了完整的实时语音交互功能。通过针对ARM架构和嵌入式环境的深度优化，提供了稳定、高效的AI语音交互体验。

**支持板卡**: RDK X3 / RDK X5 / RDK S100

**特别感谢** [@huangjunsen0406](https://github.com/huangjunsen0406) 的 [py-xiaozhi项目](https://github.com/huangjunsen0406/py-xiaozhi) 提供的技术基础支持。

### 核心特性

- **全系列RDK支持**: 适配RDK X3/X5/S100，ARM架构深度优化
- **实时语音交互**: 16kHz/24kHz采样率，超低延迟处理
- **端到端加密**: AES-128-CTR模式保障数据安全
- **双协议支持**: MQTT控制 + UDP音频传输
- **YOLOv8目标检测**: MCP协议集成，AI可调用视觉能力
- **简单易用**: 空格键交互，一键启动

## 系统架构

```
用户交互 ←→ 音频处理 ←→ 加密传输 ←→ AI服务
    ↓           ↓          ↓         ↓
 空格键控制   Opus编解码   AES加密    智能对话
 状态显示    实时流处理    UDP传输    语音合成
```

## 环境要求

### 硬件要求
- **开发板**: RDK X3 / RDK X5 / RDK S100
- **音频设备（推荐）**: USB麦克风和USB扬声器
  - 也可使用RDK X5板载音频接口（需配置默认设备）
- **网络**: WiFi或以太网连接

### 软件依赖
- **系统**: rdkos 3.0.0+
- **音频库**: ALSA + PulseAudio

## 快速开始

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
# 安装所有依赖包（自动安装最新版本）
pip3 install -r requirements.txt
```

### 3. 音频设备配置

**推荐使用USB音频设备**以获得最佳体验。如需使用RDK X5板载音频接口，请按以下步骤配置默认设备。

#### 查看音频设备

```bash
# 查看播放设备
aplay -l

# 查看录制设备
arecord -l
```

#### 配置默认音频设备（可选）

如果您使用RDK X5板载音频或需要更改默认设备，请编辑 ALSA 配置文件：

```bash
# 编辑配置文件
nano ~/.asoundrc
```

添加以下内容（根据实际设备编号调整）：

```bash
# 默认播放设备设为 card 1，录音设备 card 0
pcm.!default {
    type asym
    playback.pcm "plughw:1,0"    # 播放 - 支持自动转换
    capture.pcm "plughw:0,0"     # 录音 - 支持自动转换
}

# 控制设备
ctl.!default {
    type hw
    card 1
}
```

验证配置：

```bash
# 查看默认设备
aplay -l | grep default

# 测试音频功能
arecord -f cd -t wav -d 3 test.wav  # 录制3秒测试
aplay test.wav                       # 播放测试

# 若录制的音频没有声音，需调整麦克风音量
alsamixer  # 按F4选择录音设备，用方向键调整音量
# 或使用命令行：
amixer sset Capture 80%  # 设置录音音量为80%
```

### 4. 运行程序

**仅语音助手:**
```bash
python3 xiaozhi-in-rdk.py
```

**语音助手 + YOLOv8检测 (推荐):**

需要开启两个终端分别运行:

```bash
# 终端1: 启动小智主程序 (前台运行,支持空格键交互)
python3 xiaozhi-in-rdk.py
```

```bash
# 终端2: 启动MCP服务
source /opt/tros/humble/setup.bash
export MCP_ENDPOINT=ws://your-server:8765
export CAM_TYPE=usb  # 或 mipi
python3 mcp_pipe.py
```

## 使用指南

### 基础操作
| 操作         | 按键         | 说明                            |
| ------------ | ------------ | ------------------------------- |
| **开始录音** | 按住 `SPACE` | 开始语音输入，显示"🎤倾听中..." |
| **结束录音** | 松开 `SPACE` | 结束录音，等待AI处理和回复      |
| **退出程序** | 按 `q`       | 优雅退出程序，清理所有资源      |

### 状态提示
- **连接会话**: 建立与服务器的连接
- **倾听中**: 正在录制您的语音
- **等待回复**: 处理语音并等待AI回复
- **播放中**: AI正在回复
- **播放完成**: 回复播放结束

### YOLOv8目标检测 (MCP服务)

启用MCP服务后，AI可通过以下工具控制YOLOv8目标检测。支持所有RDK板卡（X3/X5/S100）。

#### YOLOv8可用工具
1. **start_yolov8_detection(camera_type)** - 启动YOLOv8检测服务
2. **stop_yolov8_detection()** - 停止YOLOv8检测服务
3. **get_yolov8_status()** - 查询YOLOv8运行状态
4. **restart_yolov8_detection(camera_type)** - 重启YOLOv8服务
5. **switch_camera(camera_type)** - 切换摄像头

#### 预览网址
启动YOLOv8检测服务后，可通过以下地址查看实时检测画面：
- **本地预览**: `http://127.0.0.1:8000`
- **局域网预览**: `http://<wlan0_IP地址>:8000`

服务启动时会自动检测wlan0连接状态并显示对应的预览地址：
- ✅ wlan0已连接：显示 `🎥 预览地址: http://192.168.x.x:8000`
- ⚠️ wlan0未连接：显示 `⚠️ wlan0未连接，预览地址: http://127.0.0.1:8000`

#### 语音控制示例

```
👤 用户: "启动YOLOv8目标检测"
🤖 小智: "好的，正在启动YOLOv8检测服务..."
       YOLOv8检测服务启动成功 (摄像头: usb)
       🎥 预览地址: http://192.168.1.100:8000
       [AI调用: start_yolov8_detection("usb")]

👤 用户: "停止YOLOv8检测"
🤖 小智: "YOLOv8检测已停止"
       [AI调用: stop_yolov8_detection()]

👤 用户: "YOLOv8检测状态如何?"
🤖 小智: "YOLOv8目标检测正在运行，已运行120秒"
       [AI调用: get_yolov8_status()]
```

## 配置说明

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

## 故障排除

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

#### Q3: 录音溢出错误 (Input overflowed)
```bash
# 问题：麦克风缓冲区溢出
# 解决方案：程序会自动跳过溢出的音频帧，不影响使用

# 如果频繁出现，可尝试：
# 1. 降低系统负载
# 2. 使用更好的USB音频设备
# 3. 检查CPU使用率
top
```

#### Q4: 音频延迟过大
- 使用有线网络连接
- 确保系统负载不高
- 检查USB音频设备连接稳定性

#### Q5: MCP服务无法启动
```bash
# 检查MCP_ENDPOINT是否设置
echo $MCP_ENDPOINT

# 设置MCP端点
export MCP_ENDPOINT=ws://your-server:8765
```

#### Q6: TROS环境未找到

**RDK S100 安装 TROS:**
```bash
# 更新软件源
sudo apt update

# 安装TROS
sudo apt install tros-humble
```

**配置 TROS 环境:**
```bash
# Source TROS环境
source /opt/tros/humble/setup.bash

# 永久设置
echo "source /opt/tros/humble/setup.bash" >> ~/.bashrc
```

### 日志查看
程序运行时会生成 `xiaozhi.log` 日志文件，包含详细的运行信息和错误诊断。

## 开发贡献

### 致谢
- **原始项目**: [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) by [@huangjunsen0406](https://github.com/huangjunsen0406)
- **开发团队**: 地瓜机器人团队
- **社区支持**: RDK开发者社区

### 贡献方式
1. **提交问题**: 在GitHub Issues中报告bug
2. **功能建议**: 在Discussions中提出改进建议
3. **代码贡献**: Fork项目并提交Pull Request
4. **文档改进**: 帮助完善使用文档

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 相关链接

- [py-xiaozhi原始项目](https://github.com/huangjunsen0406/py-xiaozhi)
- [RDK系列开发板官网](https://developer.d-robotics.cc/)
- [地瓜机器人官网](https://d-robotics.cc/)

---

**⭐ 如果这个项目对您有帮助，请给个Star支持！**

---

*最后更新: 2025年10月15日*