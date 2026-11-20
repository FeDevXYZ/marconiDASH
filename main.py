import psutil  # Get system stats
import platform  # Know which system the user is on
import time  # Wait functions
from flask import Flask, render_template, jsonify  # Web operations

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/data')
def returnData():
  return jsonify({
    "system": platform.system(),
    "memory": getRAM(),
    "cpu": getCPU(),
    "disk": getDISK()
  })

def getRAM(): # Prints and returns RAM data
  ram_obj = psutil.virtual_memory()
  ram_tot = ram_obj.total / (1024 ** 3)  # In GB
  ram_avail = ram_obj.available / (1024 ** 3)  # In GB
  ram_percent = ram_obj.percent

  print("RAM Data:")
  print(f"Total: {format(ram_tot, "04.2f")} GB")
  print(f"Available: {format(ram_avail, "04.2f")} GB")
  print(f"Usage percent: {format(ram_percent, "04.2f")}%")

  print("")

  swap_obj = psutil.swap_memory()
  swap_tot = swap_obj.total / (1024 ** 3)  # In GB
  swap_used = swap_obj.used / (1024 ** 3)  # In GB
  swap_free = swap_obj.free / (1024 ** 3)  # In GB
  swap_percent = swap_obj.percent

  print("SWAP Data:")
  print(f"Total: {format(swap_tot, "04.2f")} GB")
  print(f"Used: {format(swap_used, "04.2f")} GB | Free: {format(swap_free, "04.2f")} GB")
  print(f"Usage percent: {swap_percent}%")

  # return ram_tot, ram_avail, ram_percent, swap_tot, swap_used, swap_free, swap_percent
  return {
    "ram": {
      "total": ram_tot,
      "available": ram_avail,
      "percent": ram_percent
       },
    "swap": {
      "total": swap_tot,
      "used": swap_used,
      "free": swap_free,
      "percent": swap_percent
    }
  }

def getCPU(): # Prints and returns CPU data
  cpucount = psutil.cpu_count()
  cpucount_notlogical = psutil.cpu_count(logical=False)

  cpupercent = psutil.cpu_percent()
  cpufreq = psutil.cpu_freq()
  loadavg = psutil.getloadavg()
  print("CPU AND SYSTEM Stats:")

  print("Sys load average:")

  print("| 1 min |      | 5 min |      | 15min |")
  print(
    f"| {str(format(loadavg[0], "05.2f")).center(6)}|      | {str(format(loadavg[1], "05.2f")).center(6)}|      | {str(format(loadavg[2], "05.2f")).center(6)}|")
  print(f"Usage: {cpupercent}%")
  print(f"{format(cpufreq.current, "04.2f")} Mhz")

  print("")

  print("Info:")
  print(f"Count: {cpucount}     of which not logical: {cpucount_notlogical}")

  # return cpucount, cpucount_notlogical, cpufreq, cpupercent, loadavg
  return {
    "count": cpucount,
    "notlogical": cpucount_notlogical,
    "percent": cpupercent,
    "frequency": cpufreq.current,
    "loadavg": loadavg
  }

def getDISK():
  partitions = []
  partitionsobj = psutil.disk_partitions()
  for p in partitionsobj:
    partition_device = p.device
    partition_mount = p.mountpoint
    partition_fs = p.fstype
    partition_opts = p.opts
    print(f"{partition_device}, {partition_mount}, {partition_fs}, {partition_opts}")
    partitions.append({"device": partition_device, "mount": partition_mount, "filesystem": partition_fs, "opts": partition_opts})
  return partitions
if __name__ == "__main__":
  psutil.getloadavg()
  psutil.cpu_percent()

  app.run(host="0.0.0.0", port=5000) # This blocks the app until the server is closed: it's intended behavior for now.

  print("Welcome to marconiDASH. \nPlease select the server you want to connect to:")

  # The real program starts here
  while True:
    answer = input("\nSELECT THE PARAMETERS YOU WANT TO GET:"
                 "\n1. CPU AND SYSTEM"
                 "\n2. RAM"
                 "\n3. DISK\n")
    if answer == "1":
      getCPU()
    elif answer == "2":
      getRAM()
    elif answer == "3":
      getDISK()