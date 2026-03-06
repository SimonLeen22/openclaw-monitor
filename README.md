# OpenClaw Real-time Monitor

A real-time terminal monitor for OpenClaw AI agent session logs.

## Features

- Real-time tracking - Incrementally reads remote OpenClaw .jsonl session logs
- Cyberpunk style - Color-coded blocks for thinking (purple), commands (cyan), and responses (green)
- Deep parsing - Recursively unwraps nested JSON for clean output
- Compact display - Optimized for large screen mirroring
- Full UTF-8 encoding support

## Installation

```bash
pip install rich paramiko
```

## Usage

```bash
python3 monitor.py -H <server_ip> -p <ssh_port> -u <username> -psw <password> -d <openclaw_sessions_dir>
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| -H | Server IP address | (required) |
| -p | SSH port | 22 |
| -u | SSH username | root |
| -psw | SSH password | (required) |
| -d | OpenClaw sessions directory | (required) |

### Examples

```bash
# Basic usage
python3 monitor.py -H 192.168.1.100 -u root -psw your_password -d /root/.openclaw/agents/main/sessions

# With custom SSH port
python3 monitor.py -H 47.80.18.14 -p 2222 -u root -psw your_password -d /root/.openclaw/agents/main/sessions
```

## Session Directory

- Server local: `/root/.openclaw/agents/main/sessions`
- Docker container: `/openclaw/agents/main/sessions`

## Screenshot

![Demo](demo.png)

## Color Legend

- 💭 **Thinking Block** - Purple border, gray italic text
- ⚡ **Command Block** - Cyan border, code syntax highlighting  
- 🤖 **Reply Block** - Green border, Markdown rendering

## License

MIT License

---

# OpenClaw 实时监控工具

一个用于实时监控 OpenClaw 对话会话的终端工具。

## 特性

- 实时追踪：增量读取远程服务器的 OpenClaw .jsonl 会话日志
- 赛博风格：基于 Rich 库打造，区分逻辑思考(紫)、代码指令(青)与系统回复(绿)
- 深度解析：递归剥离嵌套 JSON 列表，确保输出内容纯净
- 极致紧凑：针对大屏幕投屏优化，压缩垂直间距
- 中文增强：完美支持 UTF-8 编码

## 安装

```bash
pip install rich paramiko
```

## 使用方法

```bash
python3 monitor.py -H <服务器IP> -p <SSH端口> -u <用户名> -psw <密码> -d <OpenClaw会话目录>
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -H | 服务器 IP 地址 | (必填) |
| -p | SSH 端口 | 22 |
| -u | SSH 用户名 | root |
| -psw | SSH 密码 | (必填) |
| -d | OpenClaw Session 日志目录 | (必填) |

### 示例

```bash
# 基本用法
python3 monitor.py -H 192.168.1.100 -u root -psw your_password -d /root/.openclaw/agents/main/sessions

# 自定义 SSH 端口
python3 monitor.py -H 47.80.18.14 -p 2222 -u root -psw your_password -d /root/.openclaw/agents/main/sessions
```

## 会话目录

- 服务器本地：`/root/.openclaw/agents/main/sessions`
- Docker 容器内：`/openclaw/agents/main/sessions`

## 界面预览

![Demo](demo.png)

### 颜色说明

- 💭 **逻辑思考块** - 紫色边框，灰色斜体文字
- ⚡ **指令执行块** - 青色边框，代码高亮
- 🤖 **回复消息块** - 绿色边框，Markdown 渲染

## 许可证

MIT License
