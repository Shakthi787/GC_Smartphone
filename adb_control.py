# === adb_control.py ===
import subprocess

def send_adb_command(command: str):
    subprocess.run(f"adb shell {command}", shell=True)

def unlock_device():
    send_adb_command("input keyevent 26")
    send_adb_command("input swipe 300 1000 300 500")
    send_adb_command("input keyevent 3")  # Go to home after unlock

def lock_device():
    send_adb_command("input keyevent 26")

def open_app(app_name: str):
    app_package = {
        "WhatsApp": "com.whatsapp",
        "YouTube": "com.google.android.youtube",
        "Chrome": "com.android.chrome",
        "Settings": "com.android.settings",
        "Camera": "com.android.camera"
    }
    package = app_package.get(app_name)
    if package:
        send_adb_command(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")

def navigate_app(direction: str):
    if direction == "left":
        send_adb_command("input swipe 900 500 100 500")
    elif direction == "right":
        send_adb_command("input swipe 100 500 900 500")

def scroll_app(direction: str):
    if direction == "down":
        send_adb_command("input swipe 500 500 500 1000")
    elif direction == "up":
        send_adb_command("input swipe 500 1000 500 500")

def go_home():
    send_adb_command("input keyevent 3")

def open_notifications():
    send_adb_command("cmd statusbar expand-notifications")

def sync_mobile_ui(gesture, selected_app):
    if gesture == "FIST":
        unlock_device()
    elif gesture == "TWO_FINGERS":
        lock_device()
    elif gesture == "THUMBS_UP" and selected_app != "None":
        open_app(selected_app)
    elif gesture == "THREE_FINGERS":
        open_app("YouTube")
    elif gesture == "PALM":
        scroll_app("down")
    elif gesture == "SWIPE_LEFT":
        navigate_app("left")
    elif gesture == "SWIPE_RIGHT":
        navigate_app("right")
    elif gesture == "OK_SIGN":
        go_home()
    elif gesture == "VICTORY":
        open_notifications()
