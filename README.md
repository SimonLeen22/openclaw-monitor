# OpenClaw Real-time Monitor

一个用于实时监控 OpenClaw 对话会话的终端工具。

## 特性

- 实时追踪：增量读取远程服务器的 OpenClaw .jsonl 会话日志
- 赛博风格：基于 Rich 库打造，区分逻辑思考(紫)、代码指令(青)与系统回复(绿)
- 深度解析：递归剥离嵌套 JSON 列表，确保输出内容纯净
- 极致紧凑：针对大屏幕投屏优化，压缩垂直间距
- 中文增强：完美支持 UTF-8 编码

## 环境依赖

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
# 监控本地或远程 OpenClaw
python3 monitor.py -H 192.168.1.100 -p 22 -u root -psw your_password -d /root/.openclaw/agents/main/sessions
```

## OpenClaw 会话目录

默认目录路径：
- 服务器本地：`/root/.openclaw/agents/main/sessions`
- Docker 容器内：`/openclaw/agents/main/sessions`

## 界面预览

- 💭 逻辑思考块（紫色）
- ⚡ 指令执行块（青色）  
- 🤖 回复消息块（绿色）

## 许可证

MIT License
