# ⚡ Hyper-V & KVM Mode Switcher

> **The Ultimate Fix for "Run without Intel VT-x" & `KVM support available: False` on GNS3 VM (Windows 11 / ThinkPad / Secured-Core PC)**  
> Seamlessly toggle between **WSL2 / Docker Mode** and **GNS3 Nested KVM Mode** with a single click.

---

## 🚀 Tagline & Mengapa Repositori Ini Dibuat?

Apakah Anda pengguna **Windows 10/11 (terutama ThinkPad, Dell Latitude, HP EliteBook, atau Secured-Core PC lainnya)** yang mengalami kendala berikut saat menyiapkan **GNS3 VM di VMware Workstation**?
- ❌ Muncul error: *"Run without Intel VT-x?"* atau *"Feature 'hv.capable' was 0, but must be at least 0x1"*.
- ❌ Di layar biru GNS3 VM statusnya tetap **`KVM support available: False`**, sehingga router QEMU/Cisco memakan CPU 100% atau gagal boot.
- ❌ Anda ingin belajar **Jaringan (GNS3)** dengan akselerasi penuh, tetapi tidak ingin kehilangan akses ke **WSL2 / Docker Desktop** untuk coding.

**Repositori ini menyediakan solusi ganda:**
1. **Panduan Lengkap & Tuntas (Ultimate Troubleshooting Guide)** untuk menjebol proteksi VBS/Hyper-V Windows hingga KVM bernilai **`True`**.
2. **Aplikasi Desktop GUI (HyperV-KVM-Switcher.exe)** untuk beralih mode secara instan tanpa perlu repot mengetik perintah terminal setiap hari.

---

## 🛠️ PANDUAN LENGKAP: Memperbaiki KVM Support Available: False di GNS3 VM

Jika Anda baru pertama kali menginstal GNS3 VM di VMware dan KVM masih `False`, ikuti tahapan berikut secara berurutan.

---

### Tahap 1: Konfigurasi Virtual Machine (VMware Workstation)
1. Matikan GNS3 VM terlebih dahulu.
2. Klik kanan **GNS3 VM** di VMware $\rightarrow$ **Settings** $\rightarrow$ tab **Hardware** $\rightarrow$ **Processors**.
3. Atur prosesor:
   - **Number of processors**: `1`
   - **Number of cores per processor**: `4` (atau sesuai spesifikasi laptop)
4. Pada bagian **Virtualization engine**, **CENTANG (Check)**:
   - [x] **Virtualize Intel VT-x/EPT or AMD-V/RVI**
5. Klik **OK**.

---

### Tahap 2: Nonaktifkan Fitur Hyper-V & Virtual Machine Platform di Windows
1. Tekan tombol `Windows + S`, ketik **Turn Windows features on or off**, lalu tekan Enter.
2. Cari dan **HAPUS CENTANG (Uncheck)** pada fitur-fitur berikut:
   - [ ] **Hyper-V** (semua sub-itemnya)
   - [ ] **Virtual Machine Platform**
   - [ ] **Windows Hypervisor Platform**
   - [ ] **Windows Sandbox**
3. Klik **OK**, tunggu Windows memproses perubahan (tunda restart sampai tahap berikutnya).

---

### Tahap 3: Nonaktifkan Core Isolation (Memory Integrity)
1. Buka Start Menu Windows $\rightarrow$ ketik **Core Isolation** (atau **Isolasi Inti**).
2. Cari opsi **Memory Integrity (Integritas Memori)**.
3. Ubah sakelar menjadi **OFF (Nonaktif)**.

---

### Tahap 4: Nonaktifkan Device Guard & Credential Guard via Registry & BCD
Buka **Command Prompt (Run as Administrator)** dan jalankan perintah berikut:

```cmd
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "LsaCfgFlags" /t REG_DWORD /d 0 /f
bcdedit /set hypervisorlaunchtype off
```

---

### Tahap 5: Solusi Pamungkas UEFI — Device Guard Readiness Tool (Firmware Remediation)

> **KASUS UMUM (Terutama Lenovo ThinkPad / Windows 11 Enterprise/Pro):**  
> Seringkali setelah melakukan Tahap 1–4, saat mengecek di `msinfo32`, baris **Virtualization-based security (VBS)** masih berstatus **Running**. Ini karena Windows mengunci VBS langsung di firmware UEFI.

Untuk menjebol proteksi UEFI ini secara tuntas menggunakan tool resmi Microsoft:

#### 1. Siapkan File `DG_Readiness_Tool_v3.6.ps1`
* File script resmi Microsoft ini sudah kami sediakan di repositori ini. Silakan unduh file `DG_Readiness_Tool_v3.6.ps1` (atau ekstrak dari folder repositori).

#### 2. Jalankan Script via PowerShell (Administrator)
1. Buka folder tempat file script berada.
2. Buka **PowerShell (Run as Administrator)** di folder tersebut.
3. Jalankan perintah eksekusi dengan bypass policy dan parameter remediation:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\DG_Readiness_Tool_v3.6.ps1 -Disable -ReadyForRemediation
   ```
4. Tunggu proses berjalan (memakan waktu sekitar 1–3 menit). Script akan menonaktifkan Device Guard, Credential Guard, dan menyiapkan instruksi pelepasan gembok di UEFI.
5. Abaikan jika ada pesan peringatan file tidak ditemukan (`SIPolicy.p7b not found`), itu hal yang normal.

#### 3. Restart & Konfirmasi Layar Khusus UEFI
1. Lakukan **Restart Laptop**.
2. **PERHATIKAN LAYAR SAAT BOOTING:** Sebelum logo Windows muncul, firmware UEFI akan menampilkan layar konfirmasi teks putih:
   > *"A request to opt-out of Virtualization Based Security was received..."*  
   > *"Press **F3** (atau Windows Key) to confirm."*
3. **Tekan tombol konfirmasi tersebut** (misalnya tombol **F3** atau **Windows Key** pada ThinkPad).

#### 4. Penanganan Reset PIN Windows Hello (PENTING!)
> [!IMPORTANT]
> **Mengapa Windows meminta Reset PIN setelah booting?**  
> Karena proteksi Credential Guard (LSAIso) pada TPM firmware telah dilepas, Windows menganggap ada perubahan konfigurasi keamanan dan meminta Anda memverifikasi akun Anda kembali.  
> 👉 **Lakukan saja proses Reset PIN tersebut!** Ikuti verifikasi email/password akun Microsoft Anda dan buat PIN baru. **Data, file, dan sistem Anda 100% AMAN dan tidak akan ada yang hilang.**

---

### Tahap 6: Verifikasi Hasil — KVM SUDAH TRUE! 🎉
1. Buka kembali aplikasi **VMware Workstation Pro**.
2. Nyalakan **GNS3 VM**.
3. Perhatikan layar birunya:
   ```text
   KVM support available: True
   ```
4. Selamat! Sekarang router Cisco vIOS, MikroTik CHR, dan Linux appliances di GNS3 akan berjalan sangat kencang menggunakan akselerasi hardware penuh tanpa membebani CPU!

> [!NOTE]
> **Tahap 1 s/d 5 di atas HANYA PERLU DILAKUKAN SEKALI SEUMUR HIDUP.** Kunci hardware UEFI laptop Anda sudah resmi terbuka secara permanen.

---

## 🎛️ Hyper-V & KVM Switcher (.exe)

Setelah KVM berhasil menjadi **True**, bagaimana jika suatu hari Anda ingin kembali mengerjakan tugas kuliah menggunakan **WSL2** atau **Docker Desktop**, lalu ingin kembali lagi ke **GNS3**?

Anda **TIDAK PERLU** mengulang script yang panjang di atas! Anda hanya perlu mengubah nilai `hypervisorlaunchtype`.

Untuk mempermudah hal tersebut, kami membuatkan aplikasi GUI modern: **`HyperV-KVM-Switcher.exe`**.

![Hyper-V Switcher GUI Preview](preview.png)

### Pilihan Mode di Aplikasi:
- **`Hyper-V Active (for enable WSL2, Docker, etc)`**  
  Mengaktifkan Windows Hypervisor (`bcdedit /set hypervisorlaunchtype auto`). Gunakan saat ingin coding dengan WSL2, Docker Desktop, atau Windows Sandbox.
- **`Hyper-V Inactive (for nested KVM in GNS3)`**  
  Menidurkan Windows Hypervisor (`bcdedit /set hypervisorlaunchtype off`). Menyerahkan akses Intel VT-x penuh ke VMware sehingga GNS3 VM mendapatkan status **`KVM: True`**.

### Fitur Aplikasi:
- 🔍 **Auto-Detect Status**: Otomatis mendeteksi status bootloader Windows saat ini.
- ⚡ **1-Click Smart Selection**: Dropdown otomatis memilih mode lawanannya.
- 🛡️ **Auto UAC Administrator**: Meminta izin administrator secara otomatis saat dibuka.
- 🔄 **Restart Dialog Confirmation**:
  - **Restart Now**: Langsung me-reboot komputer agar mode baru aktif seketika.
  - **Cancel, Restart Later**: Menyimpan setelan mode tanpa me-restart saat itu juga.

---

## 📦 Cara Menjalankan Switcher

### Download File Executable Langsung:
1. Masuk ke tab **[Releases](../../releases)** di repositori ini.
2. Unduh file **`HyperV-KVM-Switcher.exe`**.
3. Jalankan aplikasinya (Klik dua kali $\rightarrow$ pilih mode $\rightarrow$ klik **OK**).

### Atau Jalankan dari Source Python:
```powershell
python app.py
```

### Build ke .exe Sendiri:
```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --uac-admin --name "HyperV-KVM-Switcher" app.py
```

---

## ⚖️ License & Attribution
- Tooling powered by Microsoft Device Guard and Credential Guard Hardware Readiness Tool.
- Switcher App released under the **MIT License**. Free to use, modify, and distribute.
