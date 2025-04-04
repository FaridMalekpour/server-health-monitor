import psutil
import socket
import os
import time
import platform


def get_total_disk_usage():
    """Returns total, used, free space, and usage percentage for all partitions."""
    total_storage, used_storage, free_storage = 0, 0, 0

    for partition in psutil.disk_partitions(all=True):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_storage += usage.total
            used_storage += usage.used
            free_storage += usage.free
        except PermissionError:
            continue  # Skip if access is denied

    usage_percentage = round((used_storage / total_storage) * 100, 2) if total_storage else 0
    return total_storage, used_storage, free_storage, usage_percentage


total_storage, used_storage, free_storage, usage_percentage = get_total_disk_usage()


def get_system_stats():
    memory = psutil.virtual_memory()
    net_io = psutil.net_io_counters()

    stats = {
        "system_info": {
            "ip_address": {"value": get_ip_address(), "unit": ""},
            "os": {"value": platform.system(), "unit": platform.release()},
            "hostname": {"value": platform.node(), "unit": ""},
            "architecture": {"value": platform.architecture()[0], "unit": ""},
        },
        "cpu": {
            "usage": {"value": psutil.cpu_percent(interval=1), "unit": "%"},
            "cores/ threads": {
                "value": f"{psutil.cpu_count(logical=False)}/",
                "unit": psutil.cpu_count(logical=True),
            },
            "frequency": {
                "value": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
                "unit": "MHz",
            },
            "temperature": {
                "value": (
                    psutil.sensors_temperatures()
                    .get("cpu_thermal", [{}])[0]
                    .get("current", "N/A")
                    if hasattr(psutil, "sensors_temperatures")
                    and psutil.sensors_temperatures()
                    else "N/A"
                ),
                "unit": "°C",
            },  # only available on Unix-like systems
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
        "disk": {
            "total": {"value": round(total_storage / (1024**3), 2), "unit": "GB"},
            "used": {"value": round(used_storage / (1024**3), 2), "unit": "GB"},
            "free": {"value": round(free_storage / (1024**3), 2), "unit": "GB"},
            "usage": {"value": usage_percentage, "unit": "%"},
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
        "uptime": {
            "uptime": {
                "value": f"{int((time.time() - psutil.boot_time()) // 3600)}:"
                f"{int((time.time() - psutil.boot_time()) % 3600 // 60):02d}",
                "unit": "H:M",
            }
        },
    }

    return stats


def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "Unavailable"
