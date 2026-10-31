# ⚡ Hyper-V & KVM Mode Switcher (GNS3 & WSL2 Dual-Mode Utility)

<p align="center">
  <a href="#english">English</a> •
  <a href="#bahasa-indonesia">Bahasa Indonesia</a>
</p>

---

<div id="english"></div>

## 🌐 English

### 📌 Overview & Purpose
**Hyper-V & KVM Mode Switcher** is an automated Windows 10/11 system utility designed to solve virtualization conflicts between **GNS3 VM (VMware Workstation)** and **WSL2 / Docker Desktop**.

On modern Windows PCs (especially Lenovo ThinkPad, Dell Latitude, HP EliteBook, and other Secured-Core PCs), users often face critical GNS3 errors:
- `KVM support available: False` inside GNS3 VM.
- VMware error: *"Run without Intel VT-x?"* or *"Feature 'hv.capable' was 0, but must be at least 0x1"*.
- High CPU spikes (100%) and sluggish performance on Cisco vIOS, MikroTik, or QEMU appliances.

This issue occurs because the Windows Hypervisor and Virtualization-Based Security (VBS) monopolize hardware virtualization (Intel VT-x / AMD-V), blocking VMware from enabling nested KVM.

**Hyper-V & KVM Mode Switcher** automates the entire switching pipeline in a clean GUI, seamlessly configuring the Windows Bootloader (`bcdedit`), Windows Features (`DISM`), and UEFI VBS remediation scripts with a single click.

---

### 📁 Repository Structure
```text
hyperv-kvm-switcher/
├── HyperV-KVM-Mode-Switcher.exe   # Standalone executable (Ready-to-use, no Python needed)
├── DG_Readiness_Tool_v3.6.ps1     # UEFI VBS Remediation Script
├── DefaultWindows_*.xml / .p7b    # DG Tool policy dependencies
├── app.py                         # Complete Python source code
├── README.md                      # Documentation
└── LICENSE                        # MIT License
```

---

### 🎛️ Modes Explained

| Mode | What it Does | Target Applications |
| :--- | :--- | :--- |
| **`Hyper-V Inactive (for nested KVM in GNS3)`** | Disables Windows Hypervisor & releases hardware VT-x locks via automated UEFI remediation. | **GNS3 VM with `KVM: True`**, VMware Workstation Nested Virtualization, Cisco vIOS / QEMU fast emulation. |
| **`Hyper-V Active (for enable WSL2, Docker, etc)`** | Enables `VirtualMachinePlatform`, `WSL`, and sets `bcdedit hypervisorlaunchtype auto`. | **WSL2 (Ubuntu/Debian)**, Docker Desktop, Kubernetes, Windows Sandbox. |

---

### 🚀 How to Use (Plug & Play)

No Python installation or compilation is required for regular users!

1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/raihan2703/hyperv-kvm-switcher.git
   cd hyperv-kvm-switcher
   ```
2. **Run the Executable**:
   - Double-click **`HyperV-KVM-Mode-Switcher.exe`** directly from the repository folder.
   - Accept the Administrator (UAC) prompt.
3. **Switch Mode**:
   - The app displays your **Current Mode**.
   - Select your desired mode from the **Switch to:** dropdown.
   - Click **OK**.
4. **Reboot**:
   - When the confirmation popup appears, click **Restart Now**.
   - *(Note: When switching to GNS3 KVM Mode for the first time, press **F3** or **Windows Key** on the UEFI boot screen to confirm VBS opt-out).*
5. **Done!**
   - Boot into Windows and launch either GNS3 (with `KVM: True`) or WSL2 with full performance.

---

### 🛠️ Optional: Run or Build from Source (Developers)
If you prefer running or modifying the Python source code directly:
```powershell
# Run source code
python app.py

# Or rebuild the executable
pip install pyinstaller
pyinstaller --noconsole --onefile --uac-admin --name "HyperV-KVM-Mode-Switcher" app.py
```

---

<div id="bahasa-indonesia"></div>

## 🇮🇩 Bahasa Indonesia

### 📌 Ringkasan & Tujuan
**Hyper-V & KVM Mode Switcher** adalah utilitas otomatisasi sistem operasi Windows 10/11 yang dirancang khusus untuk mengatasi konflik virtualisasi antara **GNS3 VM (VMware Workstation)** dan **WSL2 / Docker Desktop**.

Pada laptop Windows modern (terutama Lenovo ThinkPad, Dell Latitude, HP EliteBook, atau Secured-Core PC), pengguna sering mengalami kegagalan saat menjalankan GNS3:
- Status layar biru GNS3 VM bertuliskan **`KVM support available: False`**.
- Muncul pesan error di VMware: *"Run without Intel VT-x?"* atau *"Feature 'hv.capable' was 0, but must be at least 0x1"*.
- Router Cisco vIOS, MikroTik, dan Linux appliance di GNS3 memakan CPU hingga 100% atau sangat lambat.

Masalah ini terjadi karena Windows Hypervisor dan Virtualization-Based Security (VBS) memonopoli kontrol virtualisasi hardware (Intel VT-x / AMD-V), sehingga VMware tidak dapat memberikan fitur *nested virtualization* (KVM) ke dalam VM.

**Hyper-V & KVM Mode Switcher** mengotomatiskan seluruh alur konfigurasi bootloader Windows (`bcdedit`), fitur Windows (`DISM`), dan script pelepasan gembok UEFI VBS melalui aplikasi GUI 1-klik yang mudah dan ramah pengguna.

---

### 📁 Struktur Repositori
```text
hyperv-kvm-switcher/
├── HyperV-KVM-Mode-Switcher.exe   # File aplikasi langsung pakai (Tanpa perlu install Python)
├── DG_Readiness_Tool_v3.6.ps1     # Script Remediasi UEFI VBS
├── DefaultWindows_*.xml / .p7b    # Berkas kebijakan pendukung DG Tool
├── app.py                         # Source code lengkap Python
├── README.md                      # Dokumentasi
└── LICENSE                        # Lisensi MIT
```

---

### 🎛️ Penjelasan Mode

| Nama Mode | Cara Kerja Sistem | Penggunaan |
| :--- | :--- | :--- |
| **`Hyper-V Inactive (for nested KVM in GNS3)`** | Mematikan Windows Hypervisor dan melepas proteksi UEFI VBS. Akses Intel VT-x diserahkan 100% ke VMware. | **GNS3 VM (`KVM: True`)**, Nested Virtualization VMware, Lab Jaringan L2/L3 Cisco vIOS/MikroTik berkecepatan tinggi. |
| **`Hyper-V Active (for enable WSL2, Docker, etc)`** | Mengaktifkan `VirtualMachinePlatform`, `WSL`, dan menyetel bootloader ke `auto`. | **WSL2 (Linux Environment)**, Docker Desktop, Kubernetes, Windows Sandbox. |

---

### 🚀 Cara Penggunaan (Langsung Pakai)

Pengguna tidak perlu menginstal Python atau melakukan kompilasi!

1. **Clone Repositori**:
   ```powershell
   git clone https://github.com/raihan2703/hyperv-kvm-switcher.git
   cd hyperv-kvm-switcher
   ```
2. **Jalankan Aplikasi Langsung**:
   - Klik dua kali **`HyperV-KVM-Mode-Switcher.exe`** langsung di dalam folder hasil clone.
   - Klik **Yes** pada konfirmasi Administrator (UAC).
3. **Pilih Mode**:
   - Status mode aktif Anda akan tampil di **Current Mode**.
   - Pilih mode tujuan pada menu **Switch to:**.
   - Klik tombol **OK**.
4. **Restart Komputer**:
   - Klik **Restart Now** pada dialog yang muncul.
   - *(Catatan: Saat beralih ke Mode GNS3 KVM pertama kali, tekan tombol **F3** atau **Windows Key** pada layar konfirmasi teks putih UEFI saat laptop booting).*
5. **Selesai!**
   - Setelah booting masuk Windows, GNS3 VM langsung berjalan dengan status **`KVM: True`** atau WSL2 dapat langsung digunakan.

---

### 🛠️ Opsi Tambahan: Menjalankan / Build dari Source Code (Developer)
Bagi pengguna yang ingin memodifikasi atau menjalankan source code Python:
```powershell
# Menjalankan langsung dari script Python
python app.py

# Atau build ulang file .exe
pip install pyinstaller
pyinstaller --noconsole --onefile --uac-admin --name "HyperV-KVM-Mode-Switcher" app.py
```

---

## 🔍 Search Keywords / Tags
`GNS3 KVM False Fix` • `GNS3 VMware Intel VT-x Error` • `GNS3 ThinkPad VBS Fix` • `WSL2 and GNS3 Coexistence` • `hypervisorlaunchtype switcher` • `Nested Virtualization Windows 11` • `Troubleshooting GNS3 VM` • `Device Guard Readiness Tool Automation`

---

## ⚖️ License
Released under the **[MIT License](LICENSE)**. Free for academic, personal, and commercial use.
