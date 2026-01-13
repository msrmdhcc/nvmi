import time
import pynvml
from rich.console import Console
from rich.table import Table
from rich.live import Live

pynvml.nvmlInit()

console = Console()
gpu_count = pynvml.nvmlDeviceGetCount()

def make_table():
    table = Table(title="NVMI", expand=True)
    table.add_column("GPU", justify="center")
    table.add_column("Util %", justify="center")
    table.add_column("Memory", justify="center")
    table.add_column("Temp", justify="center")
    table.add_column("Power", justify="center")

    for i in range(gpu_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)

        # Defaults in case NVML fails
        util_str = mem_str = temp_str = power_str = "N/A"

        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            util_str = f"{util.gpu}%"
        except:
            pass

        try:
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            mem_str = f"{mem.used/1024**2:.0f} / {mem.total/1024**2:.0f} MiB"
        except:
            pass

        try:
            temp = pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU
            )
            temp_str = f"{temp} °C"
        except:
            pass

        try:
            power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
            limit = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000
            power_str = f"{power:.1f} / {limit:.0f} W"
        except:
            pass

        table.add_row(
            f"{i} ({name})",
            util_str,
            mem_str,
            temp_str,
            power_str,
        )

    return table

try:
    with Live(make_table(), refresh_per_second=2, console=console) as live:
        while True:
            live.update(make_table())
            time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pynvml.nvmlShutdown()
