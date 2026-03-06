# OpenClaw Real-time Monitor

一个用于实时监控 OpenClaw 对话会话的终端工具。

---

## English Description

A real-time terminal monitor for OpenClaw AI agent session logs. Track your AI assistant's conversations across multiple channels in a cyberpunk-style interface.

## Features | 特性

- **Real-time Tracking** - Incrementally reads remote OpenClaw .jsonl session logs | 实时追踪：增量读取远程服务器的 OpenClaw .jsonl 会话日志
- **Cyberpunk Style** - Color-coded blocks for thinking (purple), commands (cyan), and responses (green) | 赛博风格：基于 Rich 库打造，区分逻辑思考(紫)、代码指令(青)与系统回复(绿)
- **Deep Parsing** - Recursively unwraps nested JSON for clean output | 深度解析：递归剥离嵌套 JSON 列表，确保输出内容纯净
- **Compact Display** - Optimized for large screen mirroring | 极致紧凑：针对大屏幕投屏优化，压缩垂直间距
- **Chinese Support** - Full UTF-8 encoding support | 中文增强：完美支持 UTF-8 编码

## Installation | 安装

```bash
pip install rich paramiko
```

## Usage | 使用方法

```bash
python3 monitor.py -H <server_ip> -p <ssh_port> -u <username> -psw <password> -d <openclaw_sessions_dir>
```

### Parameters | 参数说明

| Parameter | Description | 说明 | Default |
|-----------|-------------|------|---------|
| -H | Server IP address | 服务器 IP 地址 | (required) |
| -p | SSH port | SSH 端口 | 22 |
| -u | SSH username | SSH 用户名 | root |
| -psw | SSH password | SSH 密码 | (required) |
| -d | OpenClaw sessions directory | OpenClaw 会话目录 | (required) |

### Examples | 示例

```bash
# Monitor local or remote OpenClaw
python3 monitor.py -H 192.168.1.100 -p 22 -u root -psw your_password -d /root/.openclaw/agents/main/sessions

# With custom SSH port (e.g., 2222)
python3 monitor.py -H 47.80.18.14 -p 2222 -u root -psw your_password -d /root/.openclaw/agents/main/sessions
```

## Session Directory | OpenClaw 会话目录

Default paths:
- Server local: `/root/.openclaw/agents/main/sessions`
- Docker container: `/openclaw/agents/main/sessions`

## Screenshot | 界面预览

![Demo](demo.png)

### Color Legend | 颜色说明

- 💭 **Thinking Block** - Purple border, gray italic text | 逻辑思考块 - 紫色边框，灰色斜体文字
- ⚡ **Command Block** - Cyan border, code syntax highlighting | 指令执行块 - 青色边框，代码高亮
- 🤖 **Reply Block** - Green border, Markdown rendering | 回复消息块 - 绿色边框，Markdown 渲染

## License | 许可证

MIT License
