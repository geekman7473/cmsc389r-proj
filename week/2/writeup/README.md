# Writeup 2 - OSINT

Name: *PUT YOUR NAME HERE*
Section: *PUT YOUR SECTION NUMBER HERE*

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: *PUT YOUR NAME HERE*

## Assignment Writeup

### Part 1 (45 pts)

1. ejnorman84's real name is Eric J Norman (and presumably, he was born in 1984) Found this on pastebin
2. Wattsamp Energy http://wattsamp.net/index.html Found this by tracing down Eric's Linkdin, Instagram, and Twitter
3. Eric J Norman. Phone: (202) 656 - 2837, Address: 1300 Adabel Dr, El Paso, TX. Found this all in the "registrant" section of the whois entry.
4. 157.230.179.99, Hosted on DigitalOcean in North Bergen, NJ, USA. Was registered on 2019-09-04. This was all found on [whois.domaintools.com](http://whois.domaintools.com/wattsamp.net)
5. Robots.txt, assets/, views/
6. `nmap -A -T4 -p1-65535 wattsamp.net` 
22 -> ssh
25 -> smtp
80 -> http
554 -> tcpwrapped
1337 -> unknown
7070 -> unknown
11211 -> memcache
7. Ubuntu, from nmap
8. DNS TXT entry: *CMSC389R-{Do_you-N0T_See_this}
Page source: *CMSC389R-{html_h@x0r_lulz}
robots.txt: *CMSC389R-{n0_indexing_pls}
### Part 2 (75 pts)

The key to the solution here was dealing with the fact that the socket could have errors, so I did what I could to handle this. 

One issue I ran into was because of a red herring in the challenge. The pastebin gave "hints" at the structure of the passwords that didn't correlate to the password for the remote system.

For additional performance, using multiprocessing helped me quickly move through possible combinations. Running on 20 processes, I was able to eliminate ~150 passwords per minute.