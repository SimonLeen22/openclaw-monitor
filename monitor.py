"""
OpenClaw Real-time Monitor v1.2 (Open Source Edition)
=====================================================

A real-time terminal monitor for OpenClaw session logs.
"""

import paramiko
import time
import json
import os
import re
import argparse
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.syntax import Syntax
    from rich import box
    c = Console(highlight=False)
except ImportError:
    print("❌ Error: Missing dependencies. Run: pip install rich paramiko")
    exit(1)

def get_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="OpenClaw Real-time Monitor")
    parser.add_argument("-H", "--host", required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-u", "--user", default="root", help="SSH username (default: root)")
    parser.add_argument("-psw", "--password", required=True, help="SSH password")
    parser.add_argument("-d", "--dir", required=True, help="OpenClaw sessions directory")
    return parser.parse_args()

class CyberWatcher:
    def __init__(self, args):
        self.args = args
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.f_path = None
        self.offset = 0

    def connect(self):
        """Establish SSH connection"""
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
            c.print(f"[bold red]❌ SSH connection failed:[/] {e}")
            return False

    def safe_text(self, data):
        """Text cleaning engine"""
        if not data: return ""
        s = str(data).replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        return s.strip()

    def render_element(self, item):
        """Render engine for JSON elements"""
        if isinstance(item, list):
            for i in item: self.render_element(i)
            return
        if not isinstance(item, dict):
            return

        ts = datetime.now().strftime('%H:%M:%S')
        
        # Thinking block
        think = item.get('thinking') or item.get('thought')
        if think:
            c.print(Panel(
                Text(self.safe_text(think), style="light_slate_grey italic"),
                title=f"[steel_blue]💭 LOGIC {ts}[/]", 
                border_style="blue_violet", padding=(0, 1), expand=True, box=box.ROUNDED
            ))

        # Command/Exec block
        args = item.get('arguments', {}) if isinstance(item.get('arguments'), dict) else item
        cmd = args.get('command') or args.get('content') or item.get('command')
        
        if cmd and not think:
            name = item.get('name') or "EXEC"
            syntax_cmd = Syntax(self.safe_text(cmd), "bash", theme="monokai", background_color="default")
            c.print(Panel(
                syntax_cmd, 
                title=f"[bold cyan]⚡ {str(name).upper()}[/]", 
                border_style="cyan", padding=(0, 1), expand=True, box=box.SQUARE
            ))

        # Message block
        txt = item.get('text') or item.get('content')
        if txt and not think and not cmd:
            clean_txt = self.safe_text(txt)
            if clean_txt.startswith('[') or clean_txt.startswith('{'):
                try:
                    self.render_element(json.loads(clean_txt))
                    return
                except: pass
            
            c.print(Panel(
                Markdown(clean_txt), 
                title=f"[bold spring_green3]🤖 REPLY {ts}[/]", 
                border_style="spring_green3", padding=(0, 1), expand=True, box=box.ROUNDED
            ))

    def run(self):
        """Main monitoring loop"""
        if not self.connect(): return
        c.clear()
        c.rule(f"[bold sky_blue1]OPENCLAW MONITOR: {self.args.host}[/bold sky_blue1]", style="blue_violet")

        while True:
            try:
                _, out, _ = self.ssh.exec_command(f"ls -t {self.args.dir}/*.jsonl 2>/dev/null | head -n 1")
                new_file = out.read().decode().strip()
                
                if not new_file:
                    time.sleep(2); continue
                
                if new_file != self.f_path:
                    self.f_path = new_file
                    _, sz, _ = self.ssh.exec_command(f"stat -c %s {new_file}")
                    self.offset = max(0, int(sz.read().decode().strip() or 0) - 40000)
                    c.print(f"[dim sky_blue1]🛰️  Connected: {os.path.basename(new_file)}[/]")

                _, out, _ = self.ssh.exec_command(f"tail -c +{self.offset + 1} {self.f_path}")
                raw_data = out.read().decode('utf-8', 'replace')
                
                if raw_data:
                    for line in raw_data.strip().split('\n'):
                        if not line.strip() or "INFO" in line: continue
                        try:
                            data = json.loads(line)
                            msg_content = data.get('message', data)
                            self.render_element(msg_content)
                        except:
                            pass
                    self.offset += len(raw_data.encode('utf-8'))
                
                time.sleep(1)
            except Exception:
                time.sleep(5)
                self.connect()

if __name__ == "__main__":
    args = get_args()
    try:
        CyberWatcher(args).run()
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped.")
