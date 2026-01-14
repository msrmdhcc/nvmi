import time
import pynvml

from rich.console import Console, Group
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED

console = Console()

def gradient_color(value, min_val, max_val):
    value = max(min_val, min(value, max_val))
    ratio = (value - min_val) / (max_val - min_val)

    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    return f"rgb({r},{g},0)"

def make_gpu_table():
    table = Table(
        title="[bold rgb(118,185,0)]NVMI[/bold rgb(118,185,0)]  —  NVIDIA GPU Monitor",
        expand=True,
        box=ROUNDED,
        header_style="bold white"
    )

    table.add_column("GPU", justify="left", style="bold rgb(118,185,0)")
    table.add_column("UTIL", justify="right")
    table.add_column("MEM", justify="right")
    table.add_column("TEMP", justify="right")
    table.add_column("POWER", justify="right")

    gpu_count = pynvml.nvmlDeviceGetCount()

    for i in range(gpu_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            util_cell = Text(f"{util:>3}%", style=gradient_color(util, 0, 100))
        except:
            util_cell = Text("N/A")
        try:
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            mem_cell = Text(
                f"{mem.used // 1024**2:>4} / {mem.total // 1024**2} MiB"
            )
        except:
            mem_cell = Text("N/A")
        try:
            temp = pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU
            )
            temp_cell = Text(
                f"{temp:>3}°C",
                style=gradient_color(temp, 30, 100)
            )
        except:
            temp_cell = Text("N/A")

        try:
            power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
            limit = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000
            power_cell = Text(f"{power:>4.1f} / {limit:.0f} W")
        except:
            power_cell = Text("N/A")

        gpu_name = Text(f"{i}  {name}", style="bold rgb(118,185,0)")

        table.add_row(
            gpu_name,
            util_cell,
            mem_cell,
            temp_cell,
            power_cell,
        )

    return table

def make_video_table():
    table = Table(
        title="Video Engine",
        expand=True,
        box=ROUNDED,
        header_style="bold white"
    )

    table.add_column("GPU", justify="left")
    table.add_column("ENCODE", justify="right")
    table.add_column("DECODE", justify="right")

    gpu_count = pynvml.nvmlDeviceGetCount()

    for i in range(gpu_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)

        try:
            enc, _ = pynvml.nvmlDeviceGetEncoderUtilization(handle)
            enc_cell = Text(f"{enc:>3}%", style=gradient_color(enc, 0, 100))
        except:
            enc_cell = Text("N/A")

        try:
            dec, _ = pynvml.nvmlDeviceGetDecoderUtilization(handle)
            dec_cell = Text(f"{dec:>3}%", style=gradient_color(dec, 0, 100))
        except:
            dec_cell = Text("N/A")

        table.add_row(
            Text(f"{i}", style="bold"),
            enc_cell,
            dec_cell
        )

    return table

def main():
    pynvml.nvmlInit()

    try:
        with Live(
            Group(
                make_gpu_table(),
                make_video_table()
            ),
            refresh_per_second=1,
            console=console
        ) as live:
            while True:
                live.update(
                    Group(
                        make_gpu_table(),
                        make_video_table()
                    )
                )
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        pynvml.nvmlShutdown()


if __name__ == "__main__":
    main()
