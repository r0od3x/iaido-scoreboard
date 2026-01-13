import tkinter as tk
import math
from collections import Counter

red_time = 0
white_time = 0
red_running = False
white_running = False
controls_enabled = False
current_score = ""
team_mode = False
match_index = 0
red_wins = 0
white_wins = 0
red_team_entries = []
white_team_entries = []
red_team_names = []
white_team_names = []
match_history = []
pending_score = ""

def update_red_timer():
    global red_time
    if controls_enabled and red_running:
        red_time += 1
        red_timer_label.config(
            text=f"{red_time//60:02}:{red_time%60:02}",
            fg="white"
        )
    elif controls_enabled:
        red_timer_label.config(
            text=f"⏸ {red_time//60:02}:{red_time%60:02}",
            fg="lightgray"
        )
    root.after(1000, update_red_timer)

def update_white_timer():
    global white_time
    if controls_enabled and white_running:
        white_time += 1
        white_timer_label.config(
            text=f"{white_time//60:02}:{white_time%60:02}",
            fg="black"
        )
    elif controls_enabled:
        white_timer_label.config(
            text=f"⏸ {white_time//60:02}:{white_time%60:02}",
            fg="gray"
        )
    root.after(1000, update_white_timer)

def start_match():
    global controls_enabled, red_team_names, white_team_names, match_index
    controls_enabled = True
    match_index = 0

    if team_mode:
        red_team_names[:] = [entry.get().strip() for entry in red_team_entries]
        white_team_names[:] = [entry.get().strip() for entry in white_team_entries]
        match_history.clear()
        set_match_names()
    else:
        top_label.config(text=red_name_entry.get().strip() or "Red")
        bottom_label.config(text=white_name_entry.get().strip() or "White")

    form_frame.pack_forget()
    split_screen_frame.pack(fill="both", expand=True)
    root.focus_set()

    update_red_timer()
    update_white_timer()

def set_match_names():
    global match_index
    if team_mode:
        if match_index < 3:
            top_label.config(text=red_team_names[match_index])
            bottom_label.config(text=white_team_names[match_index])
        else:
            check_series_winner()
    else:
        # Solo mode: no changes per round
        pass

def on_key_press(event):
    global red_running, white_running, match_index, red_wins, white_wins
    global red_time, white_time, current_score, pending_score, controls_enabled
    # Quit with q anywhere, even on homepage
    if event.char.lower() == 'q':
        root.quit()
        return

    # If not enabled and key not Escape, ignore
    if not controls_enabled and event.keysym != 'Escape':
        return

    key = event.char.lower() if event.char else ""
    if key == '2':
        pending_score = "2 - 1"
    elif key == '3':
        pending_score = "3 - 0"
    elif key == 'r' and pending_score:
        red_wins += 1
        match_history.append(('red', pending_score))
        current_score = pending_score
        pending_score = ""
        show_round_winner("red")
    elif key == 'w' and pending_score:
        white_wins += 1
        match_history.append(('white', pending_score))
        current_score = pending_score
        pending_score = ""
        show_round_winner("white")
    elif key == 'z' and match_history:
        undo_last_match()
    elif key == '4':
        red_running = not red_running
    elif key == '5':
        white_running = not white_running
    elif event.keysym == 'Escape':
        # Escape pressed: go home if no overlay shown
        go_home()

def reset_timers():
    global red_time, white_time, red_running, white_running
    red_time = 0
    white_time = 0
    red_running = False
    white_running = False
    red_timer_label.config(text="00:00")
    white_timer_label.config(text="00:00")

def undo_last_match():
    global match_index, red_wins, white_wins, current_score, pending_score
    last_color, last_score = match_history.pop()
    if last_color == 'red':
        red_wins -= 1
    else:
        white_wins -= 1
    match_index -= 1
    current_score = ""
    pending_score = last_score  # restore pending score for re-entry
    reset_timers()
    set_match_names()

def check_series_winner():
    if red_wins > white_wins:
        show_winner("red")
    elif white_wins > red_wins:
        show_winner("white")
    else:
        show_draw()

# New smooth cubic ease out function for subtle animation
def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def animate_overlay(overlay, label, score_lbl=None, step=0, max_steps=60):
    t = step / max_steps
    eased_t = ease_out_cubic(t)
    alpha = eased_t
    scale = 0.8 + 0.2 * eased_t
    try:
        overlay.attributes("-alpha", alpha)
    except:
        pass
    label.config(font=("Arial", int(64 * scale), "bold"))
    if score_lbl:
        score_lbl.config(font=("Arial", int(48 * scale), "bold"))
    if step < max_steps:
        overlay.after(25, animate_overlay, overlay, label, score_lbl, step + 1, max_steps)

def animate_overlay_out(overlay, callback=None, step=60, max_steps=60):
    t = step / max_steps
    eased_t = ease_out_cubic(t)
    alpha = eased_t
    try:
        overlay.attributes("-alpha", alpha)
    except:
        pass
    if step > 0:
        overlay.after(25, animate_overlay_out, overlay, callback, step - 1, max_steps)
    else:
        if callback:
            callback()
        overlay.destroy()


def show_round_winner(color):
    overlay = tk.Toplevel(root)
    overlay.attributes('-fullscreen', True)
    overlay.overrideredirect(True)
    bg_color = "#8B0000" if color == "red" else "#f0f0f0"
    overlay.configure(bg=bg_color)
    fg = "white" if color == "red" else "black"
    name = top_label.cget("text") if color == "red" else bottom_label.cget("text")

    message = f"{name} Wins Round {match_index + 1}!"
    label = tk.Label(
        overlay,
        text=message,
        font=("Arial", 1, "bold"),  # start small for animation
        fg=fg,
        bg=bg_color
    )
    label.place(relx=0.5, rely=0.4, anchor="center")

    score_lbl = None
    if current_score:
        score_lbl = tk.Label(
            overlay,
            text=current_score,
            font=("Arial", 1, "bold"),
            fg=fg,
            bg=bg_color
        )
        score_lbl.place(relx=0.5, rely=0.6, anchor="center")

    overlay.bind("<Key-q>", lambda e: root.quit())
    overlay.bind("<Escape>", lambda e: animate_overlay_out(overlay))
    overlay.bind("<Button-1>", lambda e: animate_overlay_out(overlay))

    animate_overlay(overlay, label, score_lbl)

    def proceed():
        if not team_mode:
            animate_overlay_out(overlay)  # FIXED: no fade_to_final_winner
        else:
            animate_overlay_out(overlay, callback=next_round)

    overlay.after(3000, proceed)  # slower pause for better effect


def fade_to_final_winner(prev_overlay):
    def show_final():
        prev_overlay.destroy()
        winner_color = match_history[-1][0] if match_history else None
        if winner_color:
            show_winner(winner_color)
    animate_overlay_out(prev_overlay, callback=show_final)

def next_round():
    global match_index
    match_index += 1
    reset_timers()
    set_match_names()

def calculate_series_score(history):
    counter = Counter([winner for winner, _ in history])
    return counter['red'], counter['white']

