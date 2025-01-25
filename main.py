import os
import time
import json

def is_online():
    response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1" if os.name != 'nt' else "ping -n 1 8.8.8.8 > nul")
    return response == 0

def log_downtime(downtime_log, downtime_count, start_time, end_time):
    downtime_duration = round(end_time - start_time, 2)
    priority = "LOW"
    if downtime_duration < 120:
        priority = "LOW"
    elif downtime_duration < 360:
        priority = "MEDIUM"
    elif downtime_duration < 600:
        priority = "HIGH"
    elif downtime_duration < 6000:
        priority = "SEVERE"
    else:
        priority = "BLACKOUT"

    entry = {
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
        "Downtime #": downtime_count,
        "Length": downtime_duration,
        "Priority": priority
    }

    if os.path.exists("downtime_log.json"):
        with open("downtime_log.json", "r") as file:
            log = json.load(file)
    else:
        log = []

    log.append(entry)

    with open("downtime_log.json", "w") as file:
        json.dump(log, file, indent=4)

def main():
    print("Interneat by coolboy67YT, The Turtle Developer\n")
    print("Use Ctrl+C to quit")
    online = is_online()
    if online:
        print("[INFO] Initial status: ONLINE")
    else:
        print("[INFO] Initial status: OFFLINE")

    last_status = online
    downtime_start = None
    downtime_count = 0

    try:
        while True:
            online = is_online()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if online:
                if not last_status:
                    downtime_end = time.time()
                    downtime_count += 1
                    log_downtime("downtime_log.json", downtime_count, downtime_start, downtime_end)
                    downtime_duration = round(downtime_end - downtime_start, 2)
                    print(f"[{current_time}] ONLINE. Downtime was {downtime_duration} seconds.")
                else:
                    print(f"[{current_time}] ONLINE.")
                last_status = True
            else:
                if last_status:
                    downtime_start = time.time()
                    print(f"[{current_time}] OFFLINE. Downtime started.")
                else:
                    print(f"[{current_time}] OFFLINE.")
                last_status = False

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Program terminated by user.")

if __name__ == "__main__":
    main()
