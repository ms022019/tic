import tkinter as tk
from tkinter import ttk
import time
import pytz
from datetime import datetime
import math

class AnalogClock(tk.Canvas):
    def __init__(self, master, timezone='UTC', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.timezone = pytz.timezone(timezone)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.center = (self.width // 2, self.height // 2)
        self.radius = min(self.width, self.height) // 2 - 10
        self.hour_hand_length = self.radius * 0.5
        self.minute_hand_length = self.radius * 0.8
        self.second_hand_length = self.radius * 0.9
        self.current_time = datetime.now(self.timezone)
        self.ampm_mode = False  # Default to 24-hour mode
        self.summer_mode = False  # Default to summer_mode
        self.create_clock_face()
        self.update_clock()
        
    def create_clock_face(self):
        self.delete('all')
        self.create_oval(5, 5, self.width-5, self.height-5, outline='red', width=2)
        for i in range(12):
            angle = math.pi / 2 - i * (math.pi / 6)
            x = self.center[0] + self.radius * 0.9 * math.cos(angle)
            y = self.center[1] - self.radius * 0.9 * math.sin(angle)
            self.create_text(x, y, text=str(i if self.ampm_mode else i * 2),fill="red",  font=('Arial', 10, 'bold'))
        
    def update_clock(self):
        if self.ampm_mode :
            one_two = 1
        else :
            one_two = 2
        
        if self.summer_mode :
            summer = 1
        else :
            summer = 0
        
        self.delete('hands')
        now = datetime.now(self.timezone)
        self.current_time = now

        hours = now.hour % 12 if self.ampm_mode else now.hour
        hours = hours - summer
        minutes = now.minute
        seconds = now.second

        # Hour hand
        hour_angle = math.pi/2 - (hours + minutes/60) / one_two * (math.pi/6) 
        hour_x = self.center[0] + self.hour_hand_length * math.cos(hour_angle)
        hour_y = self.center[1] - self.hour_hand_length * math.sin(hour_angle)
        self.create_line(self.center[0], self.center[1], hour_x, hour_y, width=6, fill='black', tags='hands')

        # Minute hand
        minute_angle = math.pi/2 - minutes * (math.pi/30)
        minute_x = self.center[0] + self.minute_hand_length * math.cos(minute_angle)
        minute_y = self.center[1] - self.minute_hand_length * math.sin(minute_angle)
        self.create_line(self.center[0], self.center[1], minute_x, minute_y, width=4, fill='blue', tags='hands')

        # Second hand
        second_angle = math.pi/2 - seconds * (math.pi/30)
        second_x = self.center[0] + self.second_hand_length * math.cos(second_angle)
        second_y = self.center[1] - self.second_hand_length * math.sin(second_angle)
        self.create_line(self.center[0], self.center[1], second_x, second_y, width=2, fill='red', tags='hands')

        self.after(1000, self.update_clock)

class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analog Clock App")
        self.geometry("420x1000")
        
        self.clock = AnalogClock(self, timezone='Asia/Tokyo', width=400, height=400)
        self.clock.pack()

        self.clock1 = AnalogClock(self, timezone='Asia/Tokyo', width=400, height=400)
        self.clock1.pack()

        self.ampm_button = ttk.Button(self, text="Toggle 12/24 Hour", command=self.toggle_ampm)
        self.ampm_button.pack()

        self.summer = ttk.Button(self, text="Toggle summer", command=self.toggle_summer)
        self.summer.pack()

        self.timezone_var = tk.StringVar()
        self.timezone_menu = ttk.Combobox(self, textvariable=self.timezone_var)
        self.timezone_menu['values'] = pytz.all_timezones
        self.timezone_menu.current(pytz.all_timezones.index('Asia/Tokyo'))
        self.timezone_menu.pack()
        self.timezone_menu.bind("<<ComboboxSelected>>", self.change_timezone)

        self.style_var = tk.StringVar(value='default')
        self.style_menu = ttk.Combobox(self, textvariable=self.style_var)
        self.style_menu['values'] = ('default', 'dark', 'light')
        self.style_menu.pack()
        self.style_menu.bind("<<ComboboxSelected>>", self.change_style)

    def toggle_summer(self):
        self.clock.summer_mode = not self.clock.summer_mode
        self.clock.create_clock_face()
        self.clock.update_clock()

    def toggle_ampm(self):
        self.clock.ampm_mode = not self.clock.ampm_mode
        self.clock.create_clock_face()
        self.clock.update_clock()
        
    def change_timezone(self, event):
        timezone = self.timezone_var.get()
        self.clock.timezone = pytz.timezone(timezone)
        self.clock.update_clock()

    def change_style(self, event):
        style = self.style_var.get()

        if style == 'dark':
            bg_color = 'black'
        elif style == 'light':
            bg_color = 'white'
        else:
            bg_color = 'systemWindowBody'

        self.configure(bg=bg_color)
        self.clock.configure(bg=bg_color)
        self.clock.create_clock_face()
if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()