def show_winner(color):
    winner_overlay = tk.Toplevel(root)
    winner_overlay.attributes('-fullscreen', True)
    winner_overlay.overrideredirect(True)

    red_final, white_final = calculate_series_score(match_history)
    series_score = f"({red_final} - {white_final})"

    if color == "red":
        bg_color = "#8B0000"
        fg_color = "white"
        message = f"Red Team Wins the Series! {series_score}"
    else:
        bg_color = "#f0f0f0"
        fg_color = "#222"
        message = f"White Team Wins the Series! {series_score}"

    winner_overlay.configure(bg=bg_color)

    label = tk.Label(
        winner_overlay,
        text=message,
        font=("Arial", 1, "bold"),
        fg=fg_color,
        bg=bg_color
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    winner_overlay.bind("<Key-q>", lambda e: root.quit())
    winner_overlay.bind("<Escape>", lambda e: animate_overlay_out(winner_overlay))
    winner_overlay.bind("<Button-1>", lambda e: animate_overlay_out(winner_overlay))

    animate_overlay(winner_overlay, label)

def show_draw():
    draw_overlay = tk.Toplevel(root)
    draw_overlay.attributes('-fullscreen', True)
    draw_overlay.overrideredirect(True)
    draw_overlay.configure(bg="gray")
    label = tk.Label(
        draw_overlay,
        text="DRAW!",
        font=("Arial", 72, "bold"),
        fg="white",
        bg="gray"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")
    draw_overlay.bind("<Key-q>", lambda e: root.quit())
    draw_overlay.bind("<Escape>", lambda e: animate_overlay_out(draw_overlay))
    draw_overlay.bind("<Button-1>", lambda e: animate_overlay_out(draw_overlay))
    animate_overlay(draw_overlay, label)

def show_name_input():
    global red_name_entry, white_name_entry, red_team_entries, white_team_entries
    red_team_entries = []
    white_team_entries = []

    for widget in form_frame.winfo_children():
        widget.destroy()

    form_title = tk.Label(form_frame, text="Enter Player Names", font=("Arial", 36, "bold"), bg="#1e1e2f", fg="#f0f0f0")
    form_title.pack(pady=40)

    if team_mode:
        tk.Label(form_frame, text="Red Team (3 Players):", font=("Arial", 20), bg="#1e1e2f", fg="red").pack()
        for _ in range(3):
            e = tk.Entry(form_frame, font=("Arial", 18), bg="#2e2e3f", fg="white")
            e.pack(pady=5)
            red_team_entries.append(e)

        tk.Label(form_frame, text="White Team (3 Players):", font=("Arial", 20), bg="#1e1e2f", fg="gray").pack()
        for _ in range(3):
            e = tk.Entry(form_frame, font=("Arial", 18), bg="#2e2e3f", fg="white")
            e.pack(pady=5)
            white_team_entries.append(e)
    else:
        tk.Label(form_frame, text="Red Name:", font=("Arial", 20), bg="#1e1e2f", fg="red").pack()
        red_name_entry = tk.Entry(form_frame, font=("Arial", 18), bg="#2e2e3f", fg="white")
        red_name_entry.pack(pady=5)

        tk.Label(form_frame, text="White Name:", font=("Arial", 20), bg="#1e1e2f", fg="gray").pack()
        white_name_entry = tk.Entry(form_frame, font=("Arial", 18), bg="#2e2e3f", fg="white")
        white_name_entry.pack(pady=5)

    submit_btn = tk.Button(form_frame, text="Start Match", font=("Arial", 20), bg="#00adb5", fg="white", command=start_match)
    submit_btn.pack(pady=40)

    form_frame.pack(fill="both", expand=True)

def choose_mode(is_team):
    global team_mode
    team_mode = is_team
    mode_frame.pack_forget()
    show_name_input()

def go_home():
    global controls_enabled, match_index, red_wins, white_wins, match_history, current_score, pending_score
    controls_enabled = False
    match_index = 0
    red_wins = 0
    white_wins = 0
    match_history.clear()
    current_score = ""
    pending_score = ""
    reset_timers()
    split_screen_frame.pack_forget()
    form_frame.pack_forget()
    mode_frame.pack(fill="both", expand=True)
    root.focus_set()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.overrideredirect(True)
root.bind("<Key>", on_key_press)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

mode_frame = tk.Frame(root, bg="#1e1e2f")
mode_frame.pack(fill="both", expand=True)

# Small "Made by" label at the bottom of mode_frame
made_by_label = tk.Label(
    mode_frame,
    text="Made by Ghalbi Mohamed Reda",
    font=("Arial", 8),
    fg="white",
    bg="#1e1e2f"
)
made_by_label.pack(side="bottom", pady=5)

mode_label = tk.Label(mode_frame, text="Choose Mode", font=("Arial", 36, "bold"), bg="#1e1e2f", fg="white")
mode_label.pack(pady=60)

solo_btn = tk.Button(mode_frame, text="Solo Match", font=("Arial", 18, "bold"), bg="#00adb5", fg="white", activebackground="#007d84", relief="flat", padx=20, pady=10, command=lambda: choose_mode(False))
solo_btn.pack(pady=20)

team_btn = tk.Button(mode_frame, text="Team Match (3v3)", font=("Arial", 18, "bold"), bg="#00adb5", fg="white", activebackground="#007d84", relief="flat", padx=20, pady=10, command=lambda: choose_mode(True))
team_btn.pack(pady=20)

form_frame = tk.Frame(root, bg="#1e1e2f")
split_screen_frame = tk.Frame(root)

top_frame = tk.Frame(split_screen_frame, bg="red", width=screen_width, height=screen_height//2)
bottom_frame = tk.Frame(split_screen_frame, bg="white", width=screen_width, height=screen_height//2)

top_frame.pack(side="top", fill="both", expand=True)
bottom_frame.pack(side="bottom", fill="both", expand=True)

top_label = tk.Label(top_frame, text="", bg="red", fg="white", font=("Arial", 40, "bold"), anchor="w")
top_label.place(relx=0.02, rely=0.4, anchor="w")

bottom_label = tk.Label(bottom_frame, text="", bg="white", fg="black", font=("Arial", 40, "bold"), anchor="w")
bottom_label.place(relx=0.02, rely=0.4, anchor="w")

red_timer_label = tk.Label(top_frame, text="00:00", bg="red", fg="white", font=("Arial", 60, "bold"))
red_timer_label.place(relx=0.98, rely=0.5, anchor="e")

white_timer_label = tk.Label(bottom_frame, text="00:00", bg="white", fg="black", font=("Arial", 60, "bold"))
white_timer_label.place(relx=0.98, rely=0.5, anchor="e")

root.mainloop()
