import socket
import ssl
from datetime import datetime, timezone

def check_tls(host, port):

    ctx = ssl.create_default_context()
    ctx.load_verify_locations("/home/router/cert.pem")

    with socket.create_connection((host, port)) as sock:
        try:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                ver = ssock.version()
        except ssl.SSLCertVerificationError as e:
            print(f"{e=}")
            return


    print(f"TLS version: {ver}")


    notafter = cert['notAfter']
    fmt = "%b %d %H:%M:%S %Y %Z"
    parsed_date = datetime.strptime(notafter, fmt).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = parsed_date - now
    print(f"{diff.days} days remaining")

    if diff.days < 0:
        print("Certificate expired")
    elif (0 <= diff.days < 30):
        print("Certificate soon to expire")
    else:
        print("Certificate is valid")

check_tls("app1.lab", 443)