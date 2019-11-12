# Writeup 9 - Forensics II

Name: Justin Becker
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker


## Assignment details

### Part 1 (45 Pts)

1. Warmup: what IP address has been attacked?

142.93.136.81

2. What kind of assessment tool(s) were the attackers using against the victim machine? List the name(s) of the tool(s) as well.

nmap

3. What are the hackers' IP addresses, and where are they connecting from?

159.203.113.181. This is a digitalocean droplet, so we can't determine where the attackers are located with any certainty without a subpeona on Digitalocean's records.

4. What port are they using to steal files on the server?

21

5. Which file did they steal? What kind of file is it? Do you recognize the file?

find_me.jpg. It's an image file. exiftools reveals that it was taken at Los Dedos de Punta del Este in Maldonado, Uruguay

6. Which file did the attackers leave behind on the server?

They left behind greetz.fpff

7. What is a countermeasure to prevent this kind of intrusion from happening again? Note: disabling the vulnerable service is *not* an option.

Using a firewall to prevent hostile actors from nmapping your service. Additionally, serving your FTP service on a non-standard port number could reduce the chances of a hostile actor discovering the service.

### Part 2 (55 Pts)

CMSC389R-{w3lc0me_b@ck_fr0m_spr1ng_br3ak}
CMSC389R-{h0pefully_y0u_didnt_grep_CMSC389R}