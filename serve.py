#!/usr/bin/env python3
"""
BandMaster Listener — local HTTPS server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Serves index.html over HTTPS with a self-signed certificate so that
Android Chrome's WebMIDI API works (it requires a secure context).

Usage
-----
    python serve.py [port]          # default port: 8080

On the Android tablet, open Chrome and navigate to:
    https://<PC-IP-address>:<port>/

When Chrome warns "connection not private", tap:
    Advanced → Proceed to <IP> (unsafe)

This is expected with a self-signed cert — the page itself is safe.

Alternative (no certificate warning)
-------------------------------------
Install Termux from https://f-droid.org on the tablet, copy the
bandmaster-listener-android folder to the tablet, then run:
    python serve.py
Open Chrome → http://localhost:8080/   (localhost is always secure)
"""

import http.server
import socket
import ssl
import sys
import os
import tempfile

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_local_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"


def make_self_signed_cert():
    """
    Generate a temporary self-signed certificate using the 'cryptography'
    package.  Returns (cert_path, key_path) or (None, None) if unavailable.
    """
    try:
        import datetime
        import ipaddress
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend

        local_ip = get_local_ip()

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, "BandMaster Listener"),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                    x509.IPAddress(ipaddress.IPv4Address(local_ip)),
                ]),
                critical=False,
            )
            .sign(key, hashes.SHA256(), default_backend())
        )

        cert_f = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        key_f  = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        cert_f.write(cert.public_bytes(serialization.Encoding.PEM))
        key_f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
        cert_f.close()
        key_f.close()
        return cert_f.name, key_f.name

    except ImportError:
        return None, None
    except Exception as e:
        print(f"  Warning: could not generate TLS cert: {e}")
        return None, None


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files from SCRIPT_DIR; suppresses per-request log output."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)

    def log_message(self, fmt, *args):
        pass  # uncomment next line to re-enable access logging
        # print(f"  {self.address_string()} {fmt % args}")


def main():
    local_ip   = get_local_ip()
    cert, key  = make_self_signed_cert()
    use_https  = cert is not None

    import socketserver
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        httpd.allow_reuse_address = True

        if use_https:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(certfile=cert, keyfile=key)
            httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
            scheme = "https"
        else:
            scheme = "http"

        bar = "=" * 58
        print(bar)
        print("  BandMaster Listener — Local Server")
        print(bar)
        print(f"  Local:    {scheme}://localhost:{PORT}/")

        if use_https:
            print(f"  Network:  {scheme}://{local_ip}:{PORT}/")
            print()
            print("  On Android Chrome:")
            print(f"    1. Open  {scheme}://{local_ip}:{PORT}/")
            print("    2. Tap  Advanced → Proceed anyway  (self-signed cert)")
        else:
            print()
            print("  [!] 'cryptography' package not installed → plain HTTP.")
            print("      WebMIDI requires a secure context (HTTPS or localhost).")
            print()
            print("  To enable HTTPS:  pip install cryptography")
            print()
            print("  Alternatively — Termux on Android (no cert warning):")
            print("    Copy this folder to the tablet, open Termux, run:")
            print("    pkg install python && python serve.py")
            print("    Then open Chrome → http://localhost:8080/")

        print()
        print("  Press Ctrl+C to stop.")
        print(bar)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")
        finally:
            if cert and os.path.exists(cert):
                os.unlink(cert)
            if key and os.path.exists(key):
                os.unlink(key)


if __name__ == "__main__":
    main()
