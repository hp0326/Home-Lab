import socket

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex((host, port))

        if result == 0:
            return True
        else:
            return False

tests = [{"host": "192.168.20.2", "port": 80, "description": "HTTP in DMZ", "expected": True},
         {"host": "192.168.20.2", "port": 443, "description": "HTTPS in DMZ", "expected": True},
         {"host": "192.168.20.2", "port": 8081, "description": "Backend in DMZ", "expected": False},
         {"host": "192.168.30.2", "port": 25, "description": "Port in Servers", "expected": False},
         {"host": "192.168.10.1", "port": 22, "description": "SSH in Router", "expected": True}]

counter = 0
for test in tests: 

    port_open = check_port(test["host"], test["port"])

    if port_open == test["expected"]:
        passed = True
        print(f"{test['description']}; Expected: {test['expected']}, found: {port_open} [OK]\n")
    else:
        passed = False
        print(f"{test['description']}; Expected: {test['expected']}, found: {port_open} [FAILED]\n")

    
    
    if passed:
        counter+=1

print(f"Number of tests: {len(tests)}, test passed: {counter}, tests failed: {len(tests) - counter}")

