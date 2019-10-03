# Writeup 2 - Pentesting

Name: Justin Becker
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker

## Assignment Writeup

### Part 1 (45 pts)

Command injection, is similar to SQL injection in that it requires user input to be executed upon without santization. (See: ["bobby tables"](https://xkcd.com/327/)) In command injection, a vulnerable script takes user input and uses it to build a bash command. If you do not santize input, an attacker can take advantage of bash syntax such as the ";" which ends the current statement, the way your program was probably expecting, but then allows the attacker to append additional commands. In the case of the wattsamp.net server, an input of `"foobar"; ls` is sufficient to inject our own commands.

Using this technique, I was able to find the flag using the command `; cd /home; ls; cat flag.txt` the flag was as follows:

`Good! Here's your flag: CMSC389R-{p1ng_as_a_$erv1c3}`

To prevent this, Norman should sanitize his input. One technique for doing so is to filter out certain characters that are dangerous, such as ";" or "&." Alternatively, he could use regular expressions to match for valid ip addresses or hostnames, which should be more likely to catch the possibility of attackers injecting commands into the input. Additionally, it would best if all access to his machine was behind an authentication system. Even the weak authentication from HW2 would have been a good extra layer of security for his machine, and could dissuade automated attackers from gaining access to his machine. Alternatively, it would be best to ditch using raw plaintext sockets to communicate with his machine over the network. The industry standard solution to this problem is to use SSH, or a similar protocol, to allow cryptographically secure remote access to his machine.

### Part 2 (55 pts)

To create the shell for this part of the assignment, the key challenge is to keep track of the variables that real shells keep track of for you. Forgetting about complexities like environment variables and .bashrc files, the main design decision you face is keeping track of your current directory. Since the server we're connecting to won't remember our CD we have to keep track of it ourselves. With that said, we have two choices: either resolve relative paths manually, or just append a "cd $PWD;" before every command. This solution saves significant development time, and also avoids the issue of attempting to detect paths in command strings.

One cool feature I was able to implement is command concatentation. We allow users to string together commands with the semicolon, and then they are executed in sequence.
