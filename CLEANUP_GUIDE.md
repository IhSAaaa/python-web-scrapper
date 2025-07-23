# 🧹 Cleanup Guide - Web Scraper

## Overview
Sistem web scraper sekarang memiliki fitur cleanup otomatis yang menghapus folder-folder session di dalam path output setelah digunakan. Ini membantu menghemat ruang disk dan menjaga sistem tetap bersih.

## 🚀 Fitur Cleanup

### 1. **Auto-Cleanup Setelah Download** ✅
- Folder session otomatis dihapus setelah file di-download
- Berlaku untuk semua jenis download: CSV, Images ZIP, dan file individual
- Delay 1 detik setelah response dikirim untuk memastikan download selesai

### 2. **Scheduled Cleanup** ⏰
- Cleanup otomatis saat aplikasi startup
- Cleanup berkala untuk folder yang lebih tua dari 1 jam (default)
- Konfigurasi waktu cleanup yang dapat disesuaikan

### 3. **Manual Cleanup** 🛠️
- Endpoint untuk menghapus session tertentu
- Endpoint untuk menghapus semua session
- Endpoint untuk cleanup berdasarkan usia folder

## 📋 Endpoint Cleanup

### 1. **Cleanup Session Tertentu**
```bash
POST /api/maintenance/cleanup/{session_id}
```
**Response:**
```json
{
  "message": "Session abc123 cleaned up successfully",
  "session_id": "abc123",
  "size_freed_mb": 2.5
}
```

### 2. **Cleanup Session Lama**
```bash
POST /api/maintenance/cleanup?older_than_hours=1
```
**Response:**
```json
{
  "message": "Cleanup completed",
  "cleaned_sessions": 3,
  "total_size_freed_mb": 15.2,
  "cutoff_time": "2024-01-15T10:00:00",
  "older_than_hours": 1
}
```

### 3. **Cleanup Semua Session**
```bash
POST /api/maintenance/cleanup-all
```
**Response:**
```json
{
  "message": "All sessions cleaned up",
  "cleaned_sessions": 5,
  "total_size_freed_mb": 25.8
}
```

### 4. **Statistik Maintenance**
```bash
GET /api/maintenance/stats
```
**Response:**
```json
{
  "total_sessions": 2,
  "total_files": 8,
  "total_size_mb": 12.5,
  "output_dir": "output"
}
```

## ⚙️ Konfigurasi

### Environment Variables
```python
# Cleanup configuration
AUTO_CLEANUP_ENABLED = True          # Enable/disable auto-cleanup
CLEANUP_AFTER_DOWNLOAD = True        # Delete folder after download
DEFAULT_CLEANUP_HOURS = 1           # Default cleanup age (hours)
AUTO_CLEANUP_INTERVAL = 3600        # Auto-cleanup interval (seconds)
```

### Mengubah Konfigurasi
Untuk mengubah konfigurasi, edit file `backend/main.py`:

```python
# Cleanup configuration
AUTO_CLEANUP_ENABLED = True          # Set False untuk disable
CLEANUP_AFTER_DOWNLOAD = True        # Set False untuk disable auto-cleanup setelah download
DEFAULT_CLEANUP_HOURS = 24          # Ubah ke 24 jam untuk cleanup yang kurang agresif
AUTO_CLEANUP_INTERVAL = 7200        # Ubah ke 2 jam untuk interval yang lebih lama
```

## 🧪 Testing Cleanup

### Menjalankan Test Script
```bash
python test_cleanup.py
```

### Test Manual dengan cURL
```bash
# Test maintenance stats
curl -X GET http://localhost:8001/api/maintenance/stats

# Test cleanup session tertentu
curl -X POST http://localhost:8001/api/maintenance/cleanup/your-session-id

# Test cleanup session lama
curl -X POST "http://localhost:8001/api/maintenance/cleanup?older_than_hours=1"

# Test cleanup semua session
curl -X POST http://localhost:8001/api/maintenance/cleanup-all
```

## 📊 Monitoring Cleanup

### Log Cleanup Activity
Semua aktivitas cleanup dicatat dalam log:
```
2024-01-15 10:30:15 | INFO | Cleaned up session folder: abc123 | Reason: download-complete | Size: 2048576 bytes
2024-01-15 10:30:16 | INFO | Auto-cleanup completed: 2 sessions removed, 4097152 bytes freed
```

### Health Check dengan Cleanup Info
```bash
curl -X GET http://localhost:8001/api/health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "system_info": {
    "memory_usage_percent": 45.2,
    "disk_usage_percent": 23.1,
    "output_dir_size_mb": 125.5
  }
}
```

## 🔧 Troubleshooting

### Masalah Umum

#### 1. **Folder Tidak Terhapus Setelah Download**
**Penyebab:** Auto-cleanup disabled atau error dalam cleanup process
**Solusi:**
- Cek log untuk error messages
- Pastikan `CLEANUP_AFTER_DOWNLOAD = True`
- Test manual cleanup dengan endpoint

#### 2. **Cleanup Terlalu Agresif**
**Penyebab:** `DEFAULT_CLEANUP_HOURS` terlalu kecil
**Solusi:**
- Ubah ke nilai yang lebih besar (misal: 24 jam)
- Disable auto-cleanup jika diperlukan

#### 3. **Permission Error**
**Penyebab:** File sedang digunakan atau permission tidak cukup
**Solusi:**
- Pastikan file tidak sedang di-download
- Cek permission folder output
- Restart aplikasi jika diperlukan

### Debug Cleanup
```bash
# Cek log cleanup
tail -f logs/web_scraper.log | grep -i cleanup

# Cek status folder output
ls -la output/

# Cek ukuran folder
du -sh output/*
```

## 🚨 Best Practices

### 1. **Monitoring Disk Usage**
- Monitor ukuran folder output secara berkala
- Set alert untuk disk usage yang tinggi
- Review dan adjust cleanup settings sesuai kebutuhan

### 2. **Backup Penting**
- Backup data penting sebelum cleanup
- Test cleanup di environment development dulu
- Dokumentasikan session yang penting

### 3. **Performance Optimization**
- Set `DEFAULT_CLEANUP_HOURS` sesuai dengan pola penggunaan
- Monitor memory usage selama cleanup process
- Pertimbangkan cleanup manual untuk session besar

## 📈 Metrics dan Analytics

### Cleanup Metrics
- Jumlah session yang di-cleanup
- Total ukuran yang dibebaskan
- Waktu rata-rata cleanup process
- Error rate dalam cleanup

### Monitoring Dashboard
```bash
# Get comprehensive stats
curl -X GET http://localhost:8001/api/maintenance/stats

# Get health info
curl -X GET http://localhost:8001/api/health

# Get last session info
curl -X GET http://localhost:8001/api/debug/last-session
```

## 🔄 Workflow Cleanup

### Normal Workflow
1. User melakukan scraping → Session folder dibuat
2. User download file → Auto-cleanup di-schedule
3. File download selesai → Session folder dihapus
4. Scheduled cleanup berjalan setiap jam → Hapus folder lama

### Manual Workflow
1. Admin cek maintenance stats
2. Admin jalankan manual cleanup jika diperlukan
3. Admin monitor hasil cleanup
4. Admin adjust settings jika diperlukan

## 🎯 Kesimpulan

Sistem cleanup yang baru memberikan:
- ✅ **Otomatis**: Folder dihapus setelah digunakan
- ✅ **Efisien**: Menghemat ruang disk secara otomatis
- ✅ **Fleksibel**: Konfigurasi yang dapat disesuaikan
- ✅ **Aman**: Cleanup dengan delay dan error handling
- ✅ **Monitorable**: Logging dan metrics yang lengkap

Dengan fitur ini, folder-folder di dalam path output akan otomatis dihapus setelah digunakan, menjaga sistem tetap bersih dan efisien. 