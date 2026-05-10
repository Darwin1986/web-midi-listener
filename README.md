# BandMaster Listener — Android Companion

A minimal web app that listens on a MIDI input and displays the matching
PDF sheet music full-screen.  Runs in Chrome on an Android tablet.

---

## Quick start

### Option A — Served from PC over the local network

1. **Install the dependency** (once):
   ```
   pip install cryptography
   ```

2. **Double-click `serve.bat`** (or run `python serve.py`).  
   The terminal shows your PC's local IP address, e.g.:
   ```
   Network:  https://192.168.1.42:8080/
   ```

3. On the **Android tablet**, open Chrome and navigate to that address.

4. Chrome shows **"Your connection is not private"** — this is expected with
   a self-signed certificate.  Tap:
   > **Advanced → Proceed to 192.168.1.42 (unsafe)**

5. The app opens.  Configure once and tap **▶ Start Listening**.

---

### Option B — Served directly from the tablet (no certificate warning)

This is the cleanest approach.  The app runs entirely on the tablet.

1. Install **Termux** from [f-droid.org](https://f-droid.org) (not Google Play).

2. In Termux:
   ```
   pkg install python
   ```

3. Copy the `bandmaster-listener-android` folder to the tablet  
   (e.g. via USB to `/sdcard/Download/`).

4. In Termux:
   ```
   cd /sdcard/Download/bandmaster-listener-android
   python serve.py
   ```

5. Open Chrome → `http://localhost:8080/`  
   → WebMIDI works (localhost is always a secure context, no cert warning).

---

## Connecting a MIDI device to the tablet

| Method | Hardware needed |
|---|---|
| USB-MIDI | USB-OTG adapter + USB-MIDI interface (or a keyboard with USB-MIDI) |
| BLE-MIDI | Bluetooth MIDI device (Android 6+) |
| USB direct | Some keyboards present as USB-MIDI class-compliant devices |

Chrome on Android automatically lists connected MIDI devices.

---

## Configuration

| Setting | Description |
|---|---|
| **Device** | MIDI input port to listen on |
| **Type** | Signal type: CC / PC / Note On / Note Off / Note On+Off |
| **Channel** | MIDI channel (1–16) |
| **CC# filter** | For CC type only: which controller number carries song numbers |
| **Song offset** | Added to received value → song number  (e.g. offset 2, value 1 → song 3) |
| **Delimiter** | Separator after number in filename (default `-`) |

Settings are saved automatically in the browser's local storage.

---

## PDF file naming

Files must start with the song number, optionally followed by a delimiter
and a name:

```
01-My Song.pdf
001 - Another Song.pdf
42_Ballad.pdf
7.pdf
```

The leading digits are matched against the received MIDI value + offset.
Everything after the first non-digit is treated as the song name.

---

## Workflow with the main BandMaster app

1. Run **BandMaster** on the PC in **MIDI Master** mode.  
   It sends the song number on each "Next" press.

2. Connect the PC's MIDI output to the tablet's MIDI input  
   (USB-MIDI interface, BLE-MIDI bridge, or loopback via a DAW).

3. In **BandMaster Listener**, match the signal type / channel / CC# to
   what the main app sends (configured in BandMaster's Settings → MIDI tab,
   Song Number row).

4. When BandMaster changes to song 42, the tablet automatically displays
   `42-songname.pdf`.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | The complete web app (single self-contained file) |
| `serve.py` | Python HTTPS server (self-signed cert, works over LAN) |
| `serve.bat` | Windows launcher for `serve.py` |
| `README.md` | This file |
