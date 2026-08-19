#!/bin/bash

echo "=========================================="
echo " Automated Synthetic Drillhole Generator"
echo "=========================================="

DATA_DIR="./raw_data"
OUTPUT_DIR="./output_database"

# Validasi keberadaan folder raw_data
if [ ! -d "$DATA_DIR" ]; then
    echo "[!] Error: Folder '$DATA_DIR' tidak ditemukan!"
    echo "[*] Buat folder 'raw_data' lalu masukkan file .tif dan .csv ke dalamnya."
    exit 1
fi

# Otomatis mendeteksi file DEM (.tif) dan Grid CSV (.csv)
DEM_FILE=$(find "$DATA_DIR" -name "*.tif" | head -n 1)
GRID_FILE=$(find "$DATA_DIR" -name "*.csv" | head -n 1)

if [ -z "$DEM_FILE" ] || [ -z "$GRID_FILE" ]; then
    echo "[!] Error: File DEM (.tif) atau Grid (.csv) tidak lengkap di dalam folder $DATA_DIR!"
    exit 1
fi

echo "[✔] File DEM terdeteksi  : $DEM_FILE"
echo "[✔] File Grid terdeteksi : $GRID_FILE"
echo "[*] Folder Output diset ke : $OUTPUT_DIR"
echo "------------------------------------------"

# Menjalankan mesin Python secara otomatis
python generate_drillholes.py \
    --dem "$DEM_FILE" \
    --grid "$GRID_FILE" \
    --output "$OUTPUT_DIR"

echo "=========================================="
echo " Pipeline Selesai! Cek folder: $OUTPUT_DIR"
echo "=========================================="