from scapy.all import sniff, IP, TCP
import logging

# Configure logging
logging.basicConfig(filename='packets.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        log_message = f"[+] New Packet: {ip_layer.src} -> {ip_layer.dst}"
        print(log_message)
        logging.info(log_message)
        if packet.haslayer(TCP):
            tcp_layer = packet.getlayer(TCP)
            log_message = f"[*] {ip_layer.src}:{tcp_layer.sport} -> {ip_layer.dst}:{tcp_layer.dport}"
            print(log_message)
            logging.info(log_message)
            log_message = f"[*] Flags: {tcp_layer.flags}"
            print(log_message)
            logging.info(log_message)
            if tcp_layer.payload:
                log_message = f"[*] Payload: {tcp_layer.payload}"
                print(log_message)
                logging.info(log_message)

def main():
    print("[*] Starting packet sniffer")
    # Capture only TCP packets
    sniff(filter="tcp", prn=packet_callback, store=0)

if __name__ == '__main__':
    main()
