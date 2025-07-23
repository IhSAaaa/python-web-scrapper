# 🧹 Quick Cleanup Guide

## Overview
Folder-folder di dalam path `output` sekarang otomatis dihapus setelah digunakan untuk menghemat ruang disk.

## 🚀 Fitur Otomatis

### Auto-Cleanup Setelah Download
- ✅ Folder session dihapus otomatis setelah file di-download
- ✅ Berlaku untuk CSV, Images ZIP, dan file individual
- ✅ Delay 1 detik untuk memastikan download selesai

### Scheduled Cleanup
- ✅ Cleanup otomatis saat aplikasi startup
- ✅ Cleanup folder yang lebih tua dari 1 jam (default)

## 🛠️ Manual Cleanup

### Menggunakan Script
```bash
# Cek statistik
./cleanup_manual.sh stats

# List semua session
./cleanup_manual.sh list

# Cleanup session lama (default: 1 jam)
./cleanup_manual.sh old

# Cleanup session lama (24 jam)
./cleanup_manual.sh old 24

# Cleanup semua session
./cleanup_manual.sh all

# Cleanup session tertentu
./cleanup_manual.sh specific <session_id>
```

### Menggunakan cURL
```bash
# Cek stats
curl -X GET http://localhost:8001/api/maintenance/stats

# Cleanup session lama
curl -X POST "http://localhost:8001/api/maintenance/cleanup?older_than_hours=1"

# Cleanup semua
curl -X POST http://localhost:8001/api/maintenance/cleanup-all

# Cleanup session tertentu
curl -X POST http://localhost:8001/api/maintenance/cleanup/<session_id>
```

## 🧪 Testing
```bash
# Jalankan test cleanup
python test_cleanup.py
```

## ⚙️ Konfigurasi
Edit `backend/main.py` untuk mengubah pengaturan:
```python
AUTO_CLEANUP_ENABLED = True          # Enable/disable auto-cleanup
CLEANUP_AFTER_DOWNLOAD = True        # Delete folder setelah download
DEFAULT_CLEANUP_HOURS = 1           # Usia folder untuk cleanup (jam)
```

## 📊 Monitoring
```bash
# Cek log cleanup
tail -f logs/web_scraper.log | grep -i cleanup

# Cek ukuran folder output
du -sh output/*

# Cek health dengan info disk
curl -X GET http://localhost:8001/api/health
```

## 🚨 Troubleshooting

### Folder Tidak Terhapus
1. Cek log untuk error: `tail -f logs/web_scraper.log`
2. Pastikan `CLEANUP_AFTER_DOWNLOAD = True`
3. Test manual: `./cleanup_manual.sh specific <session_id>`

### Cleanup Terlalu Agresif
1. Ubah `DEFAULT_CLEANUP_HOURS` ke nilai lebih besar (misal: 24)
2. Disable auto-cleanup jika diperlukan

### Permission Error
1. Pastikan file tidak sedang di-download
2. Cek permission folder output
3. Restart aplikasi jika diperlukan

## 📈 Metrics
- Jumlah session yang di-cleanup
- Total ukuran yang dibebaskan
- Waktu rata-rata cleanup process
- Error rate dalam cleanup

## 🎯 Kesimpulan
Sistem cleanup otomatis menjaga folder output tetap bersih dan efisien. Folder session dihapus setelah digunakan, menghemat ruang disk secara otomatis. 