"""
OpenClaw Real-time Monitor v1.2 (Open Source Edition)
=====================================================

【特性描述】:
1. 实时追踪: 自动识别并增量读取远程服务器最新的 OpenClaw .jsonl 会话日志。
2. 赛博风格: 基于 Rich 库打造，区分逻辑思考(紫)、代码指令(青)与系统回复(绿)。
3. 深度解析: 递归剥离嵌套 JSON 列表，确保输出内容纯净、无冗余括号。
4. 极致紧凑: 针对大屏幕投屏优化，压缩垂直间距，提升信息展示密度。
5. 中文增强: 完美支持 UTF-8 编码，彻底修复中文转义及乱码问题。
6. 时间戳显示: 显示每条消息的发送时间

【环境依赖】:
pip install rich paramiko

【使用示例】:
python3 monitor.py -H 47.80.18.14 -p 2222 -u root -psw your_password -d /remote/path/to/sessions
"""

import paramiko
import time
import json
import os
import re
import argparse
from datetime import datetime, timezone, timedelta

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.syntax import Syntax
    from rich import box
    # 初始化 Console，highlight=False 防止 Rich 自动对内容进行不必要的着色
    c = Console(highlight=False)
except ImportError:
    print("❌ 错误: 缺少必要依赖。请执行: pip install rich paramiko")
    exit(1)

def get_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="OpenClaw 实时大屏监控工具 - 开源版")
    # 使用 -H 代替 -h 以避开系统预留的 --help 冲突
    parser.add_argument("-H", "--host", required=True, help="服务器 IP 地址")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH 端口 (默认: 22)")
    parser.add_argument("-u", "--user", default="root", help="SSH 用户名 (默认: root)")
    parser.add_argument("-psw", "--password", required=True, help="SSH 密码")
    parser.add_argument("-d", "--dir", required=True, help="远程 OpenClaw Session 日志存放目录")
    return parser.parse_args()

class CyberWatcher:
    def __init__(self, args):
        self.args = args
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.f_path = None  # 当前追踪的文件路径
        self.offset = 0     # 文件读取偏移量

    def connect(self):
        """建立 SSH 连接"""
        try:
            self.ssh.connect(
                self.args.host, 
                port=self.args.port, 
                username=self.args.user, 
                password=self.args.password, 
                timeout=10
            )
            return True
        except Exception as e:
            c.print(f"[bold red]❌ SSH 连接失败:[/] {e}")
            return False

    def safe_text(self, data):
        """文本清洗引擎：处理转义字符，保留中文，确保排版整洁"""
        if not data: return ""
        # 针对字符串，处理常见的换行和引号转义
        s = str(data).replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        return s.strip()

    def get_msg_timestamp(self, data):
        """从消息数据中提取时间戳（北京时间）"""
        # 优先使用 message 中的 timestamp
        msg = data.get('message', {})
        ts = msg.get('timestamp') if isinstance(msg, dict) else None
        if ts:
            try:
                # 处理 ISO 格式时间戳
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                # 转换为北京时间
                dt = dt.astimezone(BEIJING_TZ)
                return dt.strftime('%H:%M:%S')
            except:
                pass
        # 尝试从顶层 timestamp 字段获取
        ts = data.get('timestamp')
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                dt = dt.astimezone(BEIJING_TZ)
                return dt.strftime('%H:%M:%S')
            except:
                pass
        # 返回当前北京时间
        return datetime.now(BEIJING_TZ).strftime('%H:%M:%S')

    def render_element(self, item, timestamp=None):
        """渲染引擎：将解析后的 JSON 元素转化为 UI 面板"""
        # 如果是列表，递归拆解
        if isinstance(item, list):
            for i in item: self.render_element(i, timestamp)
            return
        if not isinstance(item, dict):
            return

        # 使用传入的时间戳或当前时间
        ts = timestamp or datetime.now().strftime('%H:%M:%S')
        
        # 1. 逻辑思考块 (THINKING)
        think = item.get('thinking') or item.get('thought')
        if think:
            c.print(Panel(
                Text(self.safe_text(think), style="light_slate_grey italic"),
                title=f"[steel_blue]💭 LOGIC {ts}[/]", 
                border_style="blue_violet", padding=(0, 1), expand=True, box=box.ROUNDED
            ))

        # 2. 指令执行块 (EXEC/ACTION)
        # 尝试从不同层级抓取指令内容
        args = item.get('arguments', {}) if isinstance(item.get('arguments'), dict) else item
        cmd = args.get('command') or args.get('content') or item.get('command')
        
        if cmd and not think:
            name = item.get('name') or "EXEC"
            # 使用 Syntax 模块进行代码高亮渲染
            syntax_cmd = Syntax(self.safe_text(cmd), "bash", theme="monokai", background_color="default")
            c.print(Panel(
                syntax_cmd, 
                title=f"[bold cyan]⚡ {str(name).upper()} {ts}[/]", 
                border_style="cyan", padding=(0, 1), expand=True, box=box.SQUARE
            ))

        # 3. 回复消息块 (MESSAGE)
        txt = item.get('text') or item.get('content')
        if txt and not think and not cmd:
            clean_txt = self.safe_text(txt)
            # 自动识别并解析二次包装的 JSON 字符串
            if clean_txt.startswith('[') or clean_txt.startswith('{'):
                try:
                    self.render_element(json.loads(clean_txt), timestamp)
                    return
                except: pass
            
            c.print(Panel(
                Markdown(clean_txt), 
                title=f"[bold spring_green3]🤖 REPLY {ts}[/]", 
                border_style="spring_green3", padding=(0, 1), expand=True, box=box.ROUNDED
            ))

    def run(self):
        """主监控循环"""
        if not self.connect(): return
        c.clear()
        c.rule(f"[bold sky_blue1]OPENCLAW MONITOR: {self.args.host}[/bold sky_blue1]", style="blue_violet")

        while True:
            try:
                # 获取远程目录下最新的 .jsonl 日志文件
                _, out, _ = self.ssh.exec_command(f"ls -t {self.args.dir}/*.jsonl 2>/dev/null | head -n 1")
                new_file = out.read().decode().strip()
                
                if not new_file:
                    time.sleep(2); continue
                
                # 会话切换处理
                if new_file != self.f_path:
                    self.f_path = new_file
                    _, sz, _ = self.ssh.exec_command(f"stat -c %s {new_file}")
                    # 初次读取回溯约 40KB 内容，确保启动不黑屏
                    self.offset = max(0, int(sz.read().decode().strip() or 0) - 40000)
                    c.print(f"[dim sky_blue1]🛰️  已成功接入远程会话: {os.path.basename(new_file)}[/]")

                # 执行增量读取
                _, out, _ = self.ssh.exec_command(f"tail -c +{self.offset + 1} {self.f_path}")
                raw_data = out.read().decode('utf-8', 'replace')
                
                if raw_data:
                    for line in raw_data.strip().split('\n'):
                        if not line.strip() or "INFO" in line: continue
                        try:
                            # 尝试解析标准 JSON 记录
                            data = json.loads(line)
                            # 提取时间戳
                            timestamp = self.get_msg_timestamp(data)
                            # 提取核心 message 字段进行渲染
                            msg_content = data.get('message', data)
                            self.render_element(msg_content, timestamp)
                        except:
                            pass
                    # 更新偏移量，避免重复读取
                    self.offset += len(raw_data.encode('utf-8'))
                
                time.sleep(1) # 轮询频率
            except Exception:
                # 网络抖动重连逻辑
                time.sleep(5)
                self.connect()

if __name__ == "__main__":
    args = get_args()
    try:
        CyberWatcher(args).run()
    except KeyboardInterrupt:
        print("\n👋 监控系统已下线。")
