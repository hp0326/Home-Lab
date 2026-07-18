import socket
import sys
import ssl
from datetime import datetime, timezone
import http.client

cert_path = "/home/router/cert.pem"
WARN_DAYS = 30
hosts = ["app1.lab", "app2.lab"]
tests = [{"host": "192.168.20.2", "port": 80, "description": "HTTP in DMZ", "expected": True},
         {"host": "192.168.20.2", "port": 443, "description": "HTTPS in DMZ", "expected": True},
         {"host": "192.168.20.2", "port": 8081, "description": "Backend in DMZ", "expected": False},
         {"host": "192.168.30.2", "port": 25, "description": "Port in Servers", "expected": False},
         {"host": "192.168.10.1", "port": 22, "description": "SSH in Router", "expected": True}]

# PORTS
def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex((host, port))

        if result == 0:
            return True
        else:
            return False
def run_check_port():
    failed = 0
    for test in tests: 
        port_open = check_port(test["host"], test["port"])

        if port_open == test["expected"]:
            print(f"{test['description']}; Expected: {test['expected']}, found: {port_open} [OK]")
        else:
            print(f"{test['description']}; Expected: {test['expected']}, found: {port_open} [FAILED]")
            failed+=1        
    return failed



# TLS
def check_tls(host, port):
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(cert_path)

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
def run_check_tls():
    problems = 0
    for host in hosts:
        print(host)
        result = (check_tls(host, 443))
        if result["status"] == "ok":
            print(f"TLS version: {result['tls_version']}")
            if result["days_left"] < 0:
                print("Certificate expired")
                print("\n")
                problems += 1
            elif 0 <= result["days_left"] < WARN_DAYS:
                print(f"Certificate will expire in {result['days_left']}")
                problems += 1
                print("\n")
            else:
                print("Certificate is valid")
                print("\n")
        elif result["status"] == "unreachable":
            print(f"Service unreachable: {result['error']}")
            problems += 1
        elif result["status"] == "cert_error":
            print(f"Certificate error: {result['error']}")
            problems += 1
    return problems



# HTTP
def check_http(host):

    ctx = ssl.create_default_context()
    ctx.load_verify_locations(cert_path)

    try:
        conn = http.client.HTTPSConnection(host, context=ctx)
        conn.request("GET", "/")
        resp = conn.getresponse().status
        conn.close()
    except ssl.SSLCertVerificationError as e:
        return {"status": "cert_error", "http_code": None, "error": str(e)}
    except OSError as e:
        return {"status": "unreachable", "http_code": None, "error": str(e)}

    return {"status": "ok", "http_code": resp, "error": None}
def run_check_http():
    problems = 0
    for host in hosts:
        print(host)
        result = (check_http(host))
        if result["status"] == "ok":
            if result["http_code"] >= 400:
                print("HTTP error")
                print("\n")
                problems += 1
            else:
                print("HTTP ok")
                print("\n")
        elif result["status"] == "unreachable":
            print(f"Service unreachable: {result['error']}")
            problems += 1
        elif result["status"] == "cert_error":
            print(f"Certificate error: {result['error']}")
            problems += 1
    return problems

if __name__=="__main__":
    print("=====PORTS=====")
    ports = run_check_port()

    print("=====TLS=====")
    tls = run_check_tls()

    print("=====HTTP=====")
    http =run_check_http()

    problems = ports + tls + http

    sys.exit(1 if problems else 0)