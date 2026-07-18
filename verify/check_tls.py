import socket
import ssl
from datetime import datetime, timezone
import sys

WARN_DAYS = 30

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

    problems = 0

    for host in hosts:
        print(host)
        result = (check_tls(host, 443))
        #for key, value in result.items():
            #print(f"{key}: {value}")
        if result["status"] == "ok":
            print(f"TLS version: {result['tls_version']}")
            if result["days_left"] < 0:
                print("Certificate expired")
            elif 0 <= result["days_left"] < WARN_DAYS:
                print(f"Certificate will expire in {result['days_left']}")
            else:
                print("Certificate is valid")
        elif result["status"] == "unreachable":
            print(f"Service unreachable: {result['error']}")
            problems = 1
        elif result["status"] == "cert_error":
            print(f"Certificate error: {result['error']}")
            problems = 1        
        print("\n")
    sys.exit(1 if problems else 0)
main()
