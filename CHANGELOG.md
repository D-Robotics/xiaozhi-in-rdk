# 更新日志 / Changelog

所有重要的项目更改都将记录在此文件中。  
All notable changes to this project will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)  
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [1.0.0] - 2024-08-25

### 新增 / Added
- 🎉 首次发布RDK X5适配版本 / Initial release for RDK X5 platform
- 🎙️ 实时语音交互功能 / Real-time voice interaction capabilities
- 🔒 AES-128-CTR端到端加密 / AES-128-CTR end-to-end encryption
- 🌐 MQTT+UDP双协议支持 / MQTT+UDP dual protocol support
- 📱 空格键交互控制 / Space key interaction control
- 🖥️ 终端状态显示 / Terminal status display
- 🔧 单文件部署方案 / Single file deployment solution

### RDK X5 特定优化 / RDK X5 Specific Optimizations
- ⚡ ARM架构深度适配 / Deep ARM architecture adaptation
- 🎵 ALSA音频系统优化 / ALSA audio system optimization
- 🔇 音频错误输出抑制 / Audio error output suppression
- 💾 内存和存储信息获取 / Memory and storage information acquisition
- 🏷️ MAC地址多策略获取 / Multiple MAC address acquisition strategies
- 🖥️ 终端字符模式支持 / Terminal character mode support

### 技术实现 / Technical Implementation
- 📡 自动服务器配置获取 / Automatic server configuration retrieval
- 🔄 智能重连机制 / Smart reconnection mechanism
- 💓 心跳保活机制 / Heartbeat keep-alive mechanism
- 🔀 多线程音频处理 / Multi-threaded audio processing
- 🎚️ Opus音频编解码优化 / Opus audio codec optimization
- 📊 设备硬件信息上报 / Device hardware information reporting

### 文档和工具 / Documentation and Tools
- 📖 中英双语README文档 / Bilingual README documentation
- 📦 自动化安装脚本 / Automated installation script
- 📋 完整依赖管理 / Complete dependency management
- 📄 MIT开源许可 / MIT open source license

### 致谢 / Acknowledgments
- 🙏 参考 [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) 开源项目
- 🤝 感谢 [@huangjunsen0406](https://github.com/huangjunsen0406) 提供技术基础

---

## 版本规则 / Versioning

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。  
This project follows [Semantic Versioning](https://semver.org/) specification.

- **主版本号 / Major**: 不兼容的API修改 / Incompatible API changes
- **次版本号 / Minor**: 向下兼容的功能性新增 / Backward compatible functionality additions  
- **修订号 / Patch**: 向下兼容的问题修正 / Backward compatible bug fixes

## 反馈和建议 / Feedback and Suggestions

- 🐛 **Bug报告 / Bug Reports**: [GitHub Issues](https://github.com/D-Robotics/xiaozhi-in-rdk/issues)
- 💡 **功能建议 / Feature Requests**: [GitHub Discussions](https://github.com/D-Robotics/xiaozhi-in-rdk/discussions)
- 📧 **技术支持 / Technical Support**: 