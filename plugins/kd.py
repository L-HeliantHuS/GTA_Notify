from threading import Thread
import psutil
import time

class KD(Thread):
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
    
    def run(self):
        import config
        p = None
        process_name = config.get_config("settings", "PROCESS_NAME")
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == process_name:
                pid = process.info['pid']
                p = psutil.Process(pid)
        
        print(f"暂停进程 {process_name} (PID: {pid})")
        p.suspend()
        time.sleep(config.get_config("settings", "SUSPEND_TIME"))
        p.resume()
