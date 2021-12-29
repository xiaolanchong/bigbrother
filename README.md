
# About

A simple app to track the user activity: the current active window and time period it is active.
To calculate statistics you can show working and distracting actions. Windows only.

# Requires

win32process, win32api, win32con

# Usage

1. Run and leave the app.
2. Do something.
3. Press Ctrl+C and shut the app down.
4. Look at *activity.txt*
5. Log format: time duration <tab> activity start time <tab> activity end time <tab> title of the active window
