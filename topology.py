#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet(controller=Controller)
net.addController('c0')

router = net.addDocker('r', dimage="cs4404m3t9/router")

# LAN configuration
lan_switch = net.addSwitch('s1')
net.addLink(lan_switch, router)

db = net.addDocker('db', dimage="cs4404m3t9/db",
                   dcmd="docker-entrypoint.sh postgres")
ws = net.addDocker('ws', dimage="cs4404m3t9/ws")

net.addLink(ws, lan_switch)
net.addLink(db, lan_switch)

# WAN configuration
wan_switch = net.addSwitch('s2')

net.addLink(router, wan_switch)

c2 = net.addDocker('c2', dimage="cs4404m3t9/c2")
net.addLink(c2, wan_switch)

client_1 = net.addDocker('client_1', dimage="cs4404m3t9/client")
client_2 = net.addDocker('client_2', dimage="cs4404m3t9/client")
client_3 = net.addDocker('client_3', dimage="cs4404m3t9/client")
net.addLink(client_1, wan_switch)
net.addLink(client_2, wan_switch)
net.addLink(client_3, wan_switch)

net.start()

ws.cmd("nohup python3 server.py &")
router.cmd('bash entry.sh')

net.ping([c2, ws])
net.ping([client_1, ws])
net.ping([client_2, ws])
net.ping([client_3, ws])

net.ping([ws, client_1])
net.ping([ws, client_2])
net.ping([ws, client_2])

net.ping([ws, db])

CLI(net)
net.stop()
