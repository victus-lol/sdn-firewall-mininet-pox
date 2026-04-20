# SDN Firewall using POX and Mininet

## Problem Statement
Implement a Software Defined Networking (SDN) firewall using the POX controller and Mininet.  
The firewall blocks traffic from **h1 (10.0.0.1)** to **h3 (10.0.0.3)** while allowing all other communication.

---

## Technologies Used
- Python 3.9  
- POX Controller  
- Mininet  
- Open vSwitch  
- Wireshark  

---

## Setup Instructions

### 1. Install Dependencies
sudo apt update  
sudo apt install mininet openvswitch-switch wireshark -y  
sudo apt install python3.9 python3.9-venv -y  

### 2. Setup POX Environment
cd ~/pox  
python3.9 -m venv poxenv  
source poxenv/bin/activate  

### 3. Run POX Controller
cd ~/pox  
source poxenv/bin/activate  
./pox.py log.level --DEBUG openflow.of_01 misc.firewall_controller  

### 4. Run Mininet (in a new terminal)
sudo mn -c  

sudo mn --topo single,3 \
--controller=remote,ip=127.0.0.1,port=6633 \
--switch ovsk,protocols=OpenFlow10  

---

## Execution

### Blocked Traffic
h1 ping h3  

**Expected:** 100% packet loss  

### Allowed Traffic
h2 ping h3  

**Expected:** Ping successful  

---

## Flow Table Verification
sudo ovs-ofctl dump-flows s1  

**Expected rule:**  
nw_src=10.0.0.1,nw_dst=10.0.0.3 actions=drop  

---

## Expected Output
- Traffic from **h1 → h3** is blocked  
- Traffic from **h2 → h3** is allowed  
- Drop rule is installed in the switch flow table  

---

## References
- POX Documentation  
- Mininet Documentation  
- OpenFlow Specification  
- Wireshark Documentation  

---

## Author
**Aaryan**
