# Writeup 1 - Web I

Name: Justin Becker
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement: Justin T. Becker


## Assignment details
This assignment has two parts. It is due by 11/27/19 at 11:59PM.

**There will be late penalty of 5% per day late!**

### Part 1 (40 Pts)

Such a Quick Little, website!

[http://142.93.136.81:5000/](http://142.93.136.81:5000/)

Seeing that XSS would not work for this attack, I knew to exploit the query paramater of the search. The query `item?id=0'OR'1=1' -- -` failed due to the SQL injection detection mechanism, but `item?id=0'|| 0x50 is not null` worked like a charm, yielding the flag.

CMSC389R-{y0u_ar3_th3_SQ1_ninj@}

### Part 2 (60 Pts)
Complete all 6 levels of:

[https://xss-game.appspot.com](https://xss-game.appspot.com)

Produce a writeup. We will not take off points for viewing the source code and/or viewing hints, but we strongly discourage reading online write-ups as that defeats the purpose of the homework.

1) Straightforward. Seeing that the text of your search query is directly rendered on the page searching for `<script>alert("XSS")</script>` did the trick.
2) This level sets the document type to HTML, meaing the script tag won't work anymore. As a workaround, we can find another tag that can execute JS. One example is `img` which has an `onerror` attribute, capable of running JS. Input was `<img src="http://wattsamp.net/foobar.jpg" onerror="javascript:alert("XSS")"/>` 
3) The page uses the last part of the URL to dynamically load an image on the site. ie `https://xss-game.appspot.com/level3/frame#1` will load `<img src='/static/level3/cloud" + 1 + ".jpg' />`. Inserting the rest of the attack last time into the URL bar will do the trick: `https://xss-game.appspot.com/level3/frame#3' onerror='alert("XSS")';`

### Format

Part 1 and 2 can be answered in bullet form or full, grammatical sentences.

### Scoring

* Part 1 is worth 40 points
* Part 2 is worth 60 points

### Tips

Remember to document your thought process for maximum credit!

Review the slides for help with using any of the tools or libraries discussed in
class.
