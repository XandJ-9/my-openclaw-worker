# Local Status Check

本地系统状态检查 Web 接口，使用 Python Flask 框架开发。

## 功能特性

- 🖥️ 系统信息查询（操作系统、CPU、内存等）
- 💾 文件系统信息（磁盘空间、分区信息）
- 🌐 网络状态（网络接口、流量统计）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

服务将在 `http://localhost:5000` 启动。

## API 接口

### 1. 健康检查

```bash
GET /health
```

返回服务健康状态。

### 2. 完整系统状态

```bash
GET /status
```

返回系统、文件系统和网络状态的完整信息。

### 3. 系统信息

```bash
GET /status/system
```

返回系统基本信息：
- 操作系统类型和版本
- 主机名
- Python 版本
- CPU 信息
- 当前时间

### 4. 文件系统信息

```bash
GET /status/filesystem
```

返回所有磁盘分区的信息：
- 设备名称
- 挂载点
- 文件系统类型
- 总容量、已用空间、剩余空间
- 使用率百分比

### 5. 网络状态

```bash
GET /status/network
```

返回网络接口和流量统计信息：
- 所有网络接口及其 IP 地址
- 发送/接收的字节数
- 发送/接收的数据包数
- 错误统计

### 6. API 文档

```bash
GET /
```

返回 API 文档页面。

## 示例请求

### 检查健康状态

```bash
curl http://localhost:5000/health
```

### 获取完整系统状态

```bash
curl http://localhost:5000/status
```

### 获取文件系统信息

```bash
curl http://localhost:5000/status/filesystem
```

## 返回格式

所有接口返回 JSON 格式数据。

示例：

```json
{
  "system": {
    "os": "Windows",
    "os_version": "10",
    "hostname": "DESKTOP-XXX",
    "python_version": "3.9.7",
    "architecture": "AMD64",
    "processor": "Intel(R) Core(TM) i7-XXXX",
    "current_time": "2026-03-05T10:00:00",
    "cpu_count": 8,
    "cpu_percent": 12.5
  },
  "filesystem": [
    {
      "device": "C:",
      "mountpoint": "C:\\",
      "fstype": "NTFS",
      "total_gb": 238.47,
      "used_gb": 150.23,
      "free_gb": 88.24,
      "percent_used": 62.95
    }
  ],
  "network": {
    "interfaces": {
      "Ethernet": [...]
    },
    "total_bytes_sent": 123456789,
    "total_bytes_received": 987654321,
    ...
  }
}
```

## 技术栈

- **框架**: Flask 3.0.0
- **系统信息**: psutil 5.9.6
- **语言**: Python 3.x

## 注意事项

- 需要管理员权限才能获取某些系统信息
- 网络接口信息取决于系统配置
- 磁盘信息可能因权限限制而无法获取部分分区

## 许可证

MIT License
