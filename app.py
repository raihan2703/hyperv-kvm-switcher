"""
Hyper-V & KVM Mode Switcher
Unified utility for Windows 10/11 to toggle between:
- Hyper-V Active (for enable WSL2, Docker, etc)
- Hyper-V Inactive (for nested KVM in GNS3)

Automates:
1. BCDedit hypervisorlaunchtype ({current})
2. DISM Windows Features (VirtualMachinePlatform & WSL)
3. DG_Readiness_Tool UEFI VBS Opt-Out Remediation
"""

import sys
import os
import subprocess
import threading
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

MODE_ACTIVE = "Hyper-V Active (for enable WSL2, Docker, etc)"
MODE_INACTIVE = "Hyper-V Inactive (for nested KVM in GNS3)"
MODE_UNKNOWN = "Unknown / Undetermined"

def get_script_path():
    """
    Finds DG_Readiness_Tool_v3.6.ps1 regardless of whether the app is running
    as a Python script, inside dist folder, or bundled.
    """
    candidates = []
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        candidates.append(os.path.join(exe_dir, "DG_Readiness_Tool_v3.6.ps1"))
        candidates.append(os.path.join(exe_dir, "..", "DG_Readiness_Tool_v3.6.ps1"))
    
    file_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(file_dir, "DG_Readiness_Tool_v3.6.ps1"))
    candidates.append(os.path.join(file_dir, "dist", "DG_Readiness_Tool_v3.6.ps1"))
    candidates.append(r"D:\hyperv-kvm-switcher\DG_Readiness_Tool_v3.6.ps1")
    candidates.append(r"D:\hyperv-kvm-switcher\dist\DG_Readiness_Tool_v3.6.ps1")

    for p in candidates:
        abs_p = os.path.abspath(p)
        if os.path.exists(abs_p):
            return abs_p
    return None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run_as_admin():
    if getattr(sys, 'frozen', False):
        exe = sys.executable
        args = ""
    else:
        exe = sys.executable
        args = f'"{os.path.abspath(__file__)}"'
    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, args, None, 1)
    sys.exit(0)

def get_current_hypervisor_mode():
    try:
        cmd = ["bcdedit"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        output = result.stdout.lower()

        for line in output.splitlines():
            line_clean = line.strip()
            if "hypervisorlaunchtype" in line_clean:
                parts = line_clean.split()
                if len(parts) >= 2:
                    val = parts[-1].strip()
                    if val == "off":
                        return MODE_INACTIVE
                    elif val in ["auto", "on"]:
                        return MODE_ACTIVE
        
        return MODE_ACTIVE
    except Exception as e:
        print(f"Error checking bcdedit: {e}")
        return MODE_UNKNOWN

def run_mode_switch_workflow(target_mode, progress_callback=None):
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

    if target_mode == MODE_ACTIVE:
        if progress_callback:
            progress_callback("Enabling VirtualMachinePlatform & WSL...")
        
        subprocess.run(
            ["dism", "/online", "/enable-feature", "/featurename:VirtualMachinePlatform", "/all", "/norestart"],
            creationflags=flags
        )
        subprocess.run(
            ["dism", "/online", "/enable-feature", "/featurename:Microsoft-Windows-Subsystem-Linux", "/all", "/norestart"],
            creationflags=flags
        )

        if progress_callback:
            progress_callback("Configuring bootloader to auto...")
        subprocess.run(["bcdedit", "/set", "{current}", "hypervisorlaunchtype", "auto"], creationflags=flags)

    else: # MODE_INACTIVE (for GNS3 & KVM)
        if progress_callback:
            progress_callback("Disabling VirtualMachinePlatform...")
        subprocess.run(
            ["dism", "/online", "/disable-feature", "/featurename:VirtualMachinePlatform", "/norestart"],
            creationflags=flags
        )

        if progress_callback:
            progress_callback("Configuring bootloader to off...")
        subprocess.run(["bcdedit", "/set", "{current}", "hypervisorlaunchtype", "off"], creationflags=flags)

        ps_script = get_script_path()
        if ps_script and os.path.exists(ps_script):
            if progress_callback:
                progress_callback(f"Executing DG Readiness Tool ({os.path.basename(ps_script)})...")
            
            script_dir = os.path.dirname(ps_script)
            # Run powershell directly in script's working directory
            res = subprocess.run(
                ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", 
                 f"Set-Location '{script_dir}'; .\\DG_Readiness_Tool_v3.6.ps1 -Disable -ReadyForRemediation"],
                capture_output=True,
                text=True,
                creationflags=flags
            )
            print("DG Tool output:", res.stdout, res.stderr)
        else:
            if progress_callback:
                progress_callback("Warning: DG_Readiness_Tool_v3.6.ps1 not found!")

    return True

def restart_computer():
    try:
        subprocess.run(["shutdown", "/r", "/t", "0"], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to restart: {e}")

class CustomRestartDialog(tk.Toplevel):
    def __init__(self, parent, target_mode):
        super().__init__(parent)
        self.title("Restart Required")
        self.geometry("480x240")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")
        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = 480
        h = 240
        x = px + max(0, (pw - w) // 2)
        y = py + max(0, (ph - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        icon_lbl = tk.Label(self, text="⚡", font=("Segoe UI", 26), bg="#1E1E1E", fg="#10B981")
        icon_lbl.pack(pady=(12, 3))

        note_extra = ""
        if target_mode == MODE_INACTIVE:
            note_extra = "\n⚠️ IMPORTANT: Press F3 or Windows Key when prompted on boot\nto confirm UEFI VBS Opt-Out!"

        msg = tk.Label(
            self,
            text=f"Configuration & DG Tool applied successfully!{note_extra}\n\nWould you like to restart your computer now?",
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#EDEDED",
            justify="center"
        )
        msg.pack(pady=(0, 15))

        btn_frame = tk.Frame(self, bg="#1E1E1E")
        btn_frame.pack(fill="x", padx=30)

        restart_btn = tk.Button(
            btn_frame,
            text="Restart Now",
            font=("Segoe UI", 9, "bold"),
            bg="#0D6EFD",
            fg="white",
            activebackground="#0B5ED7",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.on_restart
        )
        restart_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        later_btn = tk.Button(
            btn_frame,
            text="Cancel, Restart Later",
            font=("Segoe UI", 9),
            bg="#374151",
            fg="#EDEDED",
            activebackground="#4B5563",
            activeforeground="#EDEDED",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.on_later
        )
        later_btn.pack(side="right", expand=True, fill="x", padx=(8, 0))

    def on_restart(self):
        self.destroy()
        restart_computer()

    def on_later(self):
        self.destroy()
        sys.exit(0)

class HyperVSwitcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hyper-V & KVM Mode Switcher")
        self.geometry("550x400")
        self.resizable(False, False)
        self.configure(bg="#121212")

        self.center_window()
        self.current_mode = get_current_hypervisor_mode()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        w = 550
        h = 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def create_widgets(self):
        header = tk.Frame(self, bg="#1F2937", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Hyper-V & KVM Mode Switcher",
            font=("Segoe UI", 13, "bold"),
            bg="#1F2937",
            fg="#F9FAFB"
        )
        title.pack(side="left", padx=20, pady=16)

        badge_admin = tk.Label(
            header,
            text="Administrator",
            font=("Segoe UI", 8, "bold"),
            bg="#065F46",
            fg="#A7F3D0",
            padx=8,
            pady=3
        )
        badge_admin.pack(side="right", padx=20, pady=18)

        body = tk.Frame(self, bg="#121212", padx=25, pady=20)
        body.pack(fill="both", expand=True)

        lbl_current_title = tk.Label(
            body,
            text="Current Mode:",
            font=("Segoe UI", 9, "bold"),
            bg="#121212",
            fg="#9CA3AF"
        )
        lbl_current_title.pack(anchor="w")

        curr_frame = tk.Frame(body, bg="#1F2937", relief="flat", padx=12, pady=10)
        curr_frame.pack(fill="x", pady=(5, 18))

        dot_color = "#10B981" if self.current_mode == MODE_ACTIVE else "#3B82F6"
        dot = tk.Label(curr_frame, text="●", font=("Segoe UI", 12), bg="#1F2937", fg=dot_color)
        dot.pack(side="left", padx=(0, 8))

        self.lbl_current_val = tk.Label(
            curr_frame,
            text=self.current_mode,
            font=("Segoe UI", 9, "bold"),
            bg="#1F2937",
            fg="#F3F4F6",
            wraplength=440,
            justify="left"
        )
        self.lbl_current_val.pack(side="left", fill="x")

        lbl_switch_title = tk.Label(
            body,
            text="Switch to:",
            font=("Segoe UI", 9, "bold"),
            bg="#121212",
            fg="#9CA3AF"
        )
        lbl_switch_title.pack(anchor="w")

        if self.current_mode == MODE_ACTIVE:
            default_target = MODE_INACTIVE
        else:
            default_target = MODE_ACTIVE

        self.switch_var = tk.StringVar(value=default_target)
        modes = [MODE_ACTIVE, MODE_INACTIVE]

        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground="#1F2937",
            background="#374151",
            foreground="#F9FAFB",
            arrowcolor="#F9FAFB",
            bordercolor="#374151",
            lightcolor="#374151",
            darkcolor="#374151",
            padding=6
        )

        self.combo = ttk.Combobox(
            body,
            textvariable=self.switch_var,
            values=modes,
            state="readonly",
            font=("Segoe UI", 9),
            style="TCombobox"
        )
        self.combo.pack(fill="x", pady=(5, 15))

        self.lbl_status = tk.Label(
            body,
            text="",
            font=("Segoe UI", 8, "italic"),
            bg="#121212",
            fg="#60A5FA"
        )
        self.lbl_status.pack(anchor="w", pady=(0, 10))

        self.btn_frame = tk.Frame(body, bg="#121212")
        self.btn_frame.pack(fill="x", side="bottom")

        self.btn_ok = tk.Button(
            self.btn_frame,
            text="OK",
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            padx=28,
            pady=7,
            cursor="hand2",
            command=self.on_ok
        )
        self.btn_ok.pack(side="right", padx=(10, 0))

        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="Cancel",
            font=("Segoe UI", 9),
            bg="#374151",
            fg="#F3F4F6",
            activebackground="#4B5563",
            activeforeground="#F3F4F6",
            relief="flat",
            padx=20,
            pady=7,
            cursor="hand2",
            command=self.on_cancel
        )
        self.btn_cancel.pack(side="right")

    def on_ok(self):
        target_mode = self.switch_var.get()
        if target_mode == self.current_mode:
            messagebox.showinfo(
                "Notice",
                f"Your system is already in:\n\n{target_mode}\n\nNo change needed."
            )
            return

        self.btn_ok.config(state="disabled", text="Processing...")
        self.btn_cancel.config(state="disabled")
        self.combo.config(state="disabled")

        def worker():
            def update_progress(msg):
                self.lbl_status.config(text=msg)
                self.update_idletasks()

            run_mode_switch_workflow(target_mode, update_progress)
            
            self.lbl_status.config(text="Finished!")
            self.btn_ok.config(state="normal", text="OK")
            self.btn_cancel.config(state="normal")
            self.combo.config(state="readonly")
            
            CustomRestartDialog(self, target_mode)

        threading.Thread(target=worker, daemon=True).start()

    def on_cancel(self):
        self.destroy()

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        app = HyperVSwitcherApp()
        app.mainloop()
