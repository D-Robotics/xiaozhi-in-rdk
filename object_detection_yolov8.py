#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
YOLOv8目标检测模块 - RDK系列
=====================================

基于MCP协议的TROS YOLOv8目标检测工具,支持USB和MIPI摄像头。

支持板卡:
- RDK X3 ✓
- RDK X5 ✓
- RDK S100 ✓

功能:
- 启动/停止YOLOv8目标检测服务
- 支持USB和MIPI摄像头切换
- 配置检测参数
- 查询检测状态
"""

from mcp.server.fastmcp import FastMCP
import sys
import logging
import subprocess
import os
import signal
import time
import json

logger = logging.getLogger('YOLOv8Detection')

# Fix UTF-8 encoding for Windows/Linux
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

def get_wlan0_ip():
    """获取wlan0接口的IP地址,未连接时返回127.0.0.1"""
    try:
        result = subprocess.run(['ip', 'addr', 'show', 'wlan0'],
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'inet ' in line:
                    ip = line.strip().split()[1].split('/')[0]
                    return ip
    except Exception as e:
        logger.warning(f"无法读取wlan0 IP地址: {e}")
    return '127.0.0.1'

# 全局变量保存检测进程
detection_process = None
detection_config = {
    "camera_type": "usb",  # usb 或 mipi
    "status": "stopped",
    "start_time": None,
    "pid": None
}

# Create an MCP server
mcp = FastMCP("YOLOv8Detection")

@mcp.tool()
def start_yolov8_detection(camera_type: str = "usb") -> dict:
    """
    启动TROS YOLOv8目标检测服务

    此工具用于启动基于YOLOv8的目标检测服务,支持USB和MIPI两种摄像头类型。
    启动后会运行TROS launch文件进行实时目标检测。

    参数:
        camera_type: 摄像头类型,可选值:
            - "usb": USB摄像头 (默认)
            - "mipi": MIPI摄像头

    返回:
        dict: 包含以下字段:
            - success (bool): 是否成功启动
            - message (str): 操作结果消息
            - status (str): 当前状态 ("running", "failed", "error")
            - pid (int, 可选): 进程ID
            - camera_type (str, 可选): 使用的摄像头类型

    示例:
        # 使用USB摄像头启动
        start_yolov8_detection("usb")

        # 使用MIPI摄像头启动
        start_yolov8_detection("mipi")
    """
    global detection_process, detection_config

    try:
        # 验证camera_type参数
        if camera_type.lower() not in ["usb", "mipi"]:
            return {
                "success": False,
                "message": f"无效的摄像头类型: {camera_type}. 必须是 'usb' 或 'mipi'",
                "status": "error"
            }

        camera_type = camera_type.lower()

        # 检查是否已经在运行
        if detection_process and detection_process.poll() is None:
            return {
                "success": False,
                "message": f"YOLOv8检测服务已经在运行中 (摄像头: {detection_config['camera_type']})",
                "status": "running",
                "config": detection_config
            }

        logger.info(f"准备启动YOLOv8检测服务,摄像头类型: {camera_type}")

        # 设置环境变量
        env = os.environ.copy()
        env['CAM_TYPE'] = camera_type

        # TROS环境变量(如果需要)
        if 'ROS_DOMAIN_ID' not in env:
            env['ROS_DOMAIN_ID'] = '0'

        # 构建TROS启动命令
        # 假设YOLOv8的launch文件是 yolov8_detection.launch.py
        # 根据实际情况调整包名和launch文件名
        cmd = [
            "ros2", "launch",
            "dnn_node_example", "dnn_node_example.launch.py",
            f"dnn_example_config_file:=config/yolov8workconfig.json"
        ]

        logger.info(f"执行命令: {' '.join(cmd)}")
        logger.info(f"环境变量 CAM_TYPE={camera_type}")

        # 启动进程
        detection_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
            preexec_fn=os.setpgrp
        )

        # 等待一段时间确认启动
        time.sleep(3)

        # 检查进程是否成功启动
        if detection_process.poll() is not None:
            # 进程已经退出,读取错误信息
            _, stderr = detection_process.communicate()
            error_msg = f"YOLOv8检测启动失败: {stderr[:500]}"
            logger.error(error_msg)
            detection_process = None
            return {
                "success": False,
                "message": error_msg,
                "status": "failed"
            }

        # 获取wlan0 IP地址
        wlan0_ip = get_wlan0_ip()

        # 更新配置
        detection_config.update({
            "camera_type": camera_type,
            "status": "running",
            "start_time": time.time(),
            "pid": detection_process.pid,
            "preview_url": f"http://{wlan0_ip}:8000"
        })

        logger.info(f"YOLOv8检测已启动, PID: {detection_process.pid}, 摄像头: {camera_type}")

        # 构建返回消息
        if wlan0_ip == '127.0.0.1':
            preview_msg = f"YOLOv8检测服务启动成功 (摄像头: {camera_type})\n⚠️  wlan0未连接，预览地址: http://{wlan0_ip}:8000"
        else:
            preview_msg = f"YOLOv8检测服务启动成功 (摄像头: {camera_type})\n🎥 预览地址: http://{wlan0_ip}:8000"

        return {
            "success": True,
            "message": preview_msg,
            "status": "running",
            "pid": detection_process.pid,
            "camera_type": camera_type,
            "preview_url": f"http://{wlan0_ip}:8000"
        }

    except FileNotFoundError as e:
        error_msg = "TROS环境未找到,请确保已安装并source了TROS环境"
        logger.error(f"{error_msg}: {str(e)}")
        return {
            "success": False,
            "message": error_msg,
            "status": "error",
            "hint": "运行: source /opt/tros/humble/setup.bash (或对应的TROS版本)"
        }
    except Exception as e:
        error_msg = f"启动YOLOv8检测时发生错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "message": error_msg,
            "status": "error"
        }

@mcp.tool()
def stop_yolov8_detection() -> dict:
    """
    停止YOLOv8目标检测服务

    此工具用于停止正在运行的YOLOv8目标检测服务。
    会先尝试优雅关闭(SIGTERM),超时后强制kill。

    返回:
        dict: 包含以下字段:
            - success (bool): 是否成功停止
            - message (str): 操作结果消息
            - status (str): 当前状态 ("stopped", "error")
            - runtime_seconds (float, 可选): 运行时长(秒)

    示例:
        stop_yolov8_detection()
    """
    global detection_process, detection_config

    try:
        if detection_process is None or detection_process.poll() is not None:
            return {
                "success": False,
                "message": "YOLOv8检测服务未在运行",
                "status": "stopped"
            }

        logger.info(f"停止YOLOv8检测进程 PID: {detection_process.pid}")

        try:
            # 终止整个进程组
            pgid = os.getpgid(detection_process.pid)
            os.killpg(pgid, signal.SIGTERM)
            logger.info(f"已向进程组 {pgid} 发送SIGTERM信号")
        except ProcessLookupError:
            logger.warning("进程组已不存在")
        except Exception as e:
            logger.warning(f"终止进程组失败: {e}, 尝试终止主进程")
            detection_process.terminate()

        # 等待进程结束(最多5秒)
        try:
            detection_process.wait(timeout=5)
            logger.info("YOLOv8检测进程已优雅退出")
        except subprocess.TimeoutExpired:
            logger.warning("进程未响应SIGTERM,执行强制kill")
            try:
                pgid = os.getpgid(detection_process.pid)
                os.killpg(pgid, signal.SIGKILL)
            except:
                detection_process.kill()
            detection_process.wait()

        # 计算运行时长
        runtime = None
        if detection_config["start_time"]:
            runtime = time.time() - detection_config["start_time"]

        # 更新状态
        old_camera = detection_config["camera_type"]
        detection_config["status"] = "stopped"
        detection_config["start_time"] = None
        detection_config["pid"] = None
        detection_process = None

        return {
            "success": True,
            "message": f"YOLOv8检测服务已停止 (摄像头: {old_camera})",
            "status": "stopped",
            "runtime_seconds": runtime
        }

    except Exception as e:
        error_msg = f"停止YOLOv8检测时发生错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "message": error_msg,
            "status": "error"
        }

@mcp.tool()
def get_yolov8_status() -> dict:
    """
    获取YOLOv8目标检测服务状态

    此工具用于查询当前YOLOv8检测服务的运行状态和配置信息。

    返回:
        dict: 包含以下字段:
            - success (bool): 查询是否成功
            - status (str): 当前状态 ("running", "stopped")
            - pid (int, 可选): 进程ID
            - camera_type (str, 可选): 摄像头类型
            - runtime_seconds (float, 可选): 运行时长(秒)
            - message (str, 可选): 额外信息

    示例:
        get_yolov8_status()
    """
    global detection_process, detection_config

    try:
        # 检查进程状态
        is_running = detection_process is not None and detection_process.poll() is None

        if is_running:
            runtime = time.time() - detection_config["start_time"] if detection_config["start_time"] else 0
            return {
                "success": True,
                "status": "running",
                "pid": detection_process.pid,
                "camera_type": detection_config["camera_type"],
                "runtime_seconds": runtime,
                "message": f"YOLOv8检测服务运行中 (摄像头: {detection_config['camera_type']})"
            }
        else:
            return {
                "success": True,
                "status": "stopped",
                "message": "YOLOv8检测服务未运行"
            }

    except Exception as e:
        error_msg = f"查询状态时发生错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "message": error_msg,
            "status": "error"
        }

@mcp.tool()
def restart_yolov8_detection(camera_type: str = "usb") -> dict:
    """
    重启YOLOv8目标检测服务

    此工具用于重启YOLOv8检测服务,可以在重启时切换摄像头类型。
    会先停止当前服务,然后使用新参数重新启动。

    参数:
        camera_type: 摄像头类型,可选值:
            - "usb": USB摄像头 (默认)
            - "mipi": MIPI摄像头

    返回:
        dict: 包含以下字段:
            - success (bool): 重启是否成功
            - message (str): 操作结果消息
            - status (str): 当前状态
            - stop_result (dict): 停止操作的结果
            - start_result (dict): 启动操作的结果

    示例:
        # 重启并切换到MIPI摄像头
        restart_yolov8_detection("mipi")
    """
    # 先停止
    stop_result = stop_yolov8_detection()
    time.sleep(1)

    # 再启动
    start_result = start_yolov8_detection(camera_type)

    return {
        "success": start_result["success"],
        "message": f"重启完成: {start_result['message']}",
        "status": start_result["status"],
        "stop_result": stop_result,
        "start_result": start_result
    }

@mcp.tool()
def switch_camera(camera_type: str) -> dict:
    """
    切换摄像头类型

    此工具用于在USB和MIPI摄像头之间切换。
    如果检测服务正在运行,会自动重启以应用新的摄像头设置。

    参数:
        camera_type: 目标摄像头类型
            - "usb": USB摄像头
            - "mipi": MIPI摄像头

    返回:
        dict: 操作结果

    示例:
        # 切换到MIPI摄像头
        switch_camera("mipi")
    """
    global detection_process, detection_config

    if camera_type.lower() not in ["usb", "mipi"]:
        return {
            "success": False,
            "message": f"无效的摄像头类型: {camera_type}",
            "status": "error"
        }

    camera_type = camera_type.lower()

    # 如果服务正在运行,重启以应用新配置
    if detection_process and detection_process.poll() is None:
        if detection_config["camera_type"] == camera_type:
            return {
                "success": True,
                "message": f"已经在使用{camera_type}摄像头",
                "status": "running",
                "camera_type": camera_type
            }
        else:
            return restart_yolov8_detection(camera_type)
    else:
        # 服务未运行,仅更新配置
        detection_config["camera_type"] = camera_type
        return {
            "success": True,
            "message": f"摄像头类型已设置为{camera_type},下次启动时生效",
            "status": "stopped",
            "camera_type": camera_type
        }

def cleanup():
    """清理函数,确保进程被正确终止"""
    global detection_process
    if detection_process and detection_process.poll() is None:
        logger.info("清理:停止YOLOv8检测进程")
        try:
            pgid = os.getpgid(detection_process.pid)
            os.killpg(pgid, signal.SIGTERM)
            detection_process.wait(timeout=3)
        except:
            try:
                pgid = os.getpgid(detection_process.pid)
                os.killpg(pgid, signal.SIGKILL)
            except:
                detection_process.kill()

# 注册清理函数
import atexit
atexit.register(cleanup)

# 信号处理
def signal_handler(signum, frame):
    logger.info(f"收到信号 {signum},清理资源...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Start the server
if __name__ == "__main__":
    logger.info("YOLOv8检测MCP服务启动")
    mcp.run(transport="stdio")
