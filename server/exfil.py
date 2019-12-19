import sys

for line in sys.stdin:
    octets = line.split(':')
    if octets[-4:] == ['00', '00', '00', '00']:
        i = int(''.join(octets[0:4][::-1]), 16)
        print("EXFIL REQUEST FOR {}".format(i))
