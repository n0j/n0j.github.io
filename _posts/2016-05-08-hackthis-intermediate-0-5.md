---
layout: post
title:  "HackThis!! :: Intermediate :: Levels 1-5"
date:   2016-05-08
---

[HackThis!! Intermediate](https://www.hackthis.co.uk/levels/Intermediate)

# Intermediate Level 1

![intermediate01-01](/img/hackthis-intermediate/intermediate01-01.png)

Do what the man says! We'll assume the parameter name to be 'password.'

![intermediate01-02](/img/hackthis-intermediate/intermediate01-02.png)

Donezor.

# Intermediate Level 2

![intermediate02-01](/img/hackthis-intermediate/intermediate02-01.png)

This took me a hilariously long time to figure out.  In my first attempt I simply made a GET request for the page, captured it in a Burp proxy, changed the verb to POST, added the data, and sent it out. It looked like this:

![intermediate02-02](/img/hackthis-intermediate/intermediate02-02.png)

This does not work.  In a second attempt, months later, I decided to POST the password by injecting a form into the page and submitting it.  The form:

![intermediate02-03](/img/hackthis-intermediate/intermediate02-03.png)

![intermediate02-04](/img/hackthis-intermediate/intermediate02-04.png)

The POST request:

![intermediate02-05](/img/hackthis-intermediate/intermediate02-05.png)

As far as I can tell, the only meaningful difference is the Content-Type header.

```
Content-Type: application/x-www-form-urlencoded
```

Lesson learned.

# Intermediate Level 3

![intermediate03-01](/img/hackthis-intermediate/intermediate03-01.png)

Clicking on the image returns us to the same page with an 'Invalid details' error.

![intermediate03-02](/img/hackthis-intermediate/intermediate03-02.png)

Taking a look at the request, we see a cookie of interest.

![intermediate03-03](/img/hackthis-intermediate/intermediate03-03.png)

Copy the request to the Burp Repeater tab, modify the cookie value to 'true,' and send it along. Success, as seen from the raw response in Repeater:

![intermediate03-04](/img/hackthis-intermediate/intermediate03-04.png)

# Intermediate Level 4

![intermediate04-01](/img/hackthis-intermediate/intermediate04-01.png)

Being the first XSS challenge, I imagine it is one of the classics. My favorite is "scrscriptipt." When you remove the word script, you're left with the word script.  Plus it's fun to say scr-script-ipt like an idiot.  That didn't quite work, but the following variation did:

```
<scr<script>ipt>alert('HackThis!!');</scr</script>ipt>
```

Success.

# Intermediate Level 5

![intermediate05-01](/img/hackthis-intermediate/intermediate05-01.png)

I have to be honest, this made no sense. I tried a few things like basic SQLi strings with no luck. A few days later I tried again from a different location (and different IP) and it let me in with any input.

It might have made sense if the second request from a different IP was delivered during the 10 second lockout, maybe some kind of ridiculously ill-conceived lockout mechanism that leaves the door open. Three days later though? Yea... I dun get it.

Threads in the solutions forum are entitled things like "Literally just guessed," "I don't understand what I did," "I absolutely am confused," etc...

![intermediate05-02](/img/hackthis-intermediate/intermediate05-02.png)
