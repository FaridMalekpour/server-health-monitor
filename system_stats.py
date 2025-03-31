import psutil
import socket
import platform


def get_system_stats():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu_freq = psutil.cpu_freq()
    swap = psutil.swap_memory()
    net_io = psutil.net_io_counters()

    stats = {
        "cpu": {
            "usage": {"value": psutil.cpu_percent(interval=1), "unit": "%"},
            "cores": {
                "value": psutil.cpu_count(logical=False),
                "unit": "physical cores",
            },
            "threads": {
                "value": psutil.cpu_count(logical=True),
                "unit": "logical cores",
            },
            "frequency": {
                "value": cpu_freq.current if cpu_freq else None,
                "unit": "MHz",
            },
        },
        "memory": {
            "total": {"value": round(memory.total / (1024**3), 2), "unit": "GB"},
            "used": {"value": round(memory.used / (1024**3), 2), "unit": "GB"},
            "available": {
                "value": round(memory.available / (1024**3), 2),
                "unit": "GB",
            },
            "usage": {"value": memory.percent, "unit": "%"},
        },
        "swap": {
            "total": {"value": round(swap.total / (1024**3), 2), "unit": "GB"},
            "used": {"value": round(swap.used / (1024**3), 2), "unit": "GB"},
            "usage": {"value": swap.percent, "unit": "%"},
        },
        "disk": {
            "total": {"value": round(disk.total / (1024**3), 2), "unit": "GB"},
            "used": {"value": round(disk.used / (1024**3), 2), "unit": "GB"},
            "free": {"value": round(disk.free / (1024**3), 2), "unit": "GB"},
            "usage": {"value": disk.percent, "unit": "%"},
        },
        "network": {
            "bytes_sent": {
                "value": round(net_io.bytes_sent / (1024**2), 2),
                "unit": "MB",
            },
            "bytes_received": {
                "value": round(net_io.bytes_recv / (1024**2), 2),
                "unit": "MB",
            },
        },
        "system_info": {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "hostname": platform.node(),
            "architecture": platform.architecture()[0],
            "ip_address": get_ip_address(),
        },
        "uptime": {"value": float(round(psutil.boot_time())), "unit": "timestamp (epoch)"},
    }

    return stats


def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "Unavailable"
    