import psutil
import time
import os
import platform
from datetime import datetime
import argparse
from tabulate import tabulate
import signal


class SystemMonitor:
    def __init__(self, interval=2, show_processes=False, process_count=5, log_file=None):
        self.interval = interval
        self.show_processes = show_processes
        self.process_count = process_count
        self.log_file = log_file
        self.running = True

        # Register signal handler for clean exit
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("\n\nGracefully shutting down...")
        self.running = False

    def get_size(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024

    def get_battery_info(self):
        """Get battery information if available"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                power_plugged = battery.power_plugged
                status = "Charging" if power_plugged else "Discharging"
                return f"{percent}% ({status})"
            return "N/A"
        except:
            return "N/A"

    def get_top_processes(self):
        """Get top processes by memory usage"""
        processes = []
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = process.info
                processes.append((
                    proc_info['pid'],
                    proc_info['name'],
                    process.cpu_percent(),
                    proc_info['memory_percent']
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort by memory usage (can be changed to CPU by changing index to 2)
        processes = sorted(processes, key=lambda x: x[3], reverse=True)
        return processes[:self.process_count]

    def get_network_info(self):
        """Get network information"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': self.get_size(net_io.bytes_sent),
            'bytes_recv': self.get_size(net_io.bytes_recv),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }

    def log_stats(self, stats):
        """Log statistics to file if enabled"""
        if not self.log_file:
            return

        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"{timestamp},{stats['cpu']},{stats['memory_percent']},{stats['disk_percent']}\n")

    def display_system_info(self):
        """Display system information once at startup"""
        print("\n" + "="*50)
        print(f"SYSTEM INFORMATION:")
        print(f"OS: {platform.system()} {platform.version()}")
        print(f"Processor: {platform.processor()}")
        print(f"Machine: {platform.machine()}")
        print(f"Hostname: {platform.node()}")
        print(f"Python Version: {platform.python_version()}")

        # CPU Information
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            freq_current = f"{cpu_freq.current:.2f}MHz"
        else:
            freq_current = "N/A"

        print(
            f"CPU Cores: {psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical")
        print(f"CPU Frequency: {freq_current}")

        # Memory Information
        vm = psutil.virtual_memory()
        print(f"Total Memory: {self.get_size(vm.total)}")

        # Disk Information
        disk = psutil.disk_usage('/')
        print(f"Disk Total: {self.get_size(disk.total)}")
        print("="*50 + "\n")

    def monitor(self):
        """Main monitoring function"""
        if self.log_file:
            # Create log file with header if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    f.write("timestamp,cpu_percent,memory_percent,disk_percent\n")
            print(f"Logging data to: {self.log_file}")

        self.display_system_info()
        print("Monitoring system resources... Press Ctrl+C to stop.\n")

        try:
            while self.running:
                # Get timestamps
                timestamp = datetime.now().strftime("%H:%M:%S")

                # Get CPU stats
                cpu = psutil.cpu_percent(interval=1)

                # Get memory stats
                mem = psutil.virtual_memory()
                mem_percent = mem.percent
                mem_used = self.get_size(mem.used)
                mem_total = self.get_size(mem.total)

                # Get disk stats
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                disk_used = self.get_size(disk.used)
                disk_total = self.get_size(disk.total)

                # Get battery info
                battery = self.get_battery_info()

                # Get network info
                net = self.get_network_info()

                # Get swap memory
                swap = psutil.swap_memory()
                swap_percent = swap.percent
                swap_used = self.get_size(swap.used)
                swap_total = self.get_size(swap.total)

                # Create stats dict for logging
                stats = {
                    'cpu': cpu,
                    'memory_percent': mem_percent,
                    'disk_percent': disk_percent
                }

                # Log stats if enabled
                self.log_stats(stats)

                # Display basic stats
                print(f"[{timestamp}] CPU: {cpu:>5.1f}% | Memory: {mem_percent:>5.1f}% ({mem_used}/{mem_total}) | "
                      f"Disk: {disk_percent:>5.1f}% ({disk_used}/{disk_total}) | Battery: {battery}")
                print(f"         Swap: {swap_percent:>5.1f}% ({swap_used}/{swap_total}) | "
                      f"Network: ↑ {net['bytes_sent']} ↓ {net['bytes_recv']}")

                # Display top processes if enabled
                if self.show_processes:
                    top_processes = self.get_top_processes()
                    if top_processes:
                        process_data = [[pid, name[:20], f"{cpu:.1f}%", f"{mem:.1f}%"]
                                        for pid, name, cpu, mem in top_processes]
                        print("\nTop Processes:")
                        print(tabulate(process_data,
                                       headers=["PID", "Name",
                                                "CPU %", "Memory %"],
                                       tablefmt="simple"))
                    print("")  # Empty line for better readability

                time.sleep(self.interval)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("\nMonitoring stopped.")


def main():
    parser = argparse.ArgumentParser(description="System Resource Monitor")
    parser.add_argument("-i", "--interval", type=float, default=2.0,
                        help="Update interval in seconds (default: 2.0)")
    parser.add_argument("-p", "--processes", action="store_true",
                        help="Show top processes by memory usage")
    parser.add_argument("-n", "--num-processes", type=int, default=5,
                        help="Number of top processes to show (default: 5)")
    parser.add_argument("-l", "--log", type=str,
                        help="Log data to specified CSV file")

    args = parser.parse_args()

    monitor = SystemMonitor(
        interval=args.interval,
        show_processes=args.processes,
        process_count=args.num_processes,
        log_file=args.log
    )

    monitor.monitor()


if __name__ == "__main__":
    main()
