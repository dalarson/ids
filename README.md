title: "CS4404 Mission 3"
date: "December 8, 2019"
author:
    - "David Larson"
    - "Ben Longo"
    - "Cole Winsor"

# Containernet Instructions

1. Unzip repository and navigate to mission3 directory

2. Install docker
```
sudo apt install docker
```

3. Create docker images
```
sudo make
```

4. Start containernet
```
sudo topology.py
```
5. Start clients and begin generating traffic over bridge
```
client_1 bash loadgen.sh > /dev/null &
client_2 bash loadgen.sh > /dev/null &
client_3 bash loadgen.sh > /dev/null &
```
NOTE: These clients are going to be making http requests to the web server and printing the responses, so simply run the command without `> /dev/null` to see the output.

6. Launch cookie attack
```
c2 bash run_command.sh ls
```

7. Check snort logs
```
r tail /var/log/snort/alert
```

Find logged alerts!
```
12/09-04:15:42.219566  [**] [1:102:0] Malicious cookie detected! [**] [Priority: 0] {TCP} 10.0.0.4:38280 -> 10.0.0.3:5000
```

8. Toggle on HTTPS
```
ws bash enable_https.sh
```

8. Have server monitor 
```
ws nohup tshark -l -i ws-eth0 -f "tcp port 5000" -Y "ssl.handshake.type == 1" -o http.ssl.port:5000 -T fields -e ssl.handshake.random_bytes > output &
```
9. Put a number into the /user_id file (will default to 0 if this step is skipped)
```
c2 echo your_favorite_number > /user_id
```

10. Run TLS handshake attack
```
c2 curl -k https://10.0.0.3:5000
```

11. Look at the output on the server
```
ws cat output
```
Note: Here will be the contents of the TLS 32 bit random field. The last four octets will be zeros, the first four will contain the user_id which we entered into `/user_id`.
