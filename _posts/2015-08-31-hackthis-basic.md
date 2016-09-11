---
layout: post
title:  "HackThis!! :: Basic+ :: Levels 1-7"
date:   2015-08-31
---

[HackThis!! Basic+](https://www.hackthis.co.uk/levels/Basic)

# Basic+ Level 1

> Extract the login details from this file: b1.txt

Reading the the file as ASCII produces some unexpected results.

```
hackthis@sake:~$ file b1.txt 
b1.txt: PC bitmap, Windows 3.x format, 213 x 108 x 24
```

Ah, makes sense. Rename the file to b1.bmp (unecessary but then we can open it easily in the desktop environment) and check it out.

![basic01-01](/img/hackthis-basic/basic01-01.png)

# Basic+ Level 2

![basic02-01](/img/hackthis-basic/basic02-01.png)

There are ways to change the user agent in the browser, but I'll use Burp Suite. I prefer to use repeater for this rather than the proxy with intercept since you can take your time crafting your request and don't have to be bothered with anything else that might be pasing through the proxy at the time.

![basic02-02](/img/hackthis-basic/basic02-02.png)

# Basic+ Level 3

![basic03-01](/img/hackthis-basic/basic03-01.png)

At this point I become slightly annoyed that I have to switch over to Win10 (ooh shiny, new) because of the flash content... 

![basic03-02](/img/hackthis-basic/basic03-02.png)

The request is what we'd imagine (and probably should have just guessed). Load it into repeater, change the score, and send it along.

```
POST /levels/b3.php?submit HTTP/1.1
Host: www.hackthis.co.uk
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: <<censored>>
Connection: keep-alive
Content-type: application/x-www-form-urlencoded
Content-Length: 12

score=109384
```

# Basic+ Level 4

> Look at my awesome picture: b4.jpg

I found some info by paging through the output of `strings` after at least minimally confirming the file is in fact an image.

```
hackthis@sake:~$ file b4.jpg 
b4.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=10, orientation=upper-left, xresolution=134, yresolution=142, resolutionunit=2, software=Microsoft Windows Photo Viewer 6.1.7600.16385, datetime=2010:04:28 13:28:38], baseline, precision 8, 364x486, frames 3
hackthis@sake:~$ strings b4.jpg | less
[...]
```

The same could have been done by viewing the metadata in image viewer.

![basic04-01](/img/hackthis-basic/basic04-01.png)

We see that the image is attributed to 'james' and that he loves chocolate.  After some mucking around (e.g. "I like chocolate" as the password), we find the creds - james:chocolate.

# Basic+ Level 5

> Look another picture: b5.jpg

This time nothing intersting is present in the image metadata. There is some unusual text near the end of the file though. We can see this using the `strings` command or `hexdump`.

```
hackthis@sake:~$ strings b5.jpg
[...]
gF!+
28DsZ
eYVXV
secret.txtuser: admin
pass: safePK
secret.txtPK
```

```
hackthis@sake:~$ hexdump -C b5.jpg
[...]
0000aa30  00 00 00 00 00 1d 56 1d  3d a9 a3 4c d6 17 00 00  |......V.=..L....|
0000aa40  00 17 00 00 00 0a 00 00  00 73 65 63 72 65 74 2e  |.........secret.|
0000aa50  74 78 74 75 73 65 72 3a  20 61 64 6d 69 6e 0d 0a  |txtuser: admin..|
0000aa60  70 61 73 73 3a 20 73 61  66 65 50 4b 01 02 14 00  |pass: safePK....|
0000aa70  0a 00 00 00 00 00 1d 56  1d 3d a9 a3 4c d6 17 00  |.......V.=..L...|
0000aa80  00 00 17 00 00 00 0a 00  00 00 00 00 00 00 01 00  |................|
0000aa90  20 00 00 00 00 00 00 00  73 65 63 72 65 74 2e 74  | .......secret.t|
0000aaa0  78 74 50 4b 05 06 00 00  00 00 01 00 01 00 38 00  |xtPK..........8.|
0000aab0  00 00 3f 00 00 00 00 00                           |..?.....|
0000aab8
```

The creds are admin:safe.

# Basic+ Level 6

![basic06-01](/img/hackthis-basic/basic06-01.png)

The IP can be found easily in DNS but beware using 'www' or not! I lost a little bit of time to that.

```
hackthis@sake:~$ nslookup 
> hackthis.co.uk

Name:	hackthis.co.uk
Address: 178.17.41.123
> www.hackthis.co.uk

Name:	www.hackthis.co.uk
Address: 85.159.213.101
```

The hosting company can be found in WHOIS, Linode.

```
hackthis@sake:~$ whois 85.159.213.101
[...]
inetnum:        85.159.208.0 - 85.159.215.255
netname:        EU-LINODE-20050406
descr:          Linode, LLC
country:        GB
```

Lastly, the X-B6-Key. When I first saw that I was pretty sure it isn't... a thing. It looks pretty official though, who knows! As it turns out, this is a header set in your original registration confirmation email from hackthis.co.uk - crazy.

```
[...]
Received: from [85.159.213.101] by mandrillapp.com id 672e060d45e34a87b4aee7e474de093d; Sun, 30 Aug 2015 18:55:12 +0000
X-B6-Key: Lajklsb#!"3jlak
To: 
[...]
```

This is by far my favorite level on HackThis!! to date. The potential for this solution occured to me fairly early since playing with email headers happen to be a recent work-related activity (X-this, X-that) and the X-B6-Key form element mysteriously has id and name 'email.'

```
<label for="user">What is the IP of the server hosting this page:</label>
<input type='Text' autocomplete="off" id='ip' name='ip'><br>
<label for="user">What company hosts our server:</label>
<input type='Text' autocomplete="off" id='host' name='host'><br>
<label for="user">X-B6-Key header:</label>
<input type='Text' autocomplete="off" id='email' name='email'><br>
<input type="submit" class="button" value="Submit">
```

I dismissed it as too bizarre though and wasted a lot of time looking down other avenues. The fact that the answer to a puzzle 16 levels deep is given to everyone at the time of user registration without their knowledge is VERY cool.

# Basic+ Level 7

> We are running a suspicious looking service. Maybe it will give you the answer. 

What service? Let's find out.

```
hackthis@sake:~$ nmap --reason www.hackthis.co.uk

Starting Nmap 6.47 ( http://nmap.org ) at 2015-08-30 23:57 MST
Nmap scan report for www.hackthis.co.uk (85.159.213.101)
Host is up, received syn-ack (0.15s latency).
Not shown: 994 filtered ports
Reason: 994 no-responses
PORT     STATE  SERVICE    REASON
22/tcp   open   ssh        syn-ack
80/tcp   open   http       syn-ack
81/tcp   closed hosts2-ns  conn-refused
443/tcp  open   https      syn-ack
8080/tcp open   http-proxy syn-ack
9050/tcp closed tor-socks  conn-refused

Nmap done: 1 IP address (1 host up) scanned in 8.14 seconds
```

Nothing terrifically suspicious-looking there, maybe we missed it. I'll use `-vv` this time and check any other ports with `ncat` as they're discovered.

```
hackthis@sake:~$ nmap --reason www.hackthis.co.uk -p- -vv

Starting Nmap 6.47 ( http://nmap.org ) at 2015-08-31 00:00 MST
Initiating Ping Scan at 00:00
Scanning www.hackthis.co.uk (85.159.213.101) [2 ports]
Completed Ping Scan at 00:00, 0.15s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 00:00
Completed Parallel DNS resolution of 1 host. at 00:00, 0.00s elapsed
Initiating Connect Scan at 00:00
Scanning www.hackthis.co.uk (85.159.213.101) [65535 ports]
Discovered open port 80/tcp on 85.159.213.101
Discovered open port 443/tcp on 85.159.213.101
Discovered open port 8080/tcp on 85.159.213.101
Discovered open port 22/tcp on 85.159.213.101
Connect Scan Timing: About 23.16% done; ETC: 00:17 (0:13:10 remaining)
Discovered open port 6776/tcp on 85.159.213.101
^C
```

As luck would have it, port 6776 is the magic number and I was able to shut down the scan before completion.

```
hackthis@sake:~$ ncat www.hackthis.co.uk 6776 -v
Ncat: Version 6.47 ( http://nmap.org/ncat )
Ncat: Connected to 85.159.213.101:6776.
Welcome weary traveller. I believe you are looking for this: mapthat
^C
```
