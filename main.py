import psutil  # Get system stats
import platform  # Know which system the user is on
import time  # Wait functions

if __name__ == '__main__':
  print("Welcome to marconiDASH. \nPlease select the server you want to connect to:")

  # The real program starts here
  while True:
    answer = input("\nSELECT THE PARAMETERS YOU WANT TO GET:"
                 "\n1. CPU AND SYSTEM"
                 "\n2. RAM"
                 "\n3. DISK\n")
    if answer == "1":
      cpucount = psutil.cpu_count()
      cpucount_notlogical = psutil.cpu_count(logical=False)

      cpupercent = psutil.cpu_percent(interval=1)
      cpufreq = psutil.cpu_freq()
      if platform.system() == "Windows":      # PSUTIL has an issue where getloadavg returns an unusable namedtuple (0,0,0)
        psutil.getloadavg()                   # for the 5 seconds that follow the first getloadavg() call.
        print("Calculating system load...")   # This will probably make the wait feel less like a wait.
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
    elif answer == "2":
      ram_obj = psutil.virtual_memory()
      ram_tot = ram_obj.total/(1024**3) # In GB
      ram_avail = ram_obj.available/(1024**3) # In GB
      ram_percent = ram_obj.percent

      print("RAM Data:")
      print(f"Total: {format(ram_tot, "04.2f")} GB")
      print(f"Available: {format(ram_avail, "04.2f")} GB")
      print(f"Usage percent: {format(ram_percent, "04.2f")}%")

      print("")

      swap_obj = psutil.swap_memory()
      swap_tot = swap_obj.total/(1024**3) # In GB
      swap_used = swap_obj.used/(1024**3) # In GB
      swap_free = swap_obj.free/(1024**3) # In GB
      swap_percent = swap_obj.percent

      print("SWAP Data:")
      print(f"Total: {format(swap_tot, "04.2f")} GB")
      print(f"Used: {format(swap_used, "04.2f")} GB | Free: {format(swap_free, "04.2f")} GB")
      print(f"Usage percent: {swap_percent}%")