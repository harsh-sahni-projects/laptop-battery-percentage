import tkinter as tk
import psutil
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

class BatteryOverlay:
    def __init__(self):
        self.root = tk.Tk()
        
        # Window Setup
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg="white")
        
        # Initial Position
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"80x40+{screen_width - 100}+20")

        # The Label (Your Battery Text)
        self.label = tk.Label(self.root, text="--%", font=("Segoe UI", 14, "bold"), 
                             fg="#2ecc71", bg="white", cursor="fleur")
        self.label.pack()

        # --- DRAGGING LOGIC ---
        # Bind the Left Mouse Click
        self.label.bind("<Button-1>", self.start_drag)
        # Bind the Mouse Movement while holding the button
        self.label.bind("<B1-Motion>", self.do_drag)

        self.visible = True
        self.update_battery()

    def start_drag(self, event):
        # Record the starting position of the click relative to the window
        self.x = event.x
        self.y = event.y

    def do_drag(self, event):
        # Calculate the new position of the window
        # 'event.x_root' is the mouse position on the whole screen
        deltax = event.x_root - self.x
        deltay = event.y_root - self.y
        self.root.geometry(f"+{deltax}+{deltay}")

    def update_battery(self):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            self.label.config(text=f"{percent}%")
            self.label.config(fg="#e74c3c" if percent < 20 else "#2ecc71")
        self.root.after(10000, self.update_battery)

    def toggle_visibility(self):
        if self.visible:
            self.root.withdraw()
        else:
            self.root.deiconify()
        self.visible = not self.visible

    def quit_app(self, icon):
        icon.stop()
        self.root.after(0, self.root.destroy())

def setup_tray(app):
    img = Image.new('RGB', (64, 64), (46, 204, 113))
    menu = Menu(
        MenuItem('Show/Hide', lambda: app.toggle_visibility()),
        MenuItem('Exit', lambda icon: app.quit_app(icon))
    )
    icon = Icon("Battery", img, "Battery Monitor", menu)
    icon.run()

if __name__ == "__main__":
    app = BatteryOverlay()
    threading.Thread(target=setup_tray, args=(app,), daemon=True).start()
    app.root.mainloop()