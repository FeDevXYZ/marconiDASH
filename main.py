import psutil  # Get system stats
import platform  # Know which system the user is on
import time  # Wait functions
from flask import Flask, render_template, jsonify, request  # Web operations

partitions = []
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
    "disk": getDISK(),
    "net": getNET()
  })
@app.route('/diskdata', methods=["POST"])
def diskdata():
    data = request.get_json(silent=True) or {}
    device = data.get("device")
    if not device:
        return jsonify({"error": "Type in a device."}), 400
    for p in getPartitions():
        if p["device"] == device:
            try:
                d = psutil.disk_usage(p["mount"])
            except PermissionError:
                return jsonify({"error": "Permission denied"}), 403
            return jsonify({
                "free": f"{d.free // 1024**3} GB",
                "used": f"{d.used // 1024**3} GB",
                "total": f"{d.total // 1024**3} GB",
                "percent": f"{d.percent}%"
            })
    return jsonify({"error": "No device found."}), 404

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
      "total": format(ram_tot, "04.2f"),
      "available": format(ram_avail, "04.2f"),
      "percent": format(ram_percent, "04.2f")+"%"
       },
    "swap": {
      "total": format(swap_tot, "04.2f"),
      "used": format(swap_used, "04.2f"),
      "free": format(swap_free, "04.2f"),
      "percent": format(swap_percent, "04.2f")+"%"
    }
  }

def getCPU(): # Prints and returns CPU data
  cpucount = psutil.cpu_count()
  cpucount_notlogical = psutil.cpu_count(logical=False)

  cpupercent = psutil.cpu_percent()
  cpupercent_percore = psutil.cpu_percent(percpu=True)
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
    "frequency": format(cpufreq.current, "04.2f"),
    "loadavg": loadavg,
    "percent": {
      "general": format(cpupercent, "04.2f")+"%",
      "percore": cpupercent_percore
      }
    }

disk_last_writebytes_raw = 0
disk_last_readbytes_raw = 0
def initDISK():
  global disk_last_readbytes_raw, disk_last_writebytes_raw
  diskobj = psutil.disk_io_counters()
  disk_readbytes_raw = diskobj.read_bytes
  disk_writebytes_raw = diskobj.write_bytes
  disk_last_readbytes_raw = disk_readbytes_raw
  disk_last_writebytes_raw = disk_writebytes_raw
def getPartitions():
  unique = {}
  for p in psutil.disk_partitions():
    if p.device not in unique or len(p.mountpoint) < len(unique[p.device]["mount"]):
      unique[p.device] = {
        "device": p.device,
        "mount": p.mountpoint,
        "filesystem": p.fstype,
        "opts": p.opts
      }
  return list(unique.values())
def getDISK():
  global partitions, disk_last_readbytes_raw, disk_last_writebytes_raw
  diskobj = psutil.disk_io_counters()
  disk_readbytes_raw = diskobj.read_bytes
  disk_writebytes_raw = diskobj.write_bytes
  # Calculate difference
  disk_writebytes = format((disk_writebytes_raw-disk_last_writebytes_raw)/1024**2, "04.2f")
  disk_readbytes = format((disk_readbytes_raw-disk_last_readbytes_raw)/1024**2, "04.2f")
  disk_last_readbytes_raw = disk_readbytes_raw
  disk_last_writebytes_raw = disk_writebytes_raw
  # Choose which devices to send
  partitions = getPartitions()
  print(
    partitions, "\n", disk_readbytes, disk_writebytes
  )
  return{
    "partitions": partitions,
    "readbytes": disk_readbytes,
    "writebytes": disk_writebytes
  }
net_last_bytessent = 0
net_last_bytesrec = 0
net_last_errs = 0
def initNET():
  global net_last_bytesrec, net_last_bytessent, net_last_errs
  netobj = psutil.net_io_counters()
  net_last_bytessent = netobj.bytes_sent
  net_last_bytesrec = netobj.bytes_recv
  net_last_errs = netobj.errin + netobj.errout
def getNET():
  global net_last_bytesrec, net_last_bytessent, net_last_errs

  # Network counters fetch and calculations
  netobj = psutil.net_io_counters()     # Note for the next update: pernic=true to return singular connection data
  net_bytessent_raw = netobj.bytes_sent
  net_bytesrec_raw = netobj.bytes_recv
  net_errs_raw = netobj.errin + netobj.errout
    # Calculate difference
  net_bytessent = net_bytessent_raw - net_last_bytessent
  net_bytesrec = net_bytesrec_raw - net_last_bytesrec
  net_errs = net_errs_raw - net_last_errs
  # Save last data for next use
  net_last_bytessent = net_bytessent_raw
  net_last_bytesrec = net_bytesrec_raw
  net_last_errs = net_errs_raw

  # Transform all data in clear units
  net_bytessent = net_bytessent/(1024**2)
  net_bytesrec = net_bytesrec/(1024**2)

  print(
    str(format(net_bytessent, "04.2f"))+" MB ",
    str(format(net_bytesrec, "04.2f"))+" MB ",
    net_errs
  )
  return{
    "bytes_sent": format(net_bytessent, "04.2f"),
    "bytes_rec": format(net_bytesrec, "04.2f"),
    "errors": net_errs
  }


if __name__ == "__main__":
  import ctypes, os

  try:
    is_admin = os.getuid() == 0
  except:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
  if not is_admin:
    print("⚠️ WARNING: You may want to run this script as an administrator or with sudo, as some options could get stopped by a Permission Error.")

 # Initialize data fetch: some functions need to have a blank call for init
  initNET()
  psutil.getloadavg()
  psutil.cpu_percent()

  app.run(host="0.0.0.0", port=5000) # This blocks the app until the server is closed: it's intended behavior for now.

  print("Welcome to marconiDASH. \nPlease select the server you want to connect to:")

  # The real program starts here
  while True:
    answer = input("\nSELECT THE PARAMETERS YOU WANT TO GET:"
                 "\n1. CPU AND SYSTEM"
                 "\n2. RAM"
                 "\n3. DISK"
                 "\n4. NETWORK"
                 "\n")
    if answer == "1":
      getCPU()
    elif answer == "2":
      getRAM()
    elif answer == "3":
      getDISK()
    elif answer == "4":
      getNET()
