import scapy.all as scapy

#Funksioni per marrjen e MAC adreses
def mac(ipadd):
    arp_request = scapy.ARP(pdst=ipadd)
    br = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_br = br / arp_request
    list_1 = scapy.srp(arp_req_br, timeout=5, verbose=False)[0]
    return list_1[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

#Funksioni per perpunimin e paketes se nuhatur, marrja e vlerave te MAC adreses se vjeter dhe MAC adreses ne pergjigje.
def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            originalmac = mac(packet[scapy.ARP].psrc)
            responsemac = packet[scapy.ARP].hwsrc

#Krahasimi i vlerave te MAC adreses
            if originalmac != responsemac:
                print("[*] ALERT!! You are under attack, the ARP table is being poisoned.!")
        except IndexError:
            pass

sniff("eth0")

