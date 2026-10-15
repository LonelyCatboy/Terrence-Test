import time
from threading import Thread
import tkinter as tk
from stats import StatsFile

from django.db.models import Window

#



class ScoreWindow():
    def __init__(self, score):
        self.root = tk.Toplevel()
        self.root.title("Score")
        self.root.resizable(False, False)


        #Score Label
        self.score_label = tk.Label(self.root, text=f"Score: {score} Jeph", font=("Helvetica", 24))
        self.score_label.pack(pady=20)


        #User Entry
        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack(pady=20)

        #frame für buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)


        #Save Score Button
        self.save_button = tk.Button(self.button_frame, text="Save Score", command=lambda: self.write_stats_file(score), width = 15)
        self.save_button.pack(side="left", padx=10)
        

        #Cancel Button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.root.destroy, width = 15)
        self.cancel_button.pack(side="left", padx=10)




    def write_stats_file(self, score):
        if(self.user_entry.get() == "" or self.user_entry.get() == "Enter your name"):
            self.user_entry.configure(bg="lightcoral")
            self.user_entry.focus_set()
            return

        #statsfile schreiben
        StatsFile().save_stats(self.user_entry.get(), score)
        self.user_entry.delete(0, tk.END)
        self.root.destroy()

class StatsWindow():
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Stats")
        self.root.resizable(False, False)

        #Stats Label
        self.stats_label = tk.Label(self.root, text="Stats", font=("Helvetica", 24))
        self.stats_label.pack(pady=20)

        #Stats Text
        self.stats_text = tk.Text(self.root, width=30, height=10)
        self.stats_text.pack(pady=20)
        self.stats_text.configure(state="disabled")

        #Load Stats Button
        self.load_stats_button = tk.Button(self.root, text="Load Stats", command=self.load_stats)
        self.load_stats_button.pack(pady=20)


    def load_stats(self):
        stats = StatsFile().load_stats()
        self.stats_text.configure(state="normal")
        self.stats_text.delete(1.0, tk.END)
        for s in stats:
            self.stats_text.insert(tk.END, s)
        self.stats_text.configure(state="disabled")


class MainWindow():
    def __init__(self):

        self.end_time = 0
        self.score = 0
        self.timer = 0


        self.root = tk.Tk()
        self.root.title("Terrence Test")
        self.root.geometry("300x400")
        self.root.resizable(False, False)


        #Stats Button
        tk.Button(self.root, text="Stats", command=StatsWindow,width=20).pack(pady=20)


        #Timer Label
        self.timer_text = tk.StringVar()
        self.timer_text.set("00:00")

        self.timer_label = tk.Label(self.root, textvariable=self.timer_text, font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        #Start Timer Button
        self.start_timer = tk.Button(self.root, text="Start Timer", command=self.new_Timer)
        self.start_timer.pack()


        #Scale für die Zeit in Minuten
        self.time_str_var = tk.StringVar(value="01 min")
        time_frame = tk.Frame(self.root)
        self.time_scale = tk.Scale(time_frame, from_=1, to=60, orient="horizontal",activebackground="lightblue",showvalue=False,command=lambda x: self.time_str_var.set(f"{int(x):02d} min"))
        self.time_scale.pack(side = "left",padx = 10)
        tk.Label(time_frame, textvariable=self.time_str_var).pack(side = "right")
        time_frame.pack(pady=20)

        #Increment Button
        self.increment_button = tk.Button(self.root, text="+", command=self.increment,padx = 100, pady = 150)
        self.increment_button.pack(pady=20)
        self.increment_button.configure(state="disabled")
        self.increment_button_default_bg = self.increment_button.cget("bg")
        self.root.bind("<space>", func= lambda event: self.increment_button.invoke())

        self.root.mainloop()

    def increment(self,event=None):
        if self.timer == 0:
            return
        self.score += 1
        self.increment_button.configure(bg="lightblue")
        self.increment_button.after(20, lambda: self.increment_button.configure(bg="SystemButtonFace"))
        

    def new_Timer(self):
        try:
            self.timer = int(self.time_scale.get())
            self.end_time = time.time() + self.timer * 60
            self.time_scale.configure(state="disabled")
            self.start_timer.configure(state="disabled")
            self.increment_button.configure(state="normal")
            self.tick()

        except ValueError:
            pass


    def format_time(self):
        t = int(self.end_time - self.t)
        minutes, seconds = divmod(t, 60)
        return f"{minutes:02d}:{seconds:02d}"


    def tick(self):
            self.t = time.time()
            if self.t < self.end_time:
                self.timer_text.set(self.format_time())
                self.root.after(10, self.tick)
                return

            self.timer_text.set("00:00")
            self.time_scale.configure(state="normal")
            self.start_timer.configure(state="active")
            ScoreWindow(self.score/self.timer*3600)
            self.score = 0
        
        

MainWindow()

