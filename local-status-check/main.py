"""
本地状态检查 Web 接口
提供系统状态、文件系统和网络状态查询接口
"""

from flask import Flask, jsonify
import platform
import os
import psutil
import socket
import json
from datetime import datetime

app = Flask(__name__)


def get_system_info():
    """获取系统基本信息"""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "current_time": datetime.now().isoformat(),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=1)
    }


def get_filesystem_info():
    """获取文件系统信息"""
    filesystems = []
    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            filesystems.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": round(usage.percent, 2)
            })
        except PermissionError:
            continue
        except Exception as e:
            continue

    return filesystems


def get_network_info():
    """获取网络状态信息"""
    # 获取网络接口信息
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        addresses = []
        for addr in addrs:
            addresses.append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask if hasattr(addr, 'netmask') else None,
                "broadcast": addr.broadcast if hasattr(addr, 'broadcast') else None
            })
        interfaces[name] = addresses

    # 获取网络统计
    io_counters = psutil.net_io_counters()

    return {
        "interfaces": interfaces,
        "total_bytes_sent": io_counters.bytes_sent,
        "total_bytes_received": io_counters.bytes_recv,
        "total_packets_sent": io_counters.packets_sent,
        "total_packets_received": io_counters.packets_recv,
        "total_errors_in": io_counters.errin,
        "total_errors_out": io_counters.errout
    }


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/status', methods=['GET'])
def get_status():
    """获取系统状态接口"""
    return jsonify({
        "system": get_system_info(),
        "filesystem": get_filesystem_info(),
        "network": get_network_info()
    })


@app.route('/status/system', methods=['GET'])
def get_system():
    """获取系统信息接口"""
    return jsonify(get_system_info())


@app.route('/status/filesystem', methods=['GET'])
def get_filesystem():
    """获取文件系统信息接口"""
    return jsonify(get_filesystem_info())


@app.route('/status/network', methods=['GET'])
def get_network():
    """获取网络状态接口"""
    return jsonify(get_network_info())


@app.route('/', methods=['GET'])
def index():
    """API 文档页面"""
    return jsonify({
        "name": "Local Status Check API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "健康检查",
            "/status": "完整系统状态（系统+文件系统+网络）",
            "/status/system": "系统信息",
            "/status/filesystem": "文件系统信息",
            "/status/network": "网络状态信息"
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
