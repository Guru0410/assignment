import csv
import os
import sys
import time

class Watcher(object):
    running = True
    refresh_delay_secs = 1
    ts_list = []
    watch_file = None
    input_file = None
    watch_file_size = 0
    input_file_size = 0
    total_size = 0
    # Constructor
    def __init__(self, watch_file, input_file, *args, **kwargs):
        self.filename = watch_file
        self.watch_file = watch_file
        self.input_file = input_file
        # self.call_func_on_change = call_func_on_change
        self.call_func_on_change = self.file_change_observer
        self._cached_stamp = os.stat(self.filename).st_mtime
        self.args = args
        self.kwargs = kwargs
        self.watch_file_size = os.stat(watch_file).st_size
        self.input_file_size = os.stat(input_file).st_size
        self.total_size = self.watch_file_size + self.input_file_size
        self._setup_csv()

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            self.ts_list.append(os.stat(self.filename).st_mtime)
            print('File changed')
            self.ts_list.append(time.time())
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop
    def watch(self):
        while self.running:
            try:
                # Look for changes
                time.sleep(self.refresh_delay_secs/1000)
                self.look()
            except KeyboardInterrupt:
                print('\nDone')
                break
            except FileNotFoundError:
                # Action on file not found
                pass
            except:
                print('Unhandled error: %s' % sys.exc_info()[0])

    def _cleanup(self):
        self.watch_file_size = os.stat(self.filename).st_size
        self.total_size = self.watch_file_size + self.input_file_size
        self.ts_list = []

    def _calculate_througput(self, total_time_ms):
        throughput = round(self.input_file_size/total_time_ms)
        print("Throughput: " + str(round(throughput)) + " bytes/s")
        data = [str(self.input_file_size),str(total_time_ms), str(throughput)]
        self._write_csv(data)

    def _setup_csv(self):
        header = ['Input file size (Bytes)','Latency', 'Throughput (Bytes/sec)']
        f = open(output_file, 'w')
        writer = csv.writer(f)
        writer.writerow(header)

    def _write_csv(self, data):
        f = open(output_file, 'a')
        writer = csv.writer(f)
        writer.writerow(data)

    def _success_actions(self):
        self.ts_list.append(time.time())
        total_time = float(self.ts_list[-1]) - float(self.ts_list[0])
        total_time_ms = round(total_time*1000)
        print("Total Elapsed time: " + str(total_time_ms) + " ms")
        self._cleanup()
        self._calculate_througput(total_time_ms)

    def _compare_last_lines(self):
        with open(watch_file,"rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line_watch_file = f.readline().decode()
        with open(input_file, "rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line_input_file = f.readline().decode()

        if last_line_watch_file == last_line_input_file:
            self._success_actions()



    def file_change_observer(self):
        current_size = os.stat(self.watch_file).st_size
        last_entry_diff = float(self.ts_list[-1])  - float(self.ts_list[-2])
        print("Last Entry Diff: " + str(last_entry_diff))

        if int(self.total_size) == int(current_size):
            print("Size Match")
            self._success_actions()

        else:
            current_size = os.stat(self.watch_file).st_size
            print("Current Size: " + str(current_size))
            print("File Update")
            self._compare_last_lines()

watch_file = '/usr/src/app/events.log'
output_file = '/usr/src/app/throughput.csv'
init_watch_file_size = os.stat(watch_file).st_size
input_file = '/usr/src/app/agent/inputs/large_1M_events.log'

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, input_file)  # also call custom action function
watcher.watch()  # start the watch going
