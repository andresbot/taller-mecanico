@echo off
setlocal

REM Build ejecutable Windows con PyInstaller (onefile)
cd /d %~dp0\..

echo [1/4] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo [2/4] Generando ejecutable...
pyinstaller --noconfirm --clean --onefile --windowed --name TallerMecanico --add-data "database_schema.sql;." main.py
if errorlevel 1 (
    echo Error: fallo la construccion del ejecutable.
    exit /b 1
)

echo [3/4] Creando paquete portable...
set PORTABLE_DIR=dist\portable\TallerMecanicoPortable
if exist "%PORTABLE_DIR%" rmdir /s /q "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%\data"

copy /y "dist\TallerMecanico.exe" "%PORTABLE_DIR%\TallerMecanico.exe" >nul

(
echo @echo off
echo setlocal
echo REM Modo portable: guarda datos y respaldos en la misma carpeta de la USB
echo set "TM_DATA_DIR=%%~dp0data"
echo start "" "%%~dp0TallerMecanico.exe"
) > "%PORTABLE_DIR%\ABRIR_TALLER.bat"

(
echo TallerMecanico - USB Portable
echo.
echo 1^) Doble clic en ABRIR_TALLER.bat
echo 2^) Trabaje normalmente en la aplicacion
echo 3^) El sistema guarda y respalda automaticamente
) > "%PORTABLE_DIR%\LEEME_PORTABLE.txt"

echo [4/4] Build completado.
echo Ejecutable: dist\TallerMecanico.exe
echo Portable: %PORTABLE_DIR%
