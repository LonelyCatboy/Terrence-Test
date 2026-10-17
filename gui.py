import time
from threading import Thread
import tkinter as tk
from tkinter import ttk
from stats import StatsFile, StatsDB


from django.db.models import Window

class ScoreWindow():
    def __init__(self, score):
        self.root = tk.Toplevel()
        self.root.title("Score")
        self.root.resizable(True, True)


        


        #Headline
        ttk.Label(self.root,text= "TerrenceTest",font=("Small Fonts",15),background="#FDEC00",foreground="white").pack(fill="x",anchor="n",side="top",pady=0)

        
        #Score Label
        self.score_label = ttk.Label(self.root, text=f"Score: {score} Jeph", font=("Helvetica", 24))
        self.score_label.pack(pady=20)


        #User Entry
        self.user_entry = ttk.Entry(self.root)
        self.user_entry.pack(pady=20)

        #frame für buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=20)


        #Save Score Button
        self.save_button = ttk.Button(self.button_frame, text="Save Score", command=lambda: self.write_stats(score), width = 15)
        self.save_button.pack(side="left", padx=10)
        

        #Cancel Button
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.root.destroy, width = 15)
        self.cancel_button.pack(side="left", padx=10)


        #Ownership label
        self.owner_label = ttk.Label(self.root, text="By: LonelyCatboy", font=("Small Fonts", 8))
        self.owner_label.pack(side="bottom",anchor="e")



    def write_stats(self, score):
        if(self.user_entry.get() == "" or self.user_entry.get() == "Enter your name"):
            self.user_entry.configure(bg="lightcoral")
            self.user_entry.focus_set()
            return

        #statsfile schreiben
        print(StatsDB().save_stats(self.user_entry.get(), score))
        self.user_entry.delete(0, tk.END)
        self.root.destroy()

class StatsWindow():
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Stats")
        self.root.resizable(True, True)


        #Headline
        ttk.Label(self.root,text= "TerrenceTest",font=("Small Fonts",15),background="#FDEC00",foreground="white").pack(fill="x",anchor="n",side="top",pady=0)
        

        #Stats Label
        self.stats_label = ttk.Label(self.root, text="Stats", font=("Helvetica", 24))
        self.stats_label.pack(pady=20)


        #Stats Text
        self.stats_text = tk.Text(self.root, width=50, height = 10)
        self.stats_text.pack(pady=20,padx=20)
        self.stats_text.configure(state="disabled")


        #Load Stats Button
        self.load_stats_button = ttk.Button(self.root, text="Load Stats", command=self.load_stats)
        self.load_stats_button.pack(pady=20)


        #Ownership label
        self.owner_label = ttk.Label(self.root, text="By: LonelyCatboy", font=("Small Fonts", 8))
        self.owner_label.pack(side="bottom",anchor="e")

    def load_stats(self):
        stats = StatsDB().load_stats()
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
        self.root.resizable(True, True)

        #Headline
        ttk.Label(self.root,text= "TerrenceTest",font=("Small Fonts",15),background="#FDEC00",foreground="white").pack(fill="x",anchor="n",side="top",pady=0)



        #Stats Button
        ttk.Button(self.root, text="Stats", command=StatsWindow,width=20).pack(pady=20)


        #Timer Label
        self.timer_text = tk.StringVar()
        self.timer_text.set("00:00")

        self.timer_label = ttk.Label(self.root, textvariable=self.timer_text, font=("Helvetica", 48))
        self.timer_label.pack(pady=20)


        #Start Timer Button
        self.start_timer = ttk.Button(self.root, text="Start Timer", command=self.new_Timer,width=20,padding=5)
        self.start_timer.pack()


        #Scale für die Zeit in Minuten
        self.time_scale = ttk.Scale(self.root, from_=10, to_=60, orient="horizontal",length=150,command = lambda value: self.timer_text.set(f"{int(float(value)):02d}:00"))
        self.time_scale.set(15)
        self.time_scale.pack(pady = 10)
        


        #Increment Button
        self.increment_button = ttk.Button(self.root,text="+", command=self.increment,style="Accent.TButton", padding=50, width=20)
        self.increment_button.pack(pady=20,padx= 30)
        
        self.increment_button.configure(state="disabled")
        self.root.bind("<space>",func=self.increment)


        #Ownership label
        self.owner_label = ttk.Label(self.root, text="By: LonelyCatboy", font=("Small Fonts", 8))
        self.owner_label.pack(side="bottom",anchor="e")


        self.root.focus_force()
        self.root.mainloop()

        

    def increment(self,event=None):
        if self.timer == 0:
            return
        self.score += 1
        

    def new_Timer(self):
        try:
            self.score = 0
            self.increment_button.focus_force()
            self.timer = int(self.time_scale.get())
            self.end_time = time.time() + self.timer * 1 #TIMER 676767
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
                self.increment_button.focus_force()
                self.root.after(10, self.tick)
                return

            self.timer_text.set("00:00")
            self.time_scale.configure(state="normal")
            self.start_timer.configure(state="active")
            self.increment_button.configure(state="disabled")
            ScoreWindow(self.score/self.timer*3600)

MainWindow()   

