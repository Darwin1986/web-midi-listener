@echo off
REM ─────────────────────────────────────────────────────────────────────────
REM  BandMaster Listener — Start HTTPS server
REM  Opens index.html for Android Chrome via the local network.
REM ─────────────────────────────────────────────────────────────────────────
REM  Prerequisites:
REM    pip install cryptography
REM
REM  After starting, navigate on the Android tablet to:
REM    https://<this-PC-IP>:8080/
REM  Accept the self-signed certificate warning once.
REM ─────────────────────────────────────────────────────────────────────────

echo.
echo Checking for 'cryptography' package...
python -c "import cryptography" 2>NUL
if errorlevel 1 (
    echo   Not found -- installing...
    pip install cryptography
)

echo.
echo Starting BandMaster Listener server...
echo.
python "%~dp0serve.py" %*
pause
