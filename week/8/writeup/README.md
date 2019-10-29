# Writeup 8 - Binaries II

Name: Justin Becker
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker

## Assignment Writeup

### Part 1 (100 pts)
Answer the following questions regarding the server executable (for which source is provided).

1. How is the per-session administrator password generated? Are there any inherent weaknesses in this implementation?

The password is generated using rand() with a seed set using processor time in seconds. Since we have the source code, we could run a second instance of the process at the same time modified to output the password generated. If the random seed is set in the same second, then they should have the same password. Using this technique, I was able to gain "escalated priveleges" by running two versions of the binary in quick succession as such: `./server_modified; ./server` to my surprise, this also worked against the remote server as such: `./server_mod; nc ec2-18-222-89-163.us-east-2.compute.amazonaws.com 1337`

Fun fact: this attack was used against an online poker site. The site used the current millisecond in the day, local time, as a random seed for each hand. Attackers would then try a spread of random seeds corresponding to times around when the deck was shuffled. Based on cards in the players hand, and the cards on the table, attackers were able to guess with very high confidence the seed that was used, and therefore the state of the entire deck.

2. Describe two vulnerabilities in this program. Provide specific line numbers and classifications of the vulnerability. Explain potential ramifications as well as ways to avoid these vulnerabilities when writing code.

One vulnerability is the use of `gets()` on line 68. Using this, if the user enters more than `BUFF_SIZE + 1` characters, then they will begin to overwrite the buffer pointed to by `commands.` The risk of this vulnerability is it allows an attacker to write arbitray data into areas of memory the programmer didn't intend. This can allow memory manipulation, as I will describe in part 4, or even arbitrary code execution, as was demonstrated in lecture. In general, it's considered a best practice to use more modern functions which check for buffer overflows.

Another vulnerability is the use of `strcasestr()` on line 71. This function checks if the 3rd argument is a substring of the 2nd argument. If improperly implemented, this can allow an attacker to provide malformed inputs which are still accepted. For example, supplying `ls` as an input would match the list of whitelisted commands, even though the intention was for the whitelisted commands to be `ls /var/logs`. To avoid this, I would check that each new-line delimited command in `commands` matches the user supplied command.

3. What is the flag?

CMSC389R-{expl017-2-w1n}

4. Describe the process you followed to obtain the flag: vulnerabilities exploited, your inputs to the server in a human-readable format, etc. If you create any helper code please include it.

I built a modified binary that outputs the random password to stdout. With this binary I used the command `./server_mod; nc ec2-18-222-89-163.us-east-2.compute.amazonaws.com 1337` to generate the random password at the same time as the server starts. With a decent probability these passwords would match, but I did have to try 3-4 times until I got a match. With elevated priviledges I was able to locate the flag in `/` using `ls /`. To output the flag, I used the input `cat ^@                            cat flag`, where ^@ is the null character. (I was able to inject this character using Ctrl-Shift-2 on my keyboard) This input yielded the flag.

The following is the code for the main function of my modified server.c

```c
int main(void) {
    int i, prompt_response;
    /* password for admin to provide to dump flag */
    char *password;
    /* true if user is admin */
    uint8_t admin;

    /* seed random with time so that we can password */
    srand(time(0));
    admin = 0;
    password = calloc(1, PASS_SIZE+1);
    for (i = 0; i < PASS_SIZE; i++) {
        password[i] = rand() % ('z'-' ') + ' ';
    }
    password[PASS_SIZE] = 0;

    printf(password);

    free(password);
    fflush(stdout);

    return;
}
```