---
layout: post
title:  "OverTheWire Wargames - Bandit"
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

```sh
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




