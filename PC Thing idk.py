import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import subprocess
import platform
import psutil

# === Functions ===

# --- Storage ---
def clear_temp_files():
    temp = os.getenv('TEMP')
    try:
        for root, dirs, files in os.walk(temp):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
        messagebox.showinfo("Success", "Temp files cleared.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def empty_recycle_bin():
    try:
        import winshell
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        messagebox.showinfo("Success", "Recycle Bin emptied.")
    except ImportError:
        messagebox.showwarning("Missing Package", "Install with: pip install winshell")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_disk_cleanup():
    subprocess.Popen("cleanmgr")

# --- Network ---
def restart_network():
    subprocess.call("ipconfig /release", shell=True)
    subprocess.call("ipconfig /renew", shell=True)
    messagebox.showinfo("Success", "Network adapter restarted.")

def flush_dns():
    subprocess.call("ipconfig /flushdns", shell=True)
    messagebox.showinfo("Success", "DNS cache flushed.")

def show_ip():
    output = subprocess.getoutput("ipconfig")
    show_output("IP Configuration", output)

# --- Performance ---
def fake_clean_ram():
    messagebox.showinfo("Simulated", "Simulated RAM clean. Close unused apps for best results.")

def fps_tips():
    tips = """
💡 FPS Boost Tips:
- High Performance Mode
- Update GPU Drivers
- Close Background Apps
- Disable Xbox Game Bar
"""
    messagebox.showinfo("Tips", tips)

def disable_startup():
    subprocess.Popen("taskmgr")
    messagebox.showinfo("Hint", "Go to 'Startup' tab to disable startup programs.")

# --- System Info ---
def system_info():
    info = f"""
System: {platform.system()}
Node: {platform.node()}
Release: {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB
"""
    show_output("System Info", info)

def show_output(title, content):
    win = tk.Toplevel(root)
    win.title(title)
    text = tk.Text(win, wrap="word", bg="#111", fg="lime")
    text.insert("1.0", content)
    text.pack(expand=True, fill="both")

# === UI Functions ===
def create_button(parent, text, command):
    return ttk.Button(parent, text=text, command=command)

def make_section(parent, title, buttons):
    section = ttk.LabelFrame(parent, text=title)
    section.pack(padx=10, pady=10, fill="x")
    for btn_text, cmd in buttons:
        create_button(section, btn_text, cmd).pack(fill="x", padx=5, pady=3)

def load_main_ui():
    loading_frame.destroy()
    canvas = tk.Canvas(root, bg="#1e1e1e")
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Label(scroll_frame, text="🛠️ System Utility Dashboard", style="Title.TLabel").pack(pady=10)

    make_section(scroll_frame, "📁 Storage Tools", [
        ("🧹 Clear Temp Files", clear_temp_files),
        ("🗑️ Empty Recycle Bin", empty_recycle_bin),
        ("🧰 Open Disk Cleanup", open_disk_cleanup)
    ])

    make_section(scroll_frame, "📶 Network Tools", [
        ("🔁 Restart Network", restart_network),
        ("🧼 Flush DNS", flush_dns),
        ("🌐 Show IP Config", show_ip)
    ])

    make_section(scroll_frame, "🎮 Performance Tools", [
        ("🚀 Clean RAM (Simulated)", fake_clean_ram),
        ("📈 Show FPS Tips", fps_tips),
        ("⚙️ Disable Startup Apps", disable_startup)
    ])

    make_section(scroll_frame, "🖥️ System Info", [
        ("🔍 Show System Info", system_info)
    ])

    create_button(scroll_frame, "❌ Exit", root.quit).pack(pady=15)

def loading_animation():
    for i in range(101):
        loading_label.config(text=f"Loading... {i}%")
        time.sleep(0.015)
    load_main_ui()

# === Main Window ===
root = tk.Tk()
root.title("PC Toolbox")
root.geometry("500x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")
style.configure(".", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))
style.configure("TButton", padding=6, background="#2e2e2e", foreground="white")
style.map("TButton", background=[("active", "#4caf50")])
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="lime")

# === Loading Frame ===
loading_frame = tk.Frame(root, bg="#1e1e1e")
loading_frame.pack(expand=True, fill="both")
loading_label = tk.Label(loading_frame, text="Loading... 0%", font=("Consolas", 18), fg="white", bg="#1e1e1e")
loading_label.pack(expand=True)

threading.Thread(target=loading_animation).start()

root.mainloop()
# == End ==