import socket
import ssl
from datetime import datetime, timezone

def check_tls(host, port):

    ctx = ssl.create_default_context()
    ctx.load_verify_locations("/home/router/cert.pem")

    try:
        with socket.create_connection((host, port), timeout = 2) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                ver = ssock.version()
    except ssl.SSLCertVerificationError as e:
        return {"status": "cert_error", "tls_version": None, "days_left": None, "error": str(e)}
    except OSError as e:
        return {"status": "unreachable", "tls_version": None, "days_left": None, "error": str(e)}

    notafter = cert['notAfter']
    fmt = "%b %d %H:%M:%S %Y %Z"
    parsed_date = datetime.strptime(notafter, fmt).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = parsed_date - now

    return {"status": "ok", "tls_version": ver, "days_left": diff.days, "error": None}

def main():
    hosts = ["app1.lab", "app2.lab"]

    for host in hosts:
        print(check_tls(host, 443))

main()
