import os
import python_arptable

def get_ip_addr(hw_addr):
        os.system("fping -a -r 0 -g 172.31.105.0/22 -q | fping")
        for addr in python_arptable.get_arp_table():
                if addr['HW address']==hw_addr:
                        print("IP of "+hw_addr+" is "+addr['IP address'])
                        return addr['IP address']
        return None

#print(get_ip_addr(input("Enter hardware address:")))
