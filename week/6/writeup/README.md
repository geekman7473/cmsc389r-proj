# Writeup 6 - Binaries I

Name: *PUT YOUR NAME HERE*
Section: *PUT YOUR SECTION NUMBER HERE*

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: *PUT YOUR NAME HERE*

## Assignment Writeup

### Part 1 (50 pts)

CMSC389R-{di5a55_0r_d13}

### Part 2 (50 pts)

The input necessary to reproduce is as follows:
```bash
echo " they burn" >> sesame
export FOOBAR=" my eyes"
./crackme "Oh God"
```

The program uses four checks to determine if you have supplied the correct inputs. The first thing it does is check that argc, the variable that describes how many space delimited argument you have provided, is greater than 1. This checks that you have entered SOME string argument, but not necessarily the correct answer. After this check, the function check1 is called which loops through the argument you've provided and checks that each character is equal to the desired input "Oh God." If this check succeeds (ie. returns 0) then check2 is called. Check2 uses the syscall "getenv" to request the value of "FOOBAR." It then reverses the value, and checks if it matches the string "seye ym " character by character. If it doesn't return -2 (none matching env variable) or -1 (no definition for FOOBAR) check3 is called. Check3 opens a file in the current working directory called "sesame." If no file called sesame exists, it returns -1. If the file exists, it reads 10 characters from the file. If the file contains fewer than 10 characters, it returns -2. If 10 characters were able to be read, it then iterates through them and compares them to hardcoded if statements for each character. If any of these don't match, it returns -3. If all of these match, a non-negative value is returned, which points to the flag in memory. The flag pointer is pushed onto the stack, and printf is called, outputting the flag.

The flag was stored in mem
