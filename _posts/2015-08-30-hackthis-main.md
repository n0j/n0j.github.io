---
layout: post
title:  "HackThis!! :: Main :: Levels 1-10"
date:   2015-08-30
---

A nice warm-up series to get a feel for the site. Should be completed in under an hour if you know what's up.

[HackThis!! Main](https://www.hackthis.co.uk/levels/Main)

# Main Level 1

![main01-01](/img/hackthis-main/main01-01.png)

> Having trouble? Need a little help? Well this is the first level so that is to be expected. The first stop is always to view the source of a page.
>
> Firefox?   
> View > Page Source or CTRL+U   
> Internet Explorer?   
> Get firefox!   

In the head...

```
<script src="https://cdn.socket.io/socket.io-1.2.1.js"></script>
<!-- username: in, password: out -->
<script src="https://d3t63m1rxnixd2.cloudfront.net/files/js/modernizr-2.6.2.min.js"></script>
```

# Main Level 2

![main02-01](/img/hackthis-main/main02-01.png)

> Just expanding on the idea of Level 1. The best place to start is always the source code.
>
> Or maybe the answer is right under your nose?!

The old 'same color as the background' trick.

```
<label for="user">Username:</label> <span style="color: #000000">resu</span>
<input type="Text" name="user" id="user" autocomplete="off"><br>
<label for="user">Password:</label> <span style="color: #000000">ssap</span>
<input type="Password" name="pass" id="pass" autocomplete="off"><br>
<input type="submit" value="Submit" class="button">
```

Can be seen highlighted.

![main02-02](/img/hackthis-main/main02-02.png)

# Main Level 3

> Using JavaScript as the only method to secure your site is a bad idea, but this has obviously been over looked while coding this page.

Yea I'd say that's a bad idea.

```
<script type='text/javascript'> $(function(){ $('.level-form').submit(function(e){ if(document.getElementById('user').value == 'heaven' && document.getElementById('pass').value == 'hell') { } else { e.preventDefault(); alert('Incorrect login') } })})</script>
```

# Main Level 4

> Sometimes extra hidden fields are added to the form which contains extra information for the login script. Again this is very easy for anyone to gain access to as it is clearly shown in the source code.
>
> Sometimes these fields can contain very important information.

```
<label for="user">Username:</label>
<input type="Text" name="user" id="user" autocomplete="off"><br>
<label for="user">Password:</label>
<input type="Password" name="pass" id="pass" autocomplete="off"><br>
<input type="hidden" name="passwordfile" value="../../extras/ssap.xml">
<input type="submit" value="Submit" class="button">
```

Visit https://www.hackthis.co.uk/levels/extras/ssap.xml

```
<user>
    <name>Admin</name>
    <username>999</username>
    <password>911</password>
</user>
```

# Main Level 5

> Slightly more complicated JavaScript this time, but just as insecure.
>
> Refresh to try again.

A popup!

![main05-01](/img/hackthis-main/main05-01.png)

Aw.

![main05-02](/img/hackthis-main/main05-02.png)

D'oh.

```
<script language="JavaScript" type="text/javascript">
    var pass;
    pass=prompt("Password","");
    if (pass=="9286jas") {
        window.location.href="/levels/main/5?pass=9286jas";
    }
</script>
```

# Main Level 6

![main06-01](/img/hackthis-main/main06-01.png)

> This page is coded to only let in one user (Ronald). But there is no Ronald?! You will need to find a way to add him to the list.

Dammit, Ronald!

![main06-02](/img/hackthis-main/main06-02.png)

In a simple case like this there's no need to fire up a local proxy, the necessary changes can be made using the [page inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector) that ships with Firefox.

![main06-03](/img/hackthis-main/main06-03.png)

Cool.

![main06-04](/img/hackthis-main/main06-04.png)

# Main Level 7

> The password is again stored in a txt file. This time however it is not as straight forward as viewing the source.

> You wouldn't even find the page by using a search engine as search bots have been excluded.

The obligatory robots.txt challenge...

```
User-agent: *
Allow: /
Disallow: /contact.php
Disallow: /inbox/
Disallow: /levels/
Disallow: /levels/extras/userpass.txt
Disallow: /users/
Disallow: /ctf/8/php/*

User-agent: Mediapartners-Google
Disallow:

Sitemap: https://www.hackthis.co.uk/sitemap.xml
```

Looking at https://www.hackthis.co.uk/levels/extras/userpass.txt

```
48w3756
u3qh458
```

Yup.

![main07-01](/img/hackthis-main/main07-01.png)

# Main Level 8

> The coder has made the same mistake as level 4 but this time at least he has tried to protect the password. The password has been encrypted, convert the binary into something that is easier for humans to read (base 16).
>
> If you think you have the right answer but it isn't being accepted, submit your answer in CAPITALS.

In the source.

```
<label for="user">Username:</label>
<input type="Text" name="user" id="user" autocomplete="off"><br>
<label for="user">Password:</label>
<input type="Password" name="pass" id="pass" autocomplete="off"><br>
<input type="hidden" name="passwordfile" value="extras/secret.txt">
<input type="submit" value="Submit" class="button">
```

Loading https://www.hackthis.co.uk/levels/extras/secret.txt

```
1011 0000 0000 1011
1111 1110 1110 1101
```

Do it in your head or go home.

```
B00B
FEED
```

Well then, boob feed. Am I being fed the boobs or are we talking about some kind of boob sustenance?

# Main Level 9

> The developer has now added a feature that allows him to get a password reminder. Can you exploit it to send you the login details instead?

Clicking 'Request details' brings you to https://www.hackthis.co.uk/levels/main/9?forgot

![main09-01](/img/hackthis-main/main09-01.png)

```
<label for="email1">Email:</label>
<input type="text" name="email1" id="email1" autocomplete="off"><br>
<input type="hidden" name="email2" id="email2" value="admin@hackthis.co.uk" autocomplete="off">
<input type="submit" value="Submit" class="button">
```

Likely the story here is that an email will be sent to the address specified by user input and a copy sent to admin@hackthis.co.uk. Let's have them both sent to us instead.  The page inspector again works well for this.

![main09-02](/img/hackthis-main/main09-02.png)

Yup.

![main09-03](/img/hackthis-main/main09-03.png)

# Main Level 10

> Encrypted passwords can be quite difficult to decode, but when you use a common method there is usually a way to get around it. Especially when the encrypted information are simple common words.

```
<label for="user">Username:</label>
<input type="Text" name="user" id="user" autocomplete="off"><br>
<label for="user">Password:</label>
<input type="Password" name="pass" id="pass" autocomplete="off"><br>
<input type="hidden" name="passwordfile" value="level10pass.txt">
<input type="submit" value="Submit" class="button">
```

I wasted a bunch of time trying to find the text file here before adding the 'extras' directory seen in previous levels. Visit https://www.hackthis.co.uk/levels/extras/level10pass.txt

```
69bfe1e6e44821df7f8a0927bd7e61ef208fdb25deaa4353450bc3fb904abd52:f1abe1b083d12d181ae136cfc75b8d18a8ecb43ac4e9d1a36d6a9c75b6016b61
```

One of the most effective cracking techniques for reasonably weak passwords in the absense of salt is Google. As expected, it delivers.

![main10-01](/img/hackthis-main/main10-01.png)

So,

```
carl:guess
```
