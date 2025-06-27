# DDoS Tools
Installation on Linux:

```Update system packages
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3 python3-pip git

git clone https://github.com/yourusername/NeuroHexa-DDoS-Tool.git
cd NeuroHexa-DDoS-Tool

pip3 install -r requirements.txt

pip3 install colorama aiohttp


chmod +x advanced_ddos.py


sudo ./advanced_ddos.py
```
Alternative Installation (Docker):
```
sudo apt install -y docker.io

sudo docker build -t neurohexa-ddos .

sudo docker run -it --rm neurohexa-ddos
```
System Requirements:
Linux (Kali/Ubuntu/Debian recommended)

Python 3.8+

Root privileges (recommended)

Minimum 2GB RAM

Stable internet connection

Usage Instructions:
Start the tool:
```
sudo ./advanced_ddos.py
```
Follow the prompts:

Accept the disclaimer

Enter target URL (e.g., http://example.com)

Set number of threads (100-1000 recommended)

Optional: Set time limit

Confirm attack

During attack:

Real-time stats will be displayed

Press Ctrl+C to stop

After attack:

Detailed summary will be shown

Logs saved in attack_logs/ directory

Recommended Settings:
For testing: 50-100 threads

For stress testing: 300-500 threads

Maximum duration: 300 seconds (5 minutes)

Notes:
Running as root (sudo) provides better network performance

Monitor your system resources during attack

For educational purposes only

Check your local laws before use

Uninstallation:
```
# Remove the tool completely
cd ..
sudo rm -rf NeuroHexa-DDoS-Tool
pip3 uninstall colorama aiohttp
```
