---
layout: post
title:  "OWASP Juice Shop v7.3.0 - Level 1"
date:   2018-07-25
---

[OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project)

For this walkthrough I've pulled the [Docker image](https://hub.docker.com/r/bkimminich/juice-shop/) to run locally. Also, I've appended `127.0.0.1 juice.shop` to my `/etc/hosts` files for no reason other than to make the URL a little prettier.

Behold, Juice Shop!

![juice shop](/img/owasp-juice-shop-v7.3.0/juice000.png)

# Discovery, Enumeration

First, a click-through of the site to familiarize ourselves with its intended functionality. There's a lot going on here - user accounts with a forgotten password function, item listings with reviews, a check-out cart that generates pdf files, coupon codes, a contact form, search boxes, and on and on.

Finally, a quick `dirb` to feel out any unlinked content. I'll use the 'big' wordlist since the network is fast, the web app and server are fast, there are no concerns about stealthiness, and it's not really even that big.

![dirb](/img/owasp-juice-shop-v7.3.0/juice002.png)

My gut tells me that the `/ftp` directory is interesting, we'll save that for later.

While running `dirb` a banner appeared in the browser, congratulating me on solving a challenge. Well, OK - off to a good start. Not sure exactly what caused that but we do show an HTTP 500 response in the `dirb` results; could be that.

![error challenge](/img/owasp-juice-shop-v7.3.0/juice001.png)

# Scoreboard

Here I have to admit to a small bit of cheating. I have not worked on Juice Shop before but I have seen it and know there's a hidden scoreboard. You can find it by looking at the source of the main page. This is an act I definitely would have taken anyway, so we'll forgive the cheating. ;)

In the sourece of the menu bar, some items are present which are not rendered in the browser. The 'complain' button, for instance, appears to check whether you're logged in. 

```
<li class="dropdown" ng-show="isLoggedIn()">
    <a href="#/complain"><i class="fas fa-bomb fa-lg"></i> <span translate="NAV_COMPLAIN"></span></a>
</li>
<li class="dropdown" ng-show="scoreBoardMenuVisible">
    <a href="#/score-board"><i class="fas fa-trophy fa-lg"></i> <span translate="TITLE_SCORE_BOARD"></span></a>
</li>
<li class="dropdown ribbon-spacer">
    <a href="#/about"><i class="fas fa-info-circle fa-lg"></i> <span translate="TITLE_ABOUT"></span></a>
</li>
```

Visiting `/#/score-board`, boom...

![scoreboard](/img/owasp-juice-shop-v7.3.0/juice003.png)

From this point on I'll name each section based on the challenge name from the scoreboard and just go down the list in order, assuming that's possible.

# 1 - Admin Section

> Access the administration section of the store.

Trying the most obvious thing first and guessing `/#/admin` didn't work but...

![admin section](/img/owasp-juice-shop-v7.3.0/juice004.png)

# 1 - Confidential Document

> Access a confidential document.

Another gut call, I bet there's something in that `/ftp` directory that shouldn't be there.

![ftp](/img/owasp-juice-shop-v7.3.0/juice005.png)

`wget` can download all the links on the page with following where `-r` is for recursive, `-l 1` limits recursion to one level (not necessary here but good habit), and `-np` is for no-parent (i.e. don't download the `ftp` page itself).

```
# wget -r -l 1 -np http://juice.shop:3000/ftp/
```

The output shows a few unexpected 403 errors. Looking into one manually,

![ftp 403](/img/owasp-juice-shop-v7.3.0/juice006.png)

Take note of the file type restriction for later. For now, it appears accessing what we could has tripped 'Confidential Document' on the scoreboard.

# 1 - Error Handling

> Provoke an error that is not very gracefully handled.

Done during `dirb` run earlier.

# 1 - Redirects Tier 1

> Let us redirect you to a donation site that went out of business.

'Donation site' is a big hint here, I recall from poking around that there are PayPal and credit card buttons in the shopping cart that linked to actual OWASP donation instructions. 

![donation](/img/owasp-juice-shop-v7.3.0/juice007.png)

The source has a commented out button.

```
<!--
	<a href="/redirect?to=https://gratipay.com/juice-shop" target="_blank" class="btn btn-danger"> <i class="fab fa-gratipay fa-lg"></i> Gratipay</a>
-->
```

For quick changes like this I think the easiest method is to edit the HTML in the browser's development tools / inspector. Removing the comments,

![donation](/img/owasp-juice-shop-v7.3.0/juice008.png)

Click it, bingo.

![redirect 1](/img/owasp-juice-shop-v7.3.0/juice009.png)

# 1 - XSS Tier 0

> Perform a reflected XSS attack with \<script\>alert(\"XSS\")\</script\>.

First an aside, I just XSS'd myself running Jekyll locally by copying that description into the draft of this page. Guess I better sprinkle some escape characters in there... pretty hilarious.

![jekyll](/img/owasp-juice-shop-v7.3.0/juice010.png)

For a reflected XSS attack we're looking for something that echoes user input back into the page. Clicking around, the 'Track Orders' page appears to do this.

```
http://juice.shop:3000/#/track-result?id=foo
```

![foo](/img/owasp-juice-shop-v7.3.0/juice011.png)

Looks ripe for XSS, barring some kind of protection against it.

![xss](/img/owasp-juice-shop-v7.3.0/juice012.png)

# 1 - XSS Tier 1

> Perform a DOM XSS attack with \<script\>alert(\"XSS\")\</script\>.

