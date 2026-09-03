#!/usr/bin/env python3
"""
Zero-Setup Port Forwarding & Tunnel Manager for Remote Access.

Supports:
1. SSH localhost.run (Zero download, zero signup, instant HTTPS URL)
2. Pinggy (SSH port 443, instant HTTPS URL)
"""

import os
import sys
import re
import time
import subprocess
from typing import Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ACTIVE_TUNNELS = {}

def start_ssh_tunnel(port: int = 3000, timeout: int = 20) -> Tuple[Optional[str], Optional[subprocess.Popen]]:
    """Start an SSH tunnel via localhost.run to expose local port to public internet."""
    cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", f"80:localhost:{port}",
        "nokey@localhost.run"
    ]
    
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        public_url = None
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                time.sleep(0.3)
                continue
            
            match = re.search(r'(https://[a-zA-Z0-9\.\-]+\.lhr\.life)', line)
            if match:
                public_url = match.group(1)
                break
                
            match_generic = re.search(r'(https://[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,})', line)
            if match_generic and "localhost.run" not in match_generic.group(1):
                public_url = match_generic.group(1)
                break

        if public_url:
            ACTIVE_TUNNELS[port] = proc
            return public_url, proc
        else:
            proc.terminate()
            return None, None
    except Exception as e:
        print(f"Error starting SSH tunnel: {e}", file=sys.stderr)
        return None, None

def start_pinggy_tunnel(port: int = 3000, timeout: int = 20) -> Tuple[Optional[str], Optional[subprocess.Popen]]:
    """Start an SSH tunnel via Pinggy."""
    cmd = [
        "ssh",
        "-p", "443",
        "-R0:localhost:" + str(port),
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "a.pinggy.io"
    ]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        public_url = None
        start_time = time.time()
        while time.time() - start_time < timeout:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                time.sleep(0.3)
                continue
            match = re.search(r'(https://[a-zA-Z0-9\-]+\.a\.pinggy\.link)', line)
            if match:
                public_url = match.group(1)
                break
        if public_url:
            ACTIVE_TUNNELS[port] = proc
            return public_url, proc
        else:
            proc.terminate()
            return None, None
    except Exception as e:
        print(f"Error starting Pinggy tunnel: {e}", file=sys.stderr)
        return None, None

def get_or_create_tunnel(port: int = 3000) -> Optional[str]:
    """Try multiple zero-auth providers to get a live public HTTPS URL."""
    url, _ = start_ssh_tunnel(port)
    if url:
        return url
    url, _ = start_pinggy_tunnel(port)
    return url

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    print(f"Starting public tunnel for localhost:{port}...")
    url = get_or_create_tunnel(port)
    if url:
        print(f"[SUCCESS] Tunnel Live: {url}")
    else:
        print("[ERROR] Failed to establish public tunnel.")
