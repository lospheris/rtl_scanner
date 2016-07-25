# rtl_scanner

Clark and I were chatting the other night and I decided I want a way to try to scan for people pushing rtl_tcp connections to the public internet.

After digging through the rtl_tcp source for a short while I found that when you connect to a rtl_tcp server it immediately dumps a 12 byte structure to the socket.
The structure is 4 char bytes that is always "RTL0", then a uint32_t with the type of dongle, and another uint32_t with the dongle gain. The int desribing the dongle is set by an enum so I just copied that.
Everything else is pretty straight forward. At this time the program really only scans on port 1234 as that is the defualt. I will work on that later.
