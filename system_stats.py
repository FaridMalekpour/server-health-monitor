import psutil
import platform
import socket

def get_system_stats():
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": {
            "total": round(psutil.virtual_memory().total / (1024**3), 2),  # GB
            "used": round(psutil.virtual_memory().used / (1024**3), 2),
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": round(psutil.disk_usage('/').total / (1024**3), 2),  # GB
            "used": round(psutil.disk_usage('/').used / (1024**3), 2),
            "percent": psutil.disk_usage('/').percent
        },
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_received": psutil.net_io_counters().bytes_recv
        },
        "system_info": {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname())
        }
    }
