from threading import Thread
import time


class PollingThread(Thread):
    def __init__(self, a_proxy, daemon_value):
        Thread.__init__(self, daemon=daemon_value)
        self.proxy = a_proxy

    def run(self):
        while True:
            status = self.proxy.get_status()
            if status == 2:  #   connected without match
                self.proxy.start_status()
            elif status == 3:  #   waiting remote move
                self.proxy.match_status()
            time.sleep(1)  # Sleep for 1 second
