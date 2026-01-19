# pomodoro_tkinter_tomato.py
# Put tomato.png in the SAME folder as this file.

import tkinter as tkinter
class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)

        # ---- Pomodoro settings (minutes) ----
        self.WORK_MIN = 25
        self.SHORT_BREAK_MIN = 5
        self.LONG_BREAK_MIN = 15

        # ---- State ----
        self.reps = 0
        self.timer_id = None
        self.is_running = False
        self.remaining_sec = 0
        self.session_total_sec = 0
        self.session_type = "Ready"

        # ---- UI ----
        self.title_lbl = tkinter.Label(root, text="Pomodoro", font=("Arial", 20, "bold"))
        self.title_lbl.pack(pady=(12, 4))

        self.subtitle_lbl = tkinter.Label(root, text="Ready", font=("Arial", 11))
        self.subtitle_lbl.pack(pady=(0, 8))

        # Canvas
        self.canvas = tkinter.Canvas(root, width=300, height=320, highlightthickness=0)
        self.canvas.pack()

        # Pomodoro image (PNG)
        # IMPORTANT: keep reference in self.PomoPlanner.jpeg (otherwise it disappears)

        self.PomoPlanner.jpeg = tkinter.PhotoImage(file="PomodorPlanner.jpeg")
        self.canvas.create_image(150, 150, image=self.PomoPlanner.jpeg)

        # Time text over the image
        self.time_text = self.canvas.create_text(
            150, 170, text="00:00", fill="white", font=("Consolas", 32, "bold")
        )

        # Buttons
        btn_frame = tkinter.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = tkinter.Button(btn_frame, text="Start", width=10, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=6)

        self.pause_btn = tkinter.Button(btn_frame, text="Pause", width=10, command=self.pause, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=6)

        self.reset_btn = tkinter.Button(btn_frame, text="Reset", width=10, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=6)

        # Checkmarks
        self.check_lbl = tkinter.Label(root, text="", font=("Arial", 14))
        self.check_lbl.pack(pady=(0, 12))

        self._set_time_display(0)

    # ---------- Helpers ----------
    def _set_time_display(self, seconds):
        m = seconds // 60
        s = seconds % 60
        self.canvas.itemconfig(self.time_text, text=f"{m:02d}:{s:02d}")

    def _set_session_ui(self, title, subtitle):
        self.title_lbl.config(text=title)
        self.subtitle_lbl.config(text=subtitle)

    def _start_session(self, seconds, session_name):
        self.session_type = session_name
        self.session_total_sec = seconds
        self.remaining_sec = seconds

        if session_name == "Work":
            self._set_session_ui("Work", "Focus time 💪")
        elif session_name == "Short Break":
            self._set_session_ui("Break", "Short break ☕")
        else:
            self._set_session_ui("Break", "Long break 🌿")

        self._set_time_display(self.remaining_sec)
        self._run_tick()

    def _next_session(self):
        self.reps += 1

        if self.reps % 8 == 0:
            self._start_session(self.LONG_BREAK_MIN * 60, "Long Break")
        elif self.reps % 2 == 0:
            self._start_session(self.SHORT_BREAK_MIN * 60, "Short Break")
        else:
            self._start_session(self.WORK_MIN * 60, "Work")

        # Work sessions completed = reps//2
        self.check_lbl.config(text="✔" * (self.reps // 2))

    def _run_tick(self):
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")

        self._set_time_display(self.remaining_sec)

        if self.remaining_sec <= 0:
            self.is_running = False
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.timer_id = None

            self.root.bell()      # beep
            self._next_session()  # auto next session
            return

        self.remaining_sec -= 1
        self.timer_id = self.root.after(1000, self._run_tick)

    # ---------- Button actions ----------
    def start(self):
        if self.is_running:
            return
        # resume if paused, else start next
        if self.remaining_sec > 0 and self.session_total_sec > 0:
            self._run_tick()
        else:
            self._next_session()

    def pause(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.subtitle_lbl.config(text=f"Paused ({self.session_type}) ⏸️")

    def reset(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.is_running = False
        self.reps = 0
        self.remaining_sec = 0
        self.session_total_sec = 0
        self.session_type = "Ready"

        self._set_session_ui("Pomodoro", "Ready")
        self._set_time_display(0)
        self.check_lbl.config(text="")

        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")


if __name__ == "__main__":
    root = tkinter.Tk()
    PomodoroApp(root)
    root.mainloop()