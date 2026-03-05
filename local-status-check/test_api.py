"""
API 测试脚本
用于测试 Local Status Check API
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_health():
    """测试健康检查接口"""
    print("=== 测试健康检查 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_status():
    """测试完整状态接口"""
    print("=== 测试完整状态接口 ===")
    response = requests.get(f"{BASE_URL}/status")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"系统信息: {json.dumps(data.get('system', {}), indent=2, ensure_ascii=False)}")
    print(f"文件系统数量: {len(data.get('filesystem', []))}")
    print(f"网络接口数量: {len(data.get('network', {}).get('interfaces', {}))}")
    print()


def test_system():
    """测试系统信息接口"""
    print("=== 测试系统信息接口 ===")
    response = requests.get(f"{BASE_URL}/status/system")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_filesystem():
    """测试文件系统信息接口"""
    print("=== 测试文件系统信息接口 ===")
    response = requests.get(f"{BASE_URL}/status/filesystem")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"文件系统信息:")
    for fs in data:
        print(f"  - {fs['mountpoint']}: {fs['percent_used']}% 已使用 ({fs['used_gb']}GB / {fs['total_gb']}GB)")
    print()


def test_network():
    """测试网络状态接口"""
    print("=== 测试网络状态接口 ===")
    response = requests.get(f"{BASE_URL}/status/network")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"网络接口:")
    for iface, addrs in data.get('interfaces', {}).items():
        print(f"  - {iface}:")
        for addr in addrs:
            print(f"    {addr['family']}: {addr['address']}")
    print(f"总流量: 发送 {data['total_bytes_sent']} 字节, 接收 {data['total_bytes_received']} 字节")
    print()


if __name__ == "__main__":
    try:
        print("开始测试 Local Status Check API\n")

        test_health()
        test_status()
        test_system()
        test_filesystem()
        test_network()

        print("所有测试完成!")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到 API 服务，请确保服务已启动")
    except Exception as e:
        print(f"错误: {e}")
