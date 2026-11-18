import psutil  # Get system stats
import platform  # Know which system the user is on
import time  # Wait functions
from flask import Flask, render_template  # Web operations

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

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

  return ram_tot, ram_avail, ram_percent, swap_tot, swap_used, swap_free, swap_percent

def getCPU(): # Prints and returns CPU data
  cpucount = psutil.cpu_count()
  cpucount_notlogical = psutil.cpu_count(logical=False)

  cpupercent = psutil.cpu_percent(interval=1)
  cpufreq = psutil.cpu_freq()
  if platform.system().lower() == "windows" or platform.system().lower() == "win32":  # PSUTIL has an issue where getloadavg returns an unusable namedtuple (0,0,0)
    psutil.getloadavg()  # for the 5 seconds that follow the first getloadavg() call on Windows.
    print("Calculating system load...")  # This will probably make the wait feel less like a wait.
    time.sleep(7)
    loadavg = psutil.getloadavg()
  else:
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

  return cpucount, cpucount_notlogical, cpufreq, cpupercent, loadavg

if __name__ == '__main__':
  app.run() # This blocks the app until the server is closed: it's intended behavior for now.

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