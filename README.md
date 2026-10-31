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

### ✨ Key Features
- **Accurate WMI & System Detection**: Automatically checks `VirtualizationBasedSecurityStatus` and bootloader settings to display real-time status.
- **Unified 1-Click Automation**: Eliminates manual terminal commands, registry tweaks, and feature toggling.
- **Smart Target Selection**: Pre-selects the opposite mode in the dropdown menu.
- **Self-Elevating Admin**: Automatically requests UAC Administrator privileges on launch.
- **Guided Reboot Flow**: Provides instant reboot prompts with built-in UEFI confirmation reminders.

---

### 🎛️ Modes Explained

| Mode | What it Does | Target Applications |
| :--- | :--- | :--- |
| **`Hyper-V Inactive (for nested KVM in GNS3)`** | Disables Windows Hypervisor & releases hardware VT-x locks via automated UEFI remediation. | **GNS3 VM with `KVM: True`**, VMware Workstation Nested Virtualization, Cisco vIOS / QEMU fast emulation. |
| **`Hyper-V Active (for enable WSL2, Docker, etc)`** | Enables `VirtualMachinePlatform`, `WSL`, and sets `bcdedit hypervisorlaunchtype auto`. | **WSL2 (Ubuntu/Debian)**, Docker Desktop, Kubernetes, Windows Sandbox. |

---

### 🚀 How to Use

1. **Download**:
   - Go to the **[Releases](../../releases)** page and download `HyperV-KVM-Mode-Switcher.exe` along with the helper scripts.
   - Or run directly from `dist/HyperV-KVM-Mode-Switcher.exe`.
2. **Launch**:
   - Double-click `HyperV-KVM-Mode-Switcher.exe` and allow the Administrator prompt (UAC).
3. **Switch Mode**:
   - The app will display your **Current Mode**.
   - Select your desired mode from the **Switch to:** dropdown.
   - Click **OK**.
4. **Reboot**:
   - When the dialog appears, click **Restart Now**.
   - *(Note: When switching to GNS3 KVM Mode for the first time, press **F3** or **Windows Key** on the UEFI boot screen to confirm VBS opt-out).*
5. **Done!**
   - Boot into Windows and launch either GNS3 (with `KVM: True`) or WSL2 with full performance.

---

### 🛠️ Build from Source
```powershell
# Clone the repository
git clone https://github.com/raihan2703/hyperv-kvm-switcher.git
cd hyperv-kvm-switcher

# Run source directly
python app.py

# Or compile single executable
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

### ✨ Fitur Utama
- **Deteksi Status Akurat (WMI & System State)**: Menampilkan status aktif saat ini secara presisi tanpa salah baca.
- **Otomatisasi Penuh 1-Klik**: Tidak perlu lagi membuka CMD, Registry Editor, atau menu *Turn Windows features on or off* secara manual.
- **Pemilihan Mode Cerdas**: Dropdown otomatis memilih mode sebaliknya untuk efisiensi pengguna.
- **Auto UAC Administrator**: Otomatis meminta izin Administrator saat aplikasi dibuka.
- **Dialog Restart Terpandu**: Menyediakan dialog konfirmasi restart cepat lengkap dengan petunjuk konfirmasi UEFI.

---

### 🎛️ Penjelasan Mode

| Nama Mode | Cara Kerja Sistem | Penggunaan |
| :--- | :--- | :--- |
| **`Hyper-V Inactive (for nested KVM in GNS3)`** | Mematikan Windows Hypervisor dan melepas proteksi UEFI VBS. Akses Intel VT-x diserahkan 100% ke VMware. | **GNS3 VM (`KVM: True`)**, Nested Virtualization VMware, Lab Jaringan L2/L3 Cisco vIOS/MikroTik berkecepatan tinggi. |
| **`Hyper-V Active (for enable WSL2, Docker, etc)`** | Mengaktifkan `VirtualMachinePlatform`, `WSL`, dan menyetel bootloader ke `auto`. | **WSL2 (Linux Environment)**, Docker Desktop, Kubernetes, Windows Sandbox. |

---

### 🚀 Cara Penggunaan

1. **Unduh File**:
   - Buka halaman **[Releases](../../releases)** dan unduh file `HyperV-KVM-Mode-Switcher.exe`.
   - Atau jalankan langsung dari folder `dist/HyperV-KVM-Mode-Switcher.exe`.
2. **Jalankan Aplikasi**:
   - Klik dua kali `HyperV-KVM-Mode-Switcher.exe` dan izinkan Administrator (UAC).
3. **Pilih Mode**:
   - Aplikasi akan menampilkan **Current Mode** Anda saat ini.
   - Pilih mode yang diinginkan pada dropdown **Switch to:**.
   - Klik tombol **OK**.
4. **Restart Komputer**:
   - Pada jendela pop-up, klik **Restart Now**.
   - *(Catatan: Saat beralih ke Mode GNS3 KVM pertama kali, tekan tombol **F3** atau **Windows Key** pada layar konfirmasi teks putih UEFI saat laptop booting).*
5. **Selesai!**
   - Setelah masuk Windows, buka GNS3 VM (KVM langsung bernilai **True**) atau nikmati WSL2 dengan performa optimal.

---

## 🔍 Search Keywords / Tags
`GNS3 KVM False Fix` • `GNS3 VMware Intel VT-x Error` • `GNS3 ThinkPad VBS Fix` • `WSL2 and GNS3 Coexistence` • `hypervisorlaunchtype switcher` • `Nested Virtualization Windows 11` • `Troubleshooting GNS3 VM` • `Device Guard Readiness Tool Automation`

---

## ⚖️ License
Released under the **[MIT License](LICENSE)**. Free for academic, personal, and commercial use.
