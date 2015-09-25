---
layout: post
title:  "OverTheWire Wargames :: Bandit :: Levels 0-26"
date:   2015-08-14
---

[OverTheWire: Bandit](http://overthewire.org/wargames/bandit/)

# Level 0

> The goal of this level is for you to log into the game using SSH. The host to which you need to connect is bandit.labs.overthewire.org. The username is bandit0 and the password is bandit0. Once logged in, go to the Level 1 page to find out how to beat Level 1.

About as easy as it gets, log in.

```
otw@iDi:~/bandit$ ssh bandit0@bandit.labs.overthewire.org
The authenticity of host 'bandit.labs.overthewire.org (178.79.134.250)' can't be established.
ECDSA key fingerprint is 05:3a:1c:25:35:0a:ed:2f:cd:87:1c:f6:fe:69:e4:f6.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'bandit.labs.overthewire.org,178.79.134.250' (ECDSA) to the list of known hosts.

This is the OverTheWire game server. More information on http://www.overthewire.org/wargames

[...]

bandit0@melinda:~$ id
uid=11000(bandit0) gid=11000(bandit0) groups=11000(bandit0)
```

# Level 0 > Level 1

> The password for the next level is stored in a file called readme located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH to log into that level and continue the game.

They speak the truth. `cat` it out.

```
bandit0@melinda:~$ ls
readme
bandit0@melinda:~$ cat readme 
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
```

# Level 1 > Level 2

> The password for the next level is stored in a file called - located in the home directory

`-` has special meaning, you can't just `cat` out the file or it will hang waiting for input.

```
bandit1@melinda:~$ cat -
^C
```

Throw in the current directory to overcome this.

```
bandit1@melinda:~$ cat ./-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
```

# Level 2 > Level 3

> The password for the next level is stored in a file called spaces in this filename located in the home directory

Use escape characters for the spaces.

```
bandit2@melinda:~$ ls
spaces in this filename
bandit2@melinda:~$ cat spaces\ in\ this\ filename 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```

# Level 3 > Level 4

> The password for the next level is stored in a hidden file in the inhere directory.

`ls -a` shows hidden files (i.e those that begin with a dot). I'm in the habit of using `ls -alh` to do this, which adds the more detailed format and human-readable file sizes.

```
bandit3@melinda:~$ ls
inhere
bandit3@melinda:~$ cd inhere/
bandit3@melinda:~/inhere$ ls -alh
total 12K
drwxr-xr-x 2 root    root    4.0K Nov 14  2014 .
drwxr-xr-x 3 root    root    4.0K Nov 14  2014 ..
-rw-r----- 1 bandit4 bandit3   33 Nov 14  2014 .hidden
bandit3@melinda:~/inhere$ cat .hidden 
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
```

# Level 4 > Level 5

> The password for the next level is stored in the only human-readable file in the inhere directory. Tip: if your terminal is messed up, try the “reset” command.

The `file` command will do this.

```
bandit4@melinda:~$ ls
inhere
bandit4@melinda:~$ cd inhere/
bandit4@melinda:~/inhere$ ls
-file00  -file01  -file02  -file03  -file04  -file05  -file06  -file07  -file08  -file09
bandit4@melinda:~/inhere$ file *
file: Cannot open `ile00' (No such file or directory).
file: Cannot open `ile01' (No such file or directory).
file: Cannot open `ile02' (No such file or directory).
file: Cannot open `ile03' (No such file or directory).
file: Cannot open `ile04' (No such file or directory).
file: Cannot open `ile05' (No such file or directory).
file: Cannot open `ile06' (No such file or directory).
file: Cannot open `ile07' (No such file or directory).
file: Cannot open `ile08' (No such file or directory).
file: Cannot open `ile09' (No such file or directory).
```

The dash in front of each file name is messing us up again, use `./*` instead.

```
bandit4@melinda:~/inhere$ file ./*
./-file00: data
./-file01: data
./-file02: data
./-file03: data
./-file04: data
./-file05: data
./-file06: data
./-file07: ASCII text
./-file08: data
./-file09: data
bandit4@melinda:~/inhere$ cat ./-file07
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```

Only `-file07` is text, done.

# Level 5 > Level 6

> The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties: - human-readable - 1033 bytes in size - not executable

```
bandit5@melinda:~$ ls
inhere
bandit5@melinda:~$ cd inhere/
bandit5@melinda:~/inhere$ ls
maybehere00  maybehere03  maybehere06  maybehere09  maybehere12  maybehere15  maybehere18
maybehere01  maybehere04  maybehere07  maybehere10  maybehere13  maybehere16  maybehere19
maybehere02  maybehere05  maybehere08  maybehere11  maybehere14  maybehere17
bandit5@melinda:~/inhere$ ls maybehere00
-file1  -file2  -file3  spaces file1  spaces file2  spaces file3
```

There are many directories, each with many files. `find` will recurse into each directory and return files that match the properties we're after.

As it turns out, we don't need to be concerned with the 'human-readable' part because only one file matches the other criteria (with a ton of whitespace added at the end to make the password 1033 bytes).

```
bandit5@melinda:~$ find inhere/ -size 1033c ! -executable
inhere/maybehere07/.file2
bandit5@melinda:~$ cat inhere/maybehere07/.file2
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        bandit5@melinda:~$
```

If that was a concern, we could have used `-exec` which will run a command over the results. 

```
bandit5@melinda:~$ find inhere/ -size 1033c ! -executable -exec file {} \;
inhere/maybehere07/.file2: ASCII text, with very long lines
```

# Level 6 > Level 7

> The password for the next level is stored somewhere on the server and has all of the following properties: - owned by user bandit7 - owned by group bandit6 - 33 bytes in size

`find` to the rescue again. Running `find` over the entire filesystem will inevitably throw a lot of permissions errors as there are plenty of places bandit6 is not allowed access.

```
bandit6@melinda:~$ find / -user bandit7 -group bandit6 -size 33c
find: `/root': Permission denied
find: `/proc/tty/driver': Permission denied
[...]
```

These are written to `stderr` and can be filtered out by dumping `stderr` to `/dev/null`.

```
bandit6@melinda:~$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
/var/lib/dpkg/info/bandit7.password
```

Since we're only expecting to find one file with this search, we could have been extra cute and `cat`'d it out in the same command.

```
bandit6@melinda:~$ cat $(find / -user bandit7 -group bandit6 -size 33c 2>/dev/null)
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
```

# Level 7 > Level 8

> The password for the next level is stored in the file data.txt next to the word millionth

`grep` for the line containing 'millionth.'

```
bandit7@melinda:~$ ls
data.txt
bandit7@melinda:~$ grep millionth data.txt 
millionth	cvX2JJa4CFALtqS87jk27qwqGhBM9plV
```

# Level 8 > Level 9

> The password for the next level is stored in the file data.txt and is the only line of text that occurs only once

```
bandit8@melinda:~$ ls
data.txt
bandit8@melinda:~$ cat data.txt | sort | uniq -u
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
```

The trick here is to know what `uniq` is doing. It does not eliminate duplicates throughout the file, it eliminates duplicate consecutive lines. `sort` makes duplicate entries into neighbors and `uniq -u` takes them out.

```
UNIQ(1)                                           User Commands                                          UNIQ(1)

NAME
       uniq - report or omit repeated lines

SYNOPSIS
       uniq [OPTION]... [INPUT [OUTPUT]]

DESCRIPTION
       Filter adjacent matching lines from INPUT (or standard input), writing to OUTPUT (or standard output).
```

# Level 9 > Level 10

> The password for the next level is stored in the file data.txt in one of the few human-readable strings, beginning with several ‘=’ characters.

`strings` to the rescue.

```
bandit9@melinda:~$ ls
data.txt
bandit9@melinda:~$ strings data.txt | grep =
epr~F=K
7?YD=
?M=HqAH
/(Ne=
C=_"
I========== the6
z5Y=
`h(8=`
n\H=;
========== password
========== ism
N$=&
l/a=L)
f=C(
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
ie)=5e
```

The garbage lines that contain but do not start with '=' can be filtered out with a regular expression matching only lines that begin with an equals sign.

```
bandit9@melinda:~$ strings data.txt | grep '^='  
========== password
========== ism
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
```

# Level 10 > Level 11

> The password for the next level is stored in the file data.txt, which contains base64 encoded data

Decode [base64](https://en.wikipedia.org/wiki/Base64) with the... `base64` command. Excellent work, tool-naming people!

```
bandit10@melinda:~$ ls
data.txt
bandit10@melinda:~$ base64 -d data.txt 
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
```

# Level 11 > Level 12

> The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions

`tr` maps characters from one set into another. Give it the alphabet of lowercase and uppercase letters and map into the alphabets in the wrong order by half (i.e. rot13).

```
bandit11@melinda:~$ ls
data.txt
bandit11@melinda:~$ cat data.txt 
Gur cnffjbeq vf 5Gr8L4qetPEsPk8htqjhRK8XSP6x2RHh
bandit11@melinda:~$ cat data.txt | tr '[a-zA-Z]' '[n-za-mN-ZA-M]'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
```

This example is easier to understand but ridiculous to actually use.

```
bandit11@melinda:~$ cat data.txt | tr 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ' 'nNoOpPqQrRsStTuUvVwWxXyYzZaAbBcCdDeEfFgGhHiIjJkKlLmM'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
```

# Level 12 > Level 13

> The password for the next level is stored in the file data.txt, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work using mkdir. For example: mkdir /tmp/myname123. Then copy the datafile using cp, and rename it using mv (read the manpages!)

Wow, those bastards... this one is pretty hilarious.

I'll need a scratch space for this and since the home directory is wisely not writable, I'll make an oddly-named directory in `/tmp` as advised. We might want to use this in the future with other banditXX users so I'll open up the permissions.

```
bandit12@melinda:~$ mkdir -p /tmp/588e5fd1b
bandit12@melinda:~$ chmod 777 /tmp/588e5fd1b
```

The first file is a hexdump, as expected.

```
bandit12@melinda:/tmp/588e5fd1b$ cp ~/data.txt .
bandit12@melinda:/tmp/588e5fd1b$ file data.txt 
data.txt: ASCII text
bandit12@melinda:/tmp/588e5fd1b$ head data.txt 
0000000: 1f8b 0808 34da 6554 0203 6461 7461 322e  ....4.eT..data2.
0000010: 6269 6e00 013f 02c0 fd42 5a68 3931 4159  bin..?...BZh91AY
0000020: 2653 5982 c194 8a00 0019 ffff dbfb adfb  &SY.............
0000030: bbab b7d7 ffea ffcd fff7 bfbf 1feb eff9  ................
0000040: faab 9fbf fef2 fefb bebf ffff b001 3b18  ..............;.
0000050: 6400 001e a000 1a00 6468 0d01 a064 d000  d.......dh...d..
0000060: 0d00 0034 00c9 a320 001a 0000 0d06 80d1  ...4... ........
0000070: a340 01b4 98d2 3d13 ca20 6803 40d1 a340  .@....=.. h.@..@
0000080: 1a00 0340 0d0d 0000 000d 0c80 6803 4d01  ...@........h.M.
0000090: a3d4 d034 07a8 0683 4d0c 4034 069e 91ea  ...4....M.@4....
```

`xxd -r` will un-hexdump a dump. We'll name the resulting binary data2.bin since we see that in the hexdump.

```
bandit12@melinda:/tmp/588e5fd1b$ xxd -r data.txt > data2.bin
bandit12@melinda:/tmp/588e5fd1b$ file data2.bin 
data2.bin: gzip compressed data, was "data2.bin", from Unix, last modified: Fri Nov 14 10:32:20 2014, max compression
```

Well... here we go. Since `data.txt` gave us `data2.bin` we'll stick with the pattern to avoid confusion (even though it ends up getting confusing anyway). 

```
bandit12@melinda:/tmp/588e5fd1b$ gzip -d data2.bin -c > data3
bandit12@melinda:/tmp/588e5fd1b$ file data3
data3: bzip2 compressed data, block size = 900k
bandit12@melinda:/tmp/588e5fd1b$ bzip2 -d data3 -c > data4
bandit12@melinda:/tmp/588e5fd1b$ file data4
data4: gzip compressed data, was "data4.bin", from Unix, last modified: Fri Nov 14 10:32:20 2014, max compression
bandit12@melinda:/tmp/588e5fd1b$ gzip -d data4 -c > data5
bandit12@melinda:/tmp/588e5fd1b$ file data5
data5: POSIX tar archive (GNU)
bandit12@melinda:/tmp/588e5fd1b$ tar xf data5
bandit12@melinda:/tmp/588e5fd1b$ ls
data.txt  data2.bin  data3  data4  data5  data5.bin
bandit12@melinda:/tmp/588e5fd1b$ file data5.bin 
data5.bin: POSIX tar archive (GNU)
bandit12@melinda:/tmp/588e5fd1b$ tar xf data5.bin
bandit12@melinda:/tmp/588e5fd1b$ ls
data.txt  data2.bin  data3  data4  data5  data5.bin  data6.bin
bandit12@melinda:/tmp/588e5fd1b$ file data6.bin 
data6.bin: bzip2 compressed data, block size = 900k
bandit12@melinda:/tmp/588e5fd1b$ bzip2 -d data6.bin -c > data7
bandit12@melinda:/tmp/588e5fd1b$ file data7
data7: POSIX tar archive (GNU)
bandit12@melinda:/tmp/588e5fd1b$ tar xf data7
bandit12@melinda:/tmp/588e5fd1b$ ls
data.txt  data2.bin  data3  data4  data5  data5.bin  data6.bin  data7  data8.bin
bandit12@melinda:/tmp/588e5fd1b$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", from Unix, last modified: Fri Nov 14 10:32:20 2014, max compression
bandit12@melinda:/tmp/588e5fd1b$ gzip -d data8.bin -c > data9 
bandit12@melinda:/tmp/588e5fd1b$ file data9
data9: ASCII text
bandit12@melinda:/tmp/588e5fd1b$ cat data9
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```

I'm rusty on bash scripts so this might not be stylistically very good, but it does the job. All of the above can be automated with a recursive script. The random file name generation is a cool trick I adapted from StackOverflow.

```
#~/bin/bash

R=$(cat /dev/urandom | tr -cd 'a-zA-Z0-9' | head -c 24)

if [ -f $1 ]
  then
    case $(file $1) in
    *gzip*)
      echo "gzip!"
      gzip -d $1 -c > $R
      ./$0 $R
      ;;
    *bzip2*)
      echo "bzip2!"
      bzip2 -d $1 -c > $R
      ./$0 $R
      ;;
    *POSIX\ tar*)
      echo "tar!"
      tar xOf $1 > $R
      ./$0 $R
      ;;
    *ASCII*)
      echo "ascii!"
      cat $1
      ;;
    esac
fi
```

And... go!

```
bandit12@melinda:/tmp/588e5fd1b$ ./go.sh data2.bin 
gzip!
bzip2!
gzip!
tar!
tar!
bzip2!
tar!
gzip!
ascii!
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```

# Level 13 > Level 14

> The password for the next level is stored in /etc/bandit_pass/bandit14 and can only be read by user bandit14. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Note: localhost is a hostname that refers to the machine you are working on

Indeed, there is an SSH private key waiting for us.

```
bandit13@melinda:~$ ls
sshkey.private
bandit13@melinda:~$ cat sshkey.private 
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtCnEucB9DvN2HZkupc/h6hTKUYLqXuyLD8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----
```

These are usually short enough to copy/paste, but I'll pull it down with `scp` (also WTF private keys in the clipboard) and rename it to something meaningful.

```
bandit13@melinda:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
otw@iDi:~/bandit$ scp bandit13@bandit.labs.overthewire.org:/home/bandit13/sshkey.private ./bandit14

[...]

bandit13@bandit.labs.overthewire.org's password: 
bandit14                                                                       100% 1679     1.6KB/s   00:00
```

SSH keys require restrictive permissions so we'll set that and log in!

```
otw@iDi:~/bandit$ chmod 600 bandit14
otw@iDi:~/bandit$ ssh -i bandit14 bandit14@bandit.labs.overthewire.org

[...]

bandit14@melinda:~$ id
uid=11014(bandit14) gid=11014(bandit14) groups=11014(bandit14)
```

# Level 14 > Level 15

> The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost.

We don't know the password to the current level since we logged in with an SSH key, but the instructions on the opening page of the challenge told us where to find each (with permissions restricted to that user obviously, or this would be pretty easy).

```
bandit14@melinda:~$ cat /etc/bandit_pass/bandit14 
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
```

The password can be sent to the local port using netcat. I prefer to use `ncat` over `nc` because it has many useful additional features bestowed by the Nmap people (the ability to use SSL/TLS being a major plus).

```
bandit14@melinda:~$ ncat -v 127.0.0.1 30000 < /etc/bandit_pass/bandit14
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: Connected to 127.0.0.1:30000.
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr

Ncat: 33 bytes sent, 43 bytes received in 0.03 seconds.
```

It's nice to remember what features are in vanilla `nc` in case that's all you have, though.

```
bandit14@melinda:~$ nc -v 127.0.0.1 30000 < /etc/bandit_pass/bandit14
Connection to 127.0.0.1 30000 port [tcp/*] succeeded!
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
```

# Level 15 > Level 16

> The password for the next level can be retrieved by submitting the password of the current level to port 30001 on localhost using SSL encryption.

`ncat` will handle this nicely, though for some reason our earlier technique does not work with the redirected input.  Instead we'll paste the password into the command line (a HORRIBLE act I was trying to avoid).

```
bandit15@melinda:~$ ncat --ssl -v 127.0.0.1 30001 < /etc/bandit_pass/bandit15
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: SSL connection to 127.0.0.1:30001.
Ncat: SHA-1 fingerprint: 6872 7805 D7EC 03BA 51E2 B301 2651 8989 0556 7D66
Ncat: 33 bytes sent, 0 bytes received in 0.04 seconds.
bandit15@melinda:~$ ncat --ssl -v 127.0.0.1 30001                            
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: SSL connection to 127.0.0.1:30001.
Ncat: SHA-1 fingerprint: 6872 7805 D7EC 03BA 51E2 B301 2651 8989 0556 7D66
BfMYroe26WYalil77FoDi9qh59eK5xNr
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd
^C
```

This can also be done with the `openssl` tools (strange things are amiss if you don't use `-quiet`).

```
bandit15@melinda:~$ cat /etc/bandit_pass/bandit15 | openssl s_client -connect 127.0.0.1:30001 -quiet
depth=0 CN = li190-250.members.linode.com
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = li190-250.members.linode.com
verify return:1
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

read:errno=0
```

# Level 16 > Level 17

> The password for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000 to 32000. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

`nmap` can tell us what ports are open in the range (default SYN scan) and test for SSL\TLS (`ssl-enum-ciphers` script) in one swoop.

```
bandit16@melinda:~$ nmap --script=ssl-enum-ciphers -p 31000-32000 --reason localhost

Starting Nmap 6.40 ( http://nmap.org ) at 2015-08-15 21:41 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up, received syn-ack (0.00080s latency).
Not shown: 996 closed ports
Reason: 996 conn-refused
PORT      STATE SERVICE REASON
31046/tcp open  unknown syn-ack
31518/tcp open  unknown syn-ack
31691/tcp open  unknown syn-ack
31790/tcp open  unknown syn-ack
31960/tcp open  unknown syn-ack

Nmap done: 1 IP address (1 host up) scanned in 0.12 seconds

```

As it turns out, the script doesn't like to execute on ports which are not commonly used with SSL\TLS.  There is a fairly recent topic on this on their github [here](https://github.com/nmap/nmap/issues/168).

Version detection might have some insight.

```
bandit16@melinda:~$ nmap -sV -p 31000-32000 --reason localhost

Starting Nmap 6.40 ( http://nmap.org ) at 2015-08-28 04:59 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up, received syn-ack (0.00087s latency).
Not shown: 996 closed ports
Reason: 996 conn-refused
PORT      STATE SERVICE REASON  VERSION
31046/tcp open  echo    syn-ack
31518/tcp open  msdtc   syn-ack Microsoft Distributed Transaction Coordinator (error)
31691/tcp open  echo    syn-ack
31790/tcp open  msdtc   syn-ack Microsoft Distributed Transaction Coordinator (error)
31960/tcp open  echo    syn-ack
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 41.39 seconds
```

Out of curiosity let's connect to `echo` and see if it's what we'd expect.

```
bandit16@melinda:~$ ncat -v 127.0.0.1 31046   
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: Connected to 127.0.0.1:31046.
balls
balls
^C
``` 

Indeed!  That leaves only two ports that can be checked manually.  I'll guess the second one since I did this already and know the answer. ;)

```
bandit16@melinda:~$ ncat -v --ssl 127.0.0.1 31790                            
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: SSL connection to 127.0.0.1:31790.
Ncat: SHA-1 fingerprint: 6872 7805 D7EC 03BA 51E2 B301 2651 8989 0556 7D66
cluFn7wTiGryunymYOu4RcffSxQluehd
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----
```

# Level 17 > Level 18

> There are 2 files in the homedirectory: passwords.old and passwords.new. The password for the next level is in passwords.new and is the only line that has been changed between passwords.old and passwords.new

Save the key from the previous level on your local machine, fix its permissions for use, and log in.

```
otw@sake:~/bandit$ vim bandit17
[...]
otw@sake:~/bandit$ chmod 600 bandit17
otw@sake:~/bandit$ ssh -i bandit17 bandit17@bandit.labs.overthewire.org
```

There are two text files in the home directory as expected.

```
bandit17@melinda:~$ ls
passwords.new  passwords.old
bandit17@melinda:~$ file *
passwords.new: ASCII text
passwords.old: ASCII text
```

The `diff` command will report differences between them.

```
bandit17@melinda:~$ diff passwords.old passwords.new 
42c42
< BS8bqB1kqkinKJjuxL6k072Qq9NRwQpR
---
> kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
```

# Level 18 > Level 19

> The password for the next level is stored in a file readme in the homedirectory. Unfortunately, someone has modified .bashrc to log you out when you log in with SSH.

Try to log in.

```
otw@sake:~/bandit$ ssh bandit18@bandit.labs.overthewire.org
[...]
Byebye !
Connection to bandit.labs.overthewire.org closed.
```

The login is successful but the connection immediately closes as expected.  A command supplied as an argument to the `ssh` command will execute on the remote system and output to our terminal.  First confirm we can do this by checking that the file we're looking for is present.

```
otw@sake:~/bandit$ ssh bandit18@bandit.labs.overthewire.org ls -lh
[...]
bandit18@bandit.labs.overthewire.org's password: 
total 4.0K
-rw-r----- 1 bandit19 bandit18 33 Nov 14  2014 readme
```

Experiment succesful - `cat` it out.

```
otw@sake:~/bandit$ ssh bandit18@bandit.labs.overthewire.org cat readme
[...]
bandit18@bandit.labs.overthewire.org's password: 
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
```

# Level 19 > Level 20

> To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used to setuid binary.

First confirm the expected.

```
bandit19@melinda:~$ ls -lh
total 8.0K
-rwsr-x--- 1 bandit20 bandit19 7.2K Nov 14  2014 bandit20-do
bandit19@melinda:~$ file bandit20-do 
bandit20-do: setuid ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=08e74b8e092a91103efaab7916d75f08b887ab4d, not stripped
```

Obviously what you should do when given a mysterious executable is run it!  

```
bandit19@melinda:~$ ./bandit20-do 
Run a command as another user.
  Example: ./bandit20-do id
bandit19@melinda:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11020(bandit20),11019(bandit19)
```

Using this command we should be able to `cat` out `/etc/bandit_pass/bandit20` which belongs to bandit20.

```
bandit19@melinda:~$ ls -lh /etc/bandit_pass/bandit20
-r-------- 1 bandit20 bandit20 33 Nov 14  2014 /etc/bandit_pass/bandit20
bandit19@melinda:~$ ./bandit20-do cat !$ 
./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
```

Fun trick, `!$` is shorthand for the last argument of the previous command.

# Level 20 > Level 21

> There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

Recon.

```
bandit20@melinda:~$ ls -lh
total 8.0K
-rwsr-x--- 1 bandit21 bandit20 7.9K Nov 14  2014 suconnect
bandit20@melinda:~$ file suconnect 
suconnect: setuid ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=abcc6c52af9bbea6e735f10665c1095b89c25bd5, not stripped
bandit20@melinda:~$ ./suconnect 
Usage: ./suconnect <portnumber>
This program will connect to the given port on localhost using TCP. If it receives the correct password from the other side, the next password is transmitted back.
```

In one terminal we'll set a `netcat` listener ready to pump out the current password.  I'm in the habit of using `-nlvp` for this to not resolve DNS, listen, be verbose, and finally specify the port.

```
bandit20@melinda:~$ ncat -nlvp 6969 < /etc/bandit_pass/bandit20
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: Listening on :::6969
Ncat: Listening on 0.0.0.0:6969

```

In the second terminal we'll connect using the instructions provided by the usage message.

```
bandit20@melinda:~$ ./suconnect 6969
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
```

Looking back at the listener we see that the connection from `suconnect` sent over a password.

```
bandit20@melinda:~$ ncat -nlvp 6969 < /etc/bandit_pass/bandit20
Ncat: Version 6.40 ( http://nmap.org/ncat )
Ncat: Listening on :::6969
Ncat: Listening on 0.0.0.0:6969
Ncat: Connection from 127.0.0.1.
Ncat: Connection from 127.0.0.1:40249.
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
```

# Level 21 > Level 22

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

Check out `/etc/cron.d`.

```
bandit21@melinda:~$ cd /etc/cron.d
bandit21@melinda:/etc/cron.d$ ls
behemoth4_cleanup  cronjob_bandit24       melinda-stats          natas25_cleanup~  semtex0-32   sysstat
cron-apt           cronjob_bandit24_root  natas-session-toucher  natas26_cleanup   semtex0-64   vortex0
cronjob_bandit22   leviathan5_cleanup     natas-stats            natas27_cleanup   semtex0-ppc  vortex20
cronjob_bandit23   manpage3_resetpw_job   natas25_cleanup        php5              semtex5
```

Presumably we're interested in cronjob_bandit22.

```
bandit21@melinda:/etc/cron.d$ cat cronjob_bandit22
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@melinda:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh 
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

Each time this script executes, a world-readable file is created in `/tmp` by bandit22 which contains bandit22's password.  How handy!

For fun confirm and then `cat` it out.

```
bandit21@melinda:/etc/cron.d$ ls -lh /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
-rw-r--r-- 1 bandit22 bandit22 33 Aug 28 05:42 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@melinda:/etc/cron.d$ cat !$
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
```

# Level 22 > Level 23

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

As usual, first thing is to check it out.

```
bandit22@melinda:~$ cat /etc/cron.d/cronjob_bandit23
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@melinda:~$ cat /usr/bin/cronjob_bandit23.sh 
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

`$myname` will contain bandit23 because that is who invokes the script. `$mytarget` is calculated at runtime.  We'll repeat this step making sure to fill in the correct value for `$myname`.

```
bandit22@melinda:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1 
8ca319486bfbbc3663ea0fbe81326349
```

It's important to understand how the `cut` command works. In this case it cuts (d'oh) the string by spaces and returns the first substring.  We can see this by removing it from the command.

```
bandit22@melinda:~$ echo I am user bandit23 | md5sum 
8ca319486bfbbc3663ea0fbe81326349  -
```

This reveals the secret location in `/tmp` of bandit23's password. Under normal circumstances we could just look in `/tmp` but this machine is configured with specific restrictions.

```
bandit22@melinda:~$ ls -lh /tmp/8ca319486bfbbc3663ea0fbe81326349
-rw-rw-r-- 1 bandit23 bandit23 33 Aug 28 05:49 /tmp/8ca319486bfbbc3663ea0fbe81326349
bandit22@melinda:~$ cat !$
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
```

# Level 23 > Level 24

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

Derp.

```
bandit23@melinda:~$ cat /etc/cron.d/cronjob_bandit24
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@melinda:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
	echo "Handling $i"
	timeout -s 9 60 "./$i"
	rm -f "./$i"
    fi
done
```

The script does exactly as the `echo`'d description claims - running and then deleting all scripts in `/var/spool/bandit24`.  Bonus points for their not allowing infinite loops and the like to run indefinitely using the `timeout` command.

Checking that this directory exists, we see it is writable by us (bandit23) and bandit24.

```
bandit23@melinda:~$ ls -alh /var/spool/bandit24/
total 54K
drwxrwxrwx 2 bandit24 bandit23  49K Aug 28 05:51 .
drwxr-xr-x 6 root     root     4.0K May  3 12:32 ..
```

Since these are executed by bandit24, the most obvious tactic is to drop a script that will output bandit24's password. In order to retrieve it, we'll output to a file in our previously created, world-readable `/tmp` directory.

The script:

```
cat /etc/bandit_pass/bandit24 > /tmp/588e5fd1b/bandit24
```

Create the script, set its permissions as executable, and wait for it to disappear.  A good way to do this is using the `watch` command but that's hard to depict here.

```
bandit23@melinda:/var/spool/bandit24$ vim mmc.sh
[...]
bandit23@melinda:/var/spool/bandit24$ chmod +x mmc.sh 
bandit23@melinda:/var/spool/bandit24$ ls
mmc.sh
bandit23@melinda:/var/spool/bandit24$ ls
mmc.sh
bandit23@melinda:/var/spool/bandit24$ ls
bandit23@melinda:/var/spool/bandit24$
```

Check for output and poof!

```
bandit23@melinda:/var/spool/bandit24$ cat /tmp/588e5fd1b/bandit24
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
```

# Level 24 > Level 25

> A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinaties, called brute-forcing.

For this we'll use the following script.

```
#!/bin/bash

for i in {0000..9999}
do
    echo "$i *************"
    echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i" | ncat 127.0.0.1 30002
done
```

I did not know if `bash` would accept the quadruple 0's, but a quick test on the side shows it works.

The first `echo` is to mark our place in the bruteforce, in case that isn't clear from any output returned by the service.  Run the script and use the `tee` command to output to `stdout` while saving a copy to disk.

```
bandit24@melinda:/tmp/588e5fd1b$ ./bandit25.sh | tee bandit25.out
0000 *************
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct current password. Try again.
Exiting.
0001 *************
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct current password. Try again.
Exiting.
0002 *************
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct current password. Try again.
Exiting.
0003 ***********
[...]
```

I chose this technique because we're bruteforcing over a relatively small space and having all the results for later analysis is powerful. Typically this is not feasible and we'd have to check for the desired output at each iteration in some way. 

Previous levels use "Correct" so we'll search for that.  `grep -C` will display lines adjacent to the match which we'll need since the password isn't on that line.

```
bandit24@melinda:/tmp/588e5fd1b$ grep -C 2 Correct bandit25.out 
5669 *************
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
```

# Level 25 > Level 26

> Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not /bin/bash, but something else. Find out what it is, how it works and how to break out of it.

The shell assigned to a user is stored in `/etc/passwd`.

```
bandit25@melinda:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@melinda:~$ cat /usr/bin/showtext 
#!/bin/sh

more ~/text.txt
exit 0
```

Apparently when bandit26 logs in, instead of getting a a shell a file in bandit26's home directory is `more`'d out.  The 'fairly easy' bit in the level description is a reference to the fact that we are given an ssh key.  Let's try the login.

```
bandit25@melinda:~$ ls
bandit26.sshkey
bandit25@melinda:~$ ssh -i bandit26.sshkey bandit26@localhost
[...]
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
Connection to localhost closed.
```

The fact that the script uses `more` is critial here.  Let's examine the behavior of `more`.

When a file is shorter than the terminal, it is displayed and `more` exits.

![short.txt](/assets/images/otw-bandit/bandit25-01.png)

When a file is longer than the terminal, the portion which fits is displayed and `more` waits for user input to move through the file.

![long.txt](/assets/images/otw-bandit/bandit25-02.png)

During this time if we press the `v` key, `more` will open the file in a text editor.  From the manpage:

```
     v           Start up an editor at current line.  The editor is taken from
                 the environment variable VISUAL if defined, or EDITOR if VIS‐
                 UAL is not defined, or defaults to "vi" if neither VISUAL nor
                 EDITOR is defined.
```

Once in the editor, we can open another file - namely the one which contains bandit26's password!  The trick here is to make our window so small that the login banner exceeds the height of the terminal and `more` waits for input.

![waiting](/assets/images/otw-bandit/bandit25-03.png)

Open the password file from within `vim`.

![open file](/assets/images/otw-bandit/bandit25-04.png)

Boom!

![password](/assets/images/otw-bandit/bandit25-05.png)

5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z

Very creative challenge, really enjoyed getting that one.

# Level 26 > Level 27

> At this moment, level 27 does not exist yet.

Boo.
