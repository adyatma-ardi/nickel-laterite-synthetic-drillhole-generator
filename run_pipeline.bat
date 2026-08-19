@echo off
rem ==========================================
rem Automated Synthetic Drillhole Generator
rem ==========================================

set "DATA_DIR=.\raw_data"
set "OUTPUT_DIR=.\output_database"

rem 1. Validasi keberadaan folder raw_data
if not exist "%DATA_DIR%" (
    echo [!] Error: Folder %DATA_DIR% tidak ditemukan!
    echo [*] Buat folder raw_data lalu masukkan file .tif dan .csv ke dalamnya.
    goto :end
)

rem 2. Otomatis mendeteksi file DEM (.tif) dan Grid CSV (.csv)
set "DEM_FILE="
set "GRID_FILE="

for %%F in ("%DATA_DIR%\*.tif") do (
    set "DEM_FILE=%%F"
    goto :find_csv
)

:find_csv
for %%F in ("%DATA_DIR%\*.csv") do (
    set "GRID_FILE=%%F"
    goto :check_files
)

:check_files
if "%DEM_FILE%"=="" (
    echo [!] Error: File DEM ^(.tif^) tidak ditemukan di dalam folder %DATA_DIR%!
    goto :end
)

if "%GRID_FILE%"=="" (
    echo [!] Error: File Grid ^(.csv^) tidak ditemukan di dalam folder %DATA_DIR%!
    goto :end
)

echo [v] File DEM terdeteksi : %DEM_FILE%
echo [v] File Grid terdeteksi : %GRID_FILE%
echo [*] Folder Output diset ke : %OUTPUT_DIR%
echo ------------------------------------------

rem 3. Otomatis menginstal library yang kurang jika diperlukan
echo [*] Memeriksa environment dan library Python...
python -c "import pandas, rasterio, numpy" 2>nul
if %errorlevel% neq 0 (
    echo [!] Library pendukung belum lengkap. Menginstal pandas, numpy, dan rasterio...
    pip install pandas numpy rasterio
    echo ------------------------------------------
)

rem 4. Menjalankan mesin Python secara otomatis
echo [*] Menjalankan pemrosesan data...
python generate_drillholes.py --dem "%DEM_FILE%" --grid "%GRID_FILE%" --output "%OUTPUT_DIR%"

echo ==========================================
echo Pipeline Selesai! Cek folder: %OUTPUT_DIR%
echo ==========================================

:end
pause
