<div align="center">

<img src="docs/brand.svg" alt="Chromium Railway" width="84" height="84">

<h1>Chromium Railway</h1>

<p><a href="https://github.com/DURIAN-ORGANISASI/chromium-railway/actions/workflows/validate.yml"><img alt="Validation workflow configured; see Actions for live status" src="https://img.shields.io/badge/validation-configured-2088FF?logo=githubactions&amp;logoColor=white"></a> <a href="LICENSE"><img alt="Project license: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a> <img alt="Railway" src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?logo=railway&amp;logoColor=white"> <img alt="Docker" src="https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&amp;logoColor=white"> <img alt="Chromium" src="https://img.shields.io/badge/Browser-Chromium-4285F4?logo=googlechrome&amp;logoColor=white"></p>

<p><a href="README.md">🇮🇩 Bahasa Indonesia</a> · <a href="README.en.md">🇬🇧 English</a></p>

<p><strong>Jalankan Chromium Desktop di Railway dan akses melalui browser.</strong><br>
Dilengkapi login username/password dan profil browser sementara di filesystem container.</p>

<p><a href="docs/DEPLOY-RAILWAY.md">📘 Panduan deploy Railway</a> · <a href="#fitur">Fitur</a> · <a href="#variables-railway">Variables</a> · <a href="#deploy-ke-railway">Deploy</a> · <a href="#keamanan">Keamanan</a> · <a href="#sumber-atribusi-dan-lisensi">Sumber &amp; lisensi</a></p>

</div>

![Chromium Railway overview](docs/hero.id.svg)
<p align="center"><sub>Ilustrasi dokumentasi — bukan screenshot resmi Chromium atau Railway.</sub></p>

> [!IMPORTANT]
> **Repository ini menjalankan Chromium Desktop dengan tampilan visual.** Buka domain Railway, masukkan username dan password, lalu kendalikan browser langsung dari tab browser milikmu. Ini adalah browser desktop visual, bukan browser headless; tidak membutuhkan service tambahan.

> [!WARNING]
> Browser jarak jauh memberi pemegang kredensial akses ke sesi browser, cookie, akun yang sedang login, serta file profil. Gunakan password yang unik dan kuat. Railway menyediakan HTTPS untuk domain publik; jangan membagikan URL dan kredensial kepada orang lain.

## Ringkasan

Chromium berjalan di satu Docker service Railway. Antarmuka desktop dikirim ke browser melalui web client Selkies. Profil browser disimpan pada filesystem biasa container di `/config`, tanpa Railway Volume. Bookmark, ekstensi, cookies, pengaturan, dan file tetap tersedia selama container yang sama berjalan, tetapi akan hilang ketika container dibuat ulang atau deployment diganti.

| Komponen | Konfigurasi |
| --- | --- |
| Browser | Chromium Desktop |
| Image dasar | `lscr.io/linuxserver/chromium:7b8e918f-ls63 (pinned digest)` |
| Port internal | `3000` |
| Akses | Domain HTTPS Railway |
| Login | `CUSTOM_USER` + `PASSWORD` |
| Browser profile | Filesystem container sementara pada `/config` |
| Service tambahan | Tidak diperlukan |

## Fitur

- **Startup kompatibel dengan Railway:** wrapper khusus menjalankan service tree s6 tanpa memanggil `/init` sebagai PID 1, sehingga menghindari error `s6-overlay-suexec: fatal: can only run as pid 1`.
- **Login sebelum browser dibuka:** Nginx selalu meminta `CUSTOM_USER` dan `PASSWORD`; password di-hash dan tidak diteruskan ke environment proses desktop.
- **Health check:** endpoint internal `/healthz` tersedia untuk pemeriksaan deployment Railway.
- **Default ringan untuk Railway 1 GB:** desktop dikunci pada 1280×720 dan 30 FPS agar browser tidak dibebani stream software 1920-piksel / 60 FPS.

- **Chromium Desktop:** browser lengkap dengan tampilan visual, bukan mode headless.
- **Akses dari mana saja:** buka domain Railway lewat Chrome, Edge, Firefox, atau browser modern lainnya.
- **Login username/password:** akses web browser dilindungi HTTP Basic Authentication.
- **Profil sementara tanpa Volume:** bookmark, cookies, ekstensi, riwayat, pengaturan, dan file disimpan langsung di filesystem container pada `/config`.
- **Keyboard, mouse, dan clipboard:** kendalikan Chromium dari desktop atau perangkat seluler.
- **Upload/download file:** gunakan panel Selkies bila fitur file transfer diaktifkan.
- **Mode desktop lebih aman:** `HARDEN_DESKTOP=true` menonaktifkan terminal dan sudo di desktop session.
- **Satu service:** tidak memerlukan database, Redis, atau API key.

## Variables Railway

Buka **Railway → Chromium → Variables**. Salin blok berikut, lalu ganti username dan password contoh:

```dotenv
CUSTOM_USER=chromium
PASSWORD=GANTI_DENGAN_PASSWORD_UNIK_MINIMAL_12_KARAKTER
PORT=3000
TZ=Asia/Jakarta
HARDEN_DESKTOP=true
RAILWAY_SHM_SIZE_BYTES=1073741824
```

| Variable | Wajib | Fungsi |
| --- | --- | --- |
| `CUSTOM_USER` | Ya | Username untuk login ke halaman Chromium. Gunakan huruf, angka, titik, garis bawah, `@`, atau tanda hubung. |
| `PASSWORD` | Ya | Password untuk login. Gunakan minimal 12 karakter dan password unik. |
| `PORT` | Ya | Port internal web desktop. Biarkan `3000`. |
| `TZ` | Opsional | Zona waktu container. Default `Asia/Jakarta`. |
| `HARDEN_DESKTOP` | Opsional | `true` menonaktifkan terminal dan sudo pada desktop session. Default `true` pada Dockerfile. |
| `RAILWAY_SHM_SIZE_BYTES` | Disarankan | Shared memory container dalam byte. `1073741824` = 1 GiB. |

**Catatan username:** gunakan format yang didukung image, yaitu huruf/angka serta `.`, `_`, `@`, dan `-`. Contoh: `akun.durian` atau `chromium_admin`.

**Jangan gunakan password contoh.** Buat password sendiri yang panjang dan unik. Jangan menyimpan kredensial sungguhan di GitHub, README, screenshot publik, atau file commit.

## Deploy ke Railway

### 1. Upload repository ke GitHub

1. Buat repository baru, misalnya `DURIAN-ORGANISASI/chromium-railway`.
2. Upload seluruh isi ZIP repository ini ke branch `main`.
3. Pastikan `Dockerfile` berada di root repository.

### 2. Buat service Railway

1. Buka Railway dan buat project baru atau pilih project yang ingin digunakan.
2. Pilih **New → GitHub Repo**.
3. Hubungkan repository `chromium-railway`.
4. Biarkan **Root Directory** kosong.
5. Pastikan Railway menggunakan Dockerfile di root.
6. Beri nama service `chromium`.

### 3. Tempel Variables

Buka service Chromium → **Variables** → **RAW Editor**, kemudian tempel:

```dotenv
CUSTOM_USER=chromium
PASSWORD=GANTI_DENGAN_PASSWORD_UNIK_MINIMAL_12_KARAKTER
PORT=3000
TZ=Asia/Jakarta
HARDEN_DESKTOP=true
RAILWAY_SHM_SIZE_BYTES=1073741824
```

Ganti nilai `CUSTOM_USER` dan `PASSWORD` sesuai keinginan. Klik deploy/redeploy setelah menyimpan Variables.

### 4. Gunakan filesystem container biasa

Tidak perlu membuat Railway Volume dan jangan memasang storage pada `/config`. Chromium otomatis memakai direktori `/config` di filesystem container. Profil browser bersifat sementara dan akan kembali kosong ketika container dibuat ulang atau deployment diganti.

### 5. Atur Networking

1. Buka **Settings → Networking** pada service Chromium.
2. Pilih **Generate Domain**.
3. Pastikan target port domain adalah `3000`.
4. Simpan pengaturan dan tunggu deployment aktif.

Railway menangani HTTPS untuk domain yang dibuat melalui Networking. Aplikasi Chromium di container menerima traffic pada port internal `3000`.

### 6. Login ke Chromium

1. Buka domain Railway yang sudah dibuat.
2. Browser akan menampilkan dialog login.
3. Masukkan `CUSTOM_USER` sebagai username.
4. Masukkan `PASSWORD` sebagai password.
5. Setelah berhasil, desktop Chromium akan tampil di halaman tersebut.

Kamu dapat membuka situs, membuat bookmark, memasang ekstensi, login akun website, serta menggunakan menu samping untuk keyboard, clipboard, dan file transfer.

## Arsitektur

![Chromium Railway architecture](docs/architecture.svg)

| Path | Fungsi |
| --- | --- |
| `Dockerfile` | Image LinuxServer Chromium yang dipatok digest dan entry point khusus Railway. |
| `services/browser/railway-start.sh` | Menyiapkan autentikasi dan menjalankan service s6 tanpa konflik PID 1. |
| `services/browser/patch-image.sh` | Mengaktifkan autentikasi Nginx, proteksi Origin, header keamanan, dan `/healthz` saat build. |
| `services/browser/pkg-restore.sh` | Memulihkan paket tambahan yang diminta melalui Variables. |
| `docker-compose.yml` | Menjalankan Chromium secara lokal untuk pengujian. |
| `.env.example` | Template Variables lokal tanpa password aktif. |
| `docs/DEPLOY-RAILWAY.md` | Panduan deploy langkah demi langkah. |
| `docs/SOURCES.md` | Referensi upstream, atribusi, dan lisensi. |
| `SECURITY.md` | Kebijakan keamanan dan cara menjaga kredensial. |
| `scripts/validate_repo.py` | Pemeriksaan struktur dokumentasi dan konfigurasi repo. |

## Menjalankan secara lokal dengan Docker

Pastikan Docker Desktop atau Docker Engine sudah aktif. Kemudian jalankan:

```bash
cp .env.example .env
```

Edit `.env`, ganti `PASSWORD`, lalu jalankan:

```bash
docker compose up -d --build
```

Buka `http://localhost:3000`, lalu login menggunakan username dan password dari `.env`. Profil browser disimpan di filesystem container pada `/config`; data ini tidak persisten dan hilang saat container dibuat ulang.

## Troubleshooting

| Masalah | Pemeriksaan |
| --- | --- |
| Domain tidak terbuka | Periksa status deployment dan target port `3000` pada Networking. |
| Dialog login terus muncul | Pastikan `CUSTOM_USER` dan `PASSWORD` pada Variables benar, lalu redeploy. |
| Browser tampil kosong | Tunggu sesi desktop siap, lalu refresh halaman. Periksa Deploy Logs jika tetap kosong. |
| Browser sering crash | Mulai dengan satu tab, sediakan RAM service yang memadai, dan pertahankan shared memory `1 GiB`. |
| Bookmark/cookies hilang setelah redeploy | Ini normal tanpa Volume. Browser memakai filesystem container sementara, sehingga profil tidak dipertahankan ketika container dibuat ulang. |
| Upload/download tidak muncul | Buka menu samping Selkies dan periksa apakah file transfer diaktifkan oleh konfigurasi image. |
| Website lambat | Rendering memakai CPU, bukan GPU. WebGL, game 3D, dan video beresolusi tinggi dapat lebih lambat. |

## Keamanan

- Gunakan password unik minimal 12 karakter; lebih panjang lebih baik.
- Jangan bagikan domain, username, password, atau sesi browser.
- Akses browser melalui domain HTTPS Railway, bukan HTTP publik yang tidak terenkripsi.
- Biarkan `HARDEN_DESKTOP=true` agar terminal dan sudo desktop session dinonaktifkan.
- Browser menyimpan cookies, sesi login, dan password website di `/config`. Data berada di filesystem container sementara, bukan storage persisten.
- Jangan login ke akun penting dari perangkat bersama tanpa menghapus sesi setelah selesai.
- Hindari mengunduh atau membuka file yang tidak dipercaya. Siapa pun yang berhasil login dapat mengontrol browser.
- `CUSTOM_USER` dan `PASSWORD` merupakan satu lapisan autentikasi dasar, bukan sistem multi-user atau SSO. Untuk akses organisasi, tambahkan gateway autentikasi seperti Cloudflare Access di depan domain.

Baca [SECURITY.md](SECURITY.md) untuk panduan lebih lengkap.

## Pengembangan dan validasi

Jalankan pemeriksaan lokal:

```bash
python scripts/validate_repo.py
```

GitHub Actions memeriksa dokumentasi, struktur file, JSON, dan SVG saat push atau pull request. Workflow validasi bukan pengujian live terhadap server Railway atau seluruh fungsi browser.

## Sumber, atribusi, dan lisensi

Lihat [`docs/SOURCES.md`](docs/SOURCES.md) untuk sumber resmi, atribusi, serta batas lisensi.

- **Dokumentasi, artwork, dan materi orisinal:** MIT, lihat [`LICENSE`](LICENSE).
- **Dockerfile integrasi dan kode kompatibilitas Railway di `services/browser/`:** GPL-3.0-or-later, lihat [`LICENSES/GPL-3.0-or-later.txt`](LICENSES/GPL-3.0-or-later.txt) dan [`NOTICE.md`](NOTICE.md).
- **Image Chromium:** menggunakan image komunitas `lscr.io/linuxserver/chromium:7b8e918f-ls63 (pinned digest)`, yang dibuat berdasarkan ekosistem LinuxServer Chromium/Selkies. Image dan seluruh komponennya tetap mengikuti lisensi masing-masing.
- **Chromium dan dependency:** memiliki lisensi serta pemberitahuan pihak ketiga sendiri. Lisensi repository ini tidak mengubah lisensi upstream.
- **Pihak ketiga:** Railway, Docker, LinuxServer, Selkies, Chromium, dan penyedia image mengikuti ketentuan masing-masing.

Proyek ini independen dan tidak berafiliasi dengan atau didukung secara resmi oleh Chromium, Google, LinuxServer.io, Selkies, atau Railway.

## Kontribusi

Bug report dan pull request dipersilakan. Baca [`CONTRIBUTING.md`](CONTRIBUTING.md). Jangan menyertakan password, browser cookies, file `.env`, atau data pribadi dalam issue dan commit.
