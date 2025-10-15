# 更新日志 / Changelog

所有重要的项目更改都将记录在此文件中。
All notable changes to this project will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [1.2.0] - 2025-10-15

### 新增 / Added
- 支持全系列RDK板卡 (X3/X5/S100) / Support for all RDK boards (X3/X5/S100)
- USB音频设备推荐和配置说明 / USB audio device recommendations and configuration guide
- ALSA默认设备配置指南 / ALSA default device configuration guide
- RDK S100 TROS安装说明 / RDK S100 TROS installation guide

### 改进 / Changed
- 统一使用YOLOv8目标检测 / Unified to YOLOv8 object detection only
- 删除YOLOv5相关内容 / Removed YOLOv5 related content
- 主程序文件重命名: xiaozhi-in-rdkx5.py → xiaozhi-in-rdk.py / Main program renamed
- 优化进程管理，完全清理ROS2 launch子进程 / Improved process management for complete ROS2 launch cleanup
- 更新文档，适配全系列RDK板卡 / Updated documentation for all RDK boards

### 修复 / Fixed
- 修复stop_yolov8_detection()无法完全终止所有节点的问题 / Fixed incomplete node termination in stop_yolov8_detection()
- 使用进程组管理确保所有子进程正确清理 / Use process group for proper subprocess cleanup

### 依赖 / Dependencies
- 添加fastmcp和dotenv依赖 / Added fastmcp and dotenv dependencies

## [1.1.0] - 2025-10-13

### 新增 / Added
- YOLOv8/YOLOv5目标检测MCP服务集成 / YOLOv8/YOLOv5 object detection MCP service integration
- MCP协议支持，AI可调用视觉工具 / MCP protocol support for AI-callable vision tools
- USB/MIPI双摄像头支持 / USB/MIPI dual camera support
- 10个YOLO控制工具 (YOLOv8和YOLOv5各5个) / 10 YOLO control tools (5 for each model):
  - start_yolov8_detection() / start_yolov5_detection() - 启动检测 / Start detection
  - stop_yolov8_detection() / stop_yolov5_detection() - 停止检测 / Stop detection
  - get_yolov8_status() / get_yolov5_status() - 查询状态 / Get status
  - restart_yolov8_detection() / restart_yolov5_detection() - 重启服务 / Restart service
  - switch_camera() - 切换摄像头 / Switch camera (两个模型共用)

### 技术实现 / Technical Implementation
- MCP WebSocket通信管道 / MCP WebSocket communication pipe
- TROS环境集成 / TROS environment integration
- 进程生命周期管理 / Process lifecycle management
- 自动重连和资源清理 / Auto-reconnection and resource cleanup
- 环境变量配置支持 / Environment variable configuration support

### 文档 / Documentation
- 更新README_cn.md和README.md，整合MCP使用说明 / Updated both READMEs with MCP integration
- 简化依赖配置，使用最新版本 / Simplified dependencies with latest versions
- 新增YOLOv8和YOLOv5语音控制示例 / Added voice control examples for both models
- 添加预览网址说明 / Added preview URL documentation

### 文件结构 / File Structure
- object_detection_yolov8.py - YOLOv8检测模块 / YOLOv8 detection module
- object_detection_yolov5.py - YOLOv5检测模块 / YOLOv5 detection module
- mcp_pipe.py - MCP通信管道 / MCP communication pipe
- mcp_config.json - MCP配置文件 / MCP configuration (支持两个模型)
- requirements.txt - 更新依赖列表 / Updated dependencies

## [1.0.0] - 2024-08-25

### 新增 / Added
- 首次发布RDK X5适配版本 / Initial release for RDK X5 platform
- 实时语音交互功能 / Real-time voice interaction capabilities
- AES-128-CTR端到端加密 / AES-128-CTR end-to-end encryption
- MQTT+UDP双协议支持 / MQTT+UDP dual protocol support
- 空格键交互控制 / Space key interaction control
- 终端状态显示 / Terminal status display
- 单文件部署方案 / Single file deployment solution

### RDK X5 特定优化 / RDK X5 Specific Optimizations
- ARM架构深度适配 / Deep ARM architecture adaptation
- ALSA音频系统优化 / ALSA audio system optimization
- 音频错误输出抑制 / Audio error output suppression
- 内存和存储信息获取 / Memory and storage information acquisition
- MAC地址多策略获取 / Multiple MAC address acquisition strategies
- 终端字符模式支持 / Terminal character mode support

### 技术实现 / Technical Implementation
- 自动服务器配置获取 / Automatic server configuration retrieval
- 智能重连机制 / Smart reconnection mechanism
- 心跳保活机制 / Heartbeat keep-alive mechanism
- 多线程音频处理 / Multi-threaded audio processing
- Opus音频编解码优化 / Opus audio codec optimization
- 设备硬件信息上报 / Device hardware information reporting

### 文档和工具 / Documentation and Tools
- 中英双语README文档 / Bilingual README documentation
- 自动化安装脚本 / Automated installation script
- 完整依赖管理 / Complete dependency management
- MIT开源许可 / MIT open source license

---

## 版本规则 / Versioning

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。  
This project follows [Semantic Versioning](https://semver.org/) specification.

- **主版本号 / Major**: 不兼容的API修改 / Incompatible API changes
- **次版本号 / Minor**: 向下兼容的功能性新增 / Backward compatible functionality additions  
- **修订号 / Patch**: 向下兼容的问题修正 / Backward compatible bug fixes

## 反馈和建议 / Feedback and Suggestions

- **Bug报告 / Bug Reports**: [GitHub Issues](https://github.com/D-Robotics/xiaozhi-in-rdk/issues)
- **功能建议 / Feature Requests**: [GitHub Discussions](https://github.com/D-Robotics/xiaozhi-in-rdk/discussions)
- **技术支持 / Technical Support**: [地瓜机器人开发者社区](https://forum.d-robotics.cc/)