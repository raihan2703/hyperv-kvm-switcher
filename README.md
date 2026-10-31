# Hyper-V & KVM Mode Switcher

A lightweight Windows 10/11 utility to seamlessly toggle the Windows Hypervisor state (`bcdedit /set hypervisorlaunchtype`) between:
1. **Hyper-V Active (for enable WSL2, Docker, etc)**
2. **Hyper-V Inactive (for nested KVM in GNS3)**

---

## 📌 Problem Background
On modern Windows systems (such as ThinkPad and other Secured-Core laptops), running virtualization software requires choosing between two hypervisor states:
- **WSL2, Docker Desktop, and Windows Sandbox** require the Windows Hypervisor (`hypervisorlaunchtype auto`).
- **GNS3 VM / VMware Nested KVM** requires direct, exclusive access to hardware virtualization (Intel VT-x / AMD-V) without Windows Hypervisor intercepting it (`hypervisorlaunchtype off`).

Manually opening an elevated command prompt and running `bcdedit` every time can be tedious. This tool automates the detection, mode selection, elevation, and system restart prompt in a clean GUI.

---

## ✨ Features
- **Auto Status Detection**: Reads the current Windows bootloader configuration (`bcdedit /enum {current}`) to accurately detect the active mode.
- **Auto UAC Elevation**: Automatically prompts for Administrator privileges on launch if not already elevated.
- **Smart Target Selection**: Pre-selects the opposite mode in the dropdown for 1-click switching.
- **Graceful Restart Prompt**: Provides a confirmation modal with options:
  - **Restart Now**: Immediately reboots the computer to apply bootloader changes.
  - **Cancel, Restart Later**: Safely applies the bootloader change so it takes effect on your next reboot.
- **Modern Dark UI**: Designed with clean contrast inspired by Windows 11 aesthetics.

---

## 🚀 How to Run

### Option 1: Standalone `.exe` (Recommended)
Download the latest `HyperV-KVM-Switcher.exe` from the [Releases](../../releases) tab or build it locally. Simply double-click the `.exe` and allow the Administrator prompt (UAC).

### Option 2: Run from Python Source
Ensure you have Python 3.8+ installed:
```powershell
python app.py
```

---

## 🛠️ Build from Source (.exe)
To compile the Python script into a standalone `.exe`:
```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --uac-admin --name "HyperV-KVM-Switcher" app.py
```
The compiled executable will be located in the `dist/` folder.

---

## 📋 Modes Explained

| Mode Name | Bootloader Setting | What Works |
| :--- | :--- | :--- |
| **`Hyper-V Active (for enable WSL2, Docker, etc)`** | `bcdedit /set hypervisorlaunchtype auto` | WSL2, Docker Desktop, Windows Sandbox, Hyper-V VMs |
| **`Hyper-V Inactive (for nested KVM in GNS3)`** | `bcdedit /set hypervisorlaunchtype off` | GNS3 VM (VMware Workstation) with `KVM support: True`, VirtualBox Hardware VT-x |

---

## ⚖️ License
MIT License. Free for personal, academic, and commercial use.
