# rtl_scanner.py

## Description
Clark and I were chatting the other night and I decided I want a way to try to scan for people pushing rtl_tcp connections to the public internet. 

After digging through the rtl_tcp source for a short while I found that when you connect to a rtl_tcp server it immediately dumps a 12 byte structure to the socket.
The structure is 4 char bytes that is always "RTL0", then a uint32_t with the type of dongle, and another uint32_t with the dongle gain. The int desribing the dongle is set by an enum so I just copied that.
Everything else is pretty straight forward. At this time the program really only scans on port 1234 as that is the defualt. I will work on that later.

## Dependencies
The entire program is written in python2.7. I have no idea if it will run on other versions. There are no other dependencies. I wrote it so that you could run it on a bare python build.

## Usage
### Required Arguments
The program requires at least two arguments.
The -a or --address and -m or --mask option.
-a should be the network address to scan
-m should be the mask of the network to scan.

### Optional Arguments
Optionally you can pass the -of or --output_file argument to write the results to a text file.

### Examples
> ./rtl_scanner.py -a 127.0.0.0 -m 255.255.255.0

> ./rtl_scanner.py --address 127.0.0.1 --mask 255.255.255.255

> ./rtl_scanner.py -a 127.0.0.0 -m 255.255.255.0 -of results.txt

> ./rtl_scanner.py -a 127.0.0.0 -m 255.255.255.0 --output_file results.txt
