---
layout: post
title:  "OWASP Juice Shop v7.3.0 - Level 1"
date:   2018-07-31
---

[OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project)

For this walk through I've pulled the [Docker image](https://hub.docker.com/r/bkimminich/juice-shop/) to run locally. Also, I've appended `127.0.0.1 juice.shop` to my `/etc/hosts` files for no reason other than to make the URL a little prettier.

Behold, Juice Shop!

![juice shop](/img/owasp-juice-shop-v7.3.0/juice000.png)

# Discovery, Enumeration

First, a click-through of the site to familiarize ourselves with its intended functionality. There's a lot going on here - user accounts with a forgotten password function, item listings with reviews, a check-out cart that generates pdf files, coupon codes, a contact form, search boxes, and on and on.

Finally, a quick `dirb` to feel out any unlinked content. I'll use the 'big' word list since the network is fast, the web app and server are fast, there are no concerns about stealthiness, and it's not really even that big.

![dirb](/img/owasp-juice-shop-v7.3.0/juice002.png)

My gut tells me that the `/ftp` directory is interesting, we'll save that for later.

While running `dirb` a banner appeared in the browser, congratulating me on solving a challenge. Well, OK - off to a good start. Not sure exactly what caused that but we do show an HTTP 500 response in the `dirb` results; could be that.

![error challenge](/img/owasp-juice-shop-v7.3.0/juice001.png)

# Scoreboard

Here I have to admit to a small bit of cheating. I have not worked on Juice Shop before but I have seen it and know there's a hidden scoreboard. You can find it by looking at the source of the main page. This is an act I definitely would have taken anyway, so we'll forgive the foreknowledge. ;)

In the source of the menu bar, some items are present which are not rendered in the browser. The 'complain' button, for instance, appears to check whether you're logged in. 

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

# Admin Section

> Access the administration section of the store.

Trying the most obvious thing first and guessing `/#/admin` didn't work but...

![admin section](/img/owasp-juice-shop-v7.3.0/juice004.png)

# Confidential Document

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

# Error Handling

> Provoke an error that is not very gracefully handled.

Done during `dirb` run earlier.

# Redirects Tier 1

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

# XSS Tier 0

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

## Angular Note

A quick note on this, since Angular by default performs anti-XSS measures and we would expect some kind of protection normally here.

By inspecting the 'foo' label we see the use of `ng-bind-html` to `results.orderId`.

```
<small class="label label-default ng-binding" ng-bind-html="results.orderId">foo</small>
```

`results.orderId` is set in the `TrackResultController` controller of juice-shop.min.js by,

```
n.results.orderId = t.trustAsHtml(e.data[0].orderId),
```

where `trustAsHtml` is [a method](https://docs.angularjs.org/api/ng/service/$sce) which essentially instructs Angular to skip security checks like anti-XSS protections.

## Why Reflected XSS?

I believe this is labeled a reflected XSS because the value from the user follows the normal flow of being submitted by the user, sent to the server in a request, and bounced back to the user in the response.

Searching for an order causes a request like the following, in this case triggered by some JS mumbo-jumbo.

```
GET /rest/track-order/foo HTTP/1.1
[...]
```

The response echoes the user input and that value is incorporated into the results page.

```
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: application/json; charset=utf-8
Content-Length: 47
ETag: W/"30-XFXyVdEtZ3mZfp1226b128dTwic"
Date: Wed, 01 Aug 2018 02:29:14 GMT
Connection: close

{"status":"success","data":[{"orderId":"foo"}]}
```

Personally, I am a little leery of labeling this reflected as opposed to DOM because the user input sent to the server isn't the normal form POST where a new page is loaded that includes the reflected input. Here there's some JS firing in the background to an API and results are built into the page (DOM) absent a request for the whole page. So, a little confused on that point and the intentions of the OWASP people in making the distinction between this and the following XSS challenge.

# XSS Tier 1

> Perform a DOM XSS attack with \<script\>alert(\"XSS\")\</script\>.

Much the same for this one, except in the search bar.

![xss](/img/owasp-juice-shop-v7.3.0/juice013.png)

## Why DOM XSS?

I suspect this is labeled DOM XSS by the creators as opposed to reflected XSS due to the fact that the user input value is never returned back to the user by the server. A search causes an API request like this,

```
GET /rest/product/search?q=foo HTTP/1.1
```

And the result does not contain the user-supplied value. In fact it doesn't contain much of anything since a search for 'foo' returns no results.

```
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: application/json; charset=utf-8
Content-Length: 30
ETag: W/"1e-JkPcI+pGj7BBTxOuZTVVIm91zaY"
Date: Wed, 01 Aug 2018 02:31:13 GMT
Connection: close

{"status":"success","data":[]}
```

It must be that user input value is loaded into the page via a live modification of the DOM and not 'reflected' per se in a response from the server. As previously mentioned, I don't have great confidence in this distinction - particularly given the form of their reflected XSS example.

# Zero Stars

> Give a devastating zero-star feedback to the store.

Because of the CAPTCHA, the easiest way to do this is probably modifying the request in a local proxy (Burp Suite, in my case). Sure enough, 'rating' is in the request.

![zero star](/img/owasp-juice-shop-v7.3.0/juice014.png)

And the value of zero is accepted by the server.

![zero star](/img/owasp-juice-shop-v7.3.0/juice015.png)