# Writeup 7 - Forensics I

Name: Justin Becker
Section: 0101
I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker

## Assignment Writeup

### Part 1 (100 pts)
Answer the following questions regarding [this](../image) file:

1. What kind of file is it?
The file opens with `FF D8 FF E1` which corresponds to JPEG

2. Where was this photo taken? Provide a city, state and the name of the building in your answer.

Rooftop of the John Hancock Center, Chicago, IL

3. When was this photo taken? Provide a timestamp in your answer.

2018:08:22 11:33:24

4. What kind of camera took this photo?

Apple iPhone 8

5. How high up was this photo taken? Provide an answer in meters.

539.5 m Above Sea Level

6. Provide any found flags in this file in standard flag format.

`strings image | grep "CMSC389"` => CMSC389R-{look_I_f0und_a_str1ng}

A bruteforce attack against the file was not able to extract anything using steghide and the rockyou wordlist.

using `binwalk --dd='.*' image.jpg` recovered a png file at 0x248F20
Opening this file revealed the flag CMSC389R-{abr@cadabra}