
import sys
import os.path
import win32gui
import win32process
import win32api
import win32con
import tkinter as tk

from Activity import get_activity


############################################################################
class ActivityLogger:
    def __init__(self):
        self.file = open('activity.txt', mode='a', buffering=1, encoding='utf-8')

    def add_new_activity(self, app_name, extra_info, start, end):
        duration = end - start
        s = '{0:.1f}\t{1}\t{2}\t{3}\t{4}\n'.format(duration.total_seconds() / 60,
                                                   start.strftime('%Y-%m-%d %H:%M'),
                                                   end.strftime('%Y-%m-%d %H:%M'),
                                                   app_name, extra_info)
        self.file.write(s)


############################################################################
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.activityLogger = ActivityLogger()
        exe_name, caption = get_current_process_name()
        self.currentActivity = get_activity(exe_name, caption)
        self.update_clock()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.withdraw()
        print('Tracker is running. Press Ctrl-C to stop.')
        self.root.mainloop()

    def update_clock(self):
        self.one_cycle()
        self.root.after(10000, self.update_clock)

    def one_cycle(self):
        idle = not App.is_user_active()
        exe_name, caption = get_current_process_name()
        if exe_name and caption:
            self.currentActivity = self.currentActivity.on_timer(idle, exe_name,
                                                                 caption, self.activityLogger)
        else:
            print('Failed to get wnd')

    def on_close(self):
        self.currentActivity.close(self.activityLogger)
        self.root.destroy()

    @staticmethod
    def is_user_active():
        idle_time = win32api.GetTickCount() - win32api.GetLastInputInfo()
        return (idle_time / 1000) < 60


############################################################################
def get_current_process_name():
    pshandle = None
    try:
        is_vista_and_later = sys.getwindowsversion().major >= 6
        cur_wnd = win32gui.GetForegroundWindow()
        processid = win32process.GetWindowThreadProcessId(cur_wnd)
        pshandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                                        False, processid[1])
        if is_vista_and_later:
            import ctypes
            import ctypes.wintypes as wintypes
            max_path = 260
            application_path = ctypes.create_unicode_buffer(max_path)
            length = wintypes.DWORD(max_path)
            handle = wintypes.HANDLE(int(pshandle))
            kernel32 = ctypes.windll.kernel32
            kernel32.QueryFullProcessImageNameW(handle, 0, application_path, ctypes.byref(length))
            exe_name = application_path.value
        else:
            exe_name = win32process.GetModuleFileNameEx(pshandle, 0)
    # win32gui.error
    except Exception:
      #  print(e)
        return None, None
    finally:
        win32api.CloseHandle(pshandle)
    caption = win32gui.GetWindowText(cur_wnd)
    file_name = os.path.basename(exe_name).split('.')[0]
    return file_name, caption


def main():
    App()


if __name__ == '__main__':
    main()
