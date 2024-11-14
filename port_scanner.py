import socket
import threading

def get_service_name(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        8080: "HTTP-Alt"
    }
    return services.get(port, "Unknown")


def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)  
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except (socket.error, UnicodeDecodeError):
        return None


def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)  
        result = sock.connect_ex((ip, port))
        if result == 0:  
            service_name = get_service_name(port)
            print(f"Port {port} is OPEN - Service: {service_name}")

           
            banner = grab_banner(ip, port)
            if banner:
                print(f"  Banner: {banner}")
            else:
                print("  No banner available")
        sock.close()
    except socket.error:
        pass



def scan_ports(ip, start_port, end_port):
    print(f"Starting port scan on {ip} from port {start_port} to {end_port}...")
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    print("Port scan completed.")



if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    scan_ports(target_ip, start_port, end_port)
