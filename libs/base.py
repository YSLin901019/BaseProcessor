import multiprocessing
import traceback
from queue import Queue, Empty
import time

class BaseProcessor(multiprocessing.Process):
    interval_sec = 0.2
    def __init__(self, name:str):
        super().__init__(name=name)
        self.name = name
        self.is_running = False
        self.__stop_event = multiprocessing.Event()
        self.input_queue: Queue = None
        self.output_queue: Queue = None

    def run(self):
        self.on_start()
        self.is_running = True
        try:
            while not self.__stop_event.is_set():
                try:
                    self.loop()
                except Empty:
                    time.sleep(self.interval_sec)
                except Exception as e:
                    raise e
        except KeyboardInterrupt:
            print(f"KeyboardInterrupt caught in {self.name}.")
        except Exception as e:
            traceback.print_exc()
        finally:
            try:
                self.on_stop()
            except Exception as e:
                print(f"Error during {self.name} on_stop: {e}")
            self.is_running = False

    def stop(self):
        self.__stop_event.set()
        self.on_stop()
        self.is_running = False

    def on_start(self):
        raise NotImplementedError

    def on_stop(self):
        raise NotImplementedError
    
    def loop(self):
        raise NotImplementedError
    
    def set_queue(self, input_queue:Queue, output_queue:Queue):
        self.input_queue = input_queue
        self.output_queue = output_queue