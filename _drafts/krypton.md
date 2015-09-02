---
layout: post
title:  "OverTheWire Wargames :: Krypton"
date:   2015-08-25
---

[OverTheWire: Krypton](http://overthewire.org/wargames/krypton/)

# Level 0

> Welcome to Krypton! The first level is easy. The following string encodes the password using Base64:

> S1JZUFRPTklTR1JFQVQ=

> Use this password to log in to krypton.labs.overthewire.org with username krypton1 using SSH. You can find the files for other levels in /krypton/

Indeed.

```
otw@sake:~$ echo S1JZUFRPTklTR1JFQVQ= | base64 -d
KRYPTONISGREAT
```

# Level 0 > Level 1

> The password for level 2 is in the file ‘krypton2’. It is ‘encrypted’ using a simple rotation. It is also in non-standard ciphertext format. When using alpha characters for cipher text it is normal to group the letters into 5 letter clusters, regardless of word boundaries. This helps obfuscate any patterns. This file has kept the plain text word boundaries and carried them to the cipher text. Enjoy!

```
krypton1@melinda:/krypton/krypton1$ cat krypton2 
YRIRY GJB CNFFJBEQ EBGGRA
```

We're basically guaranteed that the rotation is 13 characters, rot13, but for fun we'll check every possible rotation over the capital letters since there aren't very many.

```python
import string

ctext = "YRIRY GJB CNFFJBEQ EBGGRA"
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in range(1,25):
    tab = string.maketrans(alph, alph[i:]+alph[:i])
    print "{:02d}".format(i), ctext.translate(tab)
```

There's certainly some insane way to do this in one line with map, lambda functions, etc... but I'm not that cool right now. [string.maketrans()](https://docs.python.org/2/library/string.html#string.maketrans) [string.translate()](https://docs.python.org/2/library/string.html#string.translate)

```
otw@sake:~$ python krypton2.py 
01 ZSJSZ HKC DOGGKCFR FCHHSB
02 ATKTA ILD EPHHLDGS GDIITC
03 BULUB JME FQIIMEHT HEJJUD
04 CVMVC KNF GRJJNFIU IFKKVE
05 DWNWD LOG HSKKOGJV JGLLWF
06 EXOXE MPH ITLLPHKW KHMMXG
07 FYPYF NQI JUMMQILX LINNYH
08 GZQZG ORJ KVNNRJMY MJOOZI
09 HARAH PSK LWOOSKNZ NKPPAJ
10 IBSBI QTL MXPPTLOA OLQQBK
11 JCTCJ RUM NYQQUMPB PMRRCL
12 KDUDK SVN OZRRVNQC QNSSDM
13 LEVEL TWO PASSWORD ROTTEN
14 MFWFM UXP QBTTXPSE SPUUFO
15 NGXGN VYQ RCUUYQTF TQVVGP
16 OHYHO WZR SDVVZRUG URWWHQ
17 PIZIP XAS TEWWASVH VSXXIR
18 QJAJQ YBT UFXXBTWI WTYYJS
19 RKBKR ZCU VGYYCUXJ XUZZKT
20 SLCLS ADV WHZZDVYK YVAALU
21 TMDMT BEW XIAAEWZL ZWBBMV
22 UNENU CFX YJBBFXAM AXCCNW
23 VOFOV DGY ZKCCGYBN BYDDOX
24 WPGPW EHZ ALDDHZCO CZEEPY
25 XQHQX FIA BMEEIADP DAFFQZ
```

As suspected, 13.

```
ROTTEN
```

# Level 1 > Level 2

> Substitution ciphers are a simple replacement algorithm. In this example of a substitution cipher, we will explore a ‘monoalphebetic’ cipher. Monoalphebetic means, literally, “one alphabet” and you will see why.

> This level contains an old form of cipher called a ‘Caesar Cipher’. A Caesar cipher shifts the alphabet by a set number. For example:

> plain:  a b c d e f g h i j k ...   
> cipher: G H I J K L M N O P Q ...

> In this example, the letter ‘a’ in plaintext is replaced by a ‘G’ in the ciphertext so, for example, the plaintext ‘bad’ becomes ‘HGJ’ in ciphertext.

> The password for level 3 is in the file krypton3. It is in 5 letter group ciphertext. It is encrypted with a Caesar Cipher. Without any further information, this cipher text may be difficult to break. You do not have direct access to the key, however you do have access to a program that will encrypt anything you wish to give it using the key. If you think logically, this is completely easy.

> One shot can solve it!

> Have fun.

```
krypton2@melinda:/tmp/f9b922cd6$ cat krypton3 
OMQEMDUEQMEK
```

Given that this is again a rotation/shifting cypher and that the alphabet is again capital letters, reuse our solution from the previous level.

```
otw@sake:~$ python krypton2.py 
01 PNRFNEVFRNFL
02 QOSGOFWGSOGM
03 RPTHPGXHTPHN
04 SQUIQHYIUQIO
05 TRVJRIZJVRJP
06 USWKSJAKWSKQ
07 VTXLTKBLXTLR
08 WUYMULCMYUMS
09 XVZNVMDNZVNT
10 YWAOWNEOAWOU
11 ZXBPXOFPBXPV
12 AYCQYPGQCYQW
13 BZDRZQHRDZRX
14 CAESARISEASY
15 DBFTBSJTFBTZ
16 ECGUCTKUGCUA
17 FDHVDULVHDVB
18 GEIWEVMWIEWC
19 HFJXFWNXJFXD
20 IGKYGXOYKGYE
21 JHLZHYPZLHZF
22 KIMAIZQAMIAG
23 LJNBJARBNJBH
24 MKOCKBSCOKCI
25 NLPDLCTDPLDJ
```

D'oh. A shift of 14 instead of 13 this time, how exotic! 

```
CAESARISEASY
```

This can also be done the way they suggest, by learning the extent of the shift by supplying a crafted plaintext and observing the ciphertext. Note that the solution above only works because we expect the input text to be human-readable in some fashion. If the input were encoded in some other way the technique below might be the only option. It is also a generally more elegant and powerful technique than a short brute force.

```
krypton2@melinda:/tmp/f9b922cd6$ ln -s /krypton/krypton2/keyfile.dat
krypton2@melinda:/tmp/f9b922cd6$ echo ABCDEFGHIJKLMNOPQRSTUVWXYZ > plaintext
krypton2@melinda:/tmp/f9b922cd6$ /krypton/krypton2/encrypt plaintext 
krypton2@melinda:/tmp/f9b922cd6$ cat ciphertext 
MNOPQRSTUVWXYZABCDEFGHIJKL
```

A to M, 14 characters.

# Level 2 > Level 3

> Well done. You’ve moved past an easy substitution cipher.

> The main weakness of a simple substitution cipher is repeated use of a simple key. In the previous exercise you were able to introduce arbitrary plaintext to expose the key. In this example, the cipher mechanism is not available to you, the attacker.

> However, you have been lucky. You have intercepted more than one message. The password to the next level is found in the file ‘krypton4’. You have also found 3 other files. (found1, found2, found3)

> You know the following important details:

> The message plaintexts are in English (*** very important) - They were produced from the same key (*** even better!)

> Enjoy.

```
krypton3@melinda:~$ cd /krypton/krypton3/
krypton3@melinda:/krypton/krypton3$ ls
HINT1  HINT2  README  found1  found2  found3  krypton4
krypton3@melinda:/krypton/krypton3$ cat krypton4 
KSVVW BGSJD SVSIS VXBMN YQUUK BNWCU ANMJS
```

Each of the 'found' files is a reasonably large sample ciphertext.

```
krypton3@melinda:/krypton/krypton3$ cat found1
CGZNL YJBEN QYDLQ ZQSUQ NZCYD SNQVU BFGBK GQUQZ QSUQN UZCYD SNJDS UDCXJ ZCYDS NZQSU QNUZB WSBNZ QSUQN UDCXJ CUBGS BXJDS UCTYV SUJQG WTBUJ KCWSV LFGBK GSGZN LYJCB GJSZD GCHMS UCJCU QJLYS BXUMA UJCJM JCBGZ CYDSN CGKDC ZDSQZ DVSJJ SNCGJ DSYVQ CGJSO JCUNS YVQZS WALQV SJJSN UBTSX COSWG MTASN BXYBU CJCBG UWBKG JDSQV YDQAS JXBNS OQTYV SKCJD QUDCX JBXQK BMVWA SNSYV QZSWA LWAKB MVWAS ZBTSS QGWUB BGJDS TSJDB WCUGQ TSWQX JSNRM VCMUZ QSUQN KDBMU SWCJJ BZBTT MGCZQ JSKCJ DDCUE SGSNQ VUJDS SGZNL YJCBG UJSYY SNXBN TSWAL QZQSU QNZCY DSNCU BXJSG CGZBN YBNQJ SWQUY QNJBX TBNSZ BTYVS OUZDS TSUUM ZDQUJ DSICE SGNSZ CYDSN QGWUJ CVVDQ UTBWS NGQYY VCZQJ CBGCG JDSNB JULUJ STQUK CJDQV VUCGE VSQVY DQASJ UMAUJ CJMJC BGZCY DSNUJ DSZQS UQNZC YDSNC USQUC VLANB FSGQG WCGYN QZJCZ SBXXS NUSUU SGJCQ VVLGB ZBTTM GCZQJ CBGUS ZMNCJ LUDQF SUYSQ NSYNB WMZSW TBUJB XDCUF GBKGK BNFAS JKSSG QGWDC USQNV LYVQL UKSNS TQCGV LZBTS WCSUQ GWDCU JBNCS UESGN SUDSN QCUSW JBJDS YSQFB XUBYD CUJCZ QJCBG QGWQN JCUJN LALJD SSGWB XJDSU COJSS GJDZS GJMNL GSOJD SKNBJ STQCG VLJNQ ESWCS UMGJC VQABM JCGZV MWCGE DQTVS JFCGE VSQNQ GWTQZ ASJDZ BGUCW SNSWU BTSBX JDSXC GSUJS OQTYV SUCGJ DSSGE VCUDV QGEMQ ESCGD CUVQU JYDQU SDSKN BJSJN QECZB TSWCS UQVUB FGBKG QUNBT QGZSU QGWZB VVQAB NQJSW KCJDB JDSNY VQLKN CEDJU TQGLB XDCUY VQLUK SNSYM AVCUD SWCGS WCJCB GUBXI QNLCG EHMQV CJLQG WQZZM NQZLW MNCGE DCUVC XSJCT SQGWC GJKBB XDCUX BNTSN JDSQJ NCZQV ZBVVS QEMSU YMAVC UDSWJ DSXCN UJXBV CBQZB VVSZJ SWSWC JCBGB XDCUW NQTQJ CZKBN FUJDQ JCGZV MWSWQ VVAMJ JKBBX JDSYV QLUGB KNSZB EGCUS WQUUD QFSUY SQNSU
```

The hints tell you to use frequency analysis, already pretty strongly hinted at by the setup.

I joined these three files into one and removed the spaces to make the set easier to work with.

```
krypton3@melinda:/tmp/f9b922cd6$ cat found
CGZNLYJBENQYDLQZQSUQNZCYDSNQVUBFGBKGQUQZQSUQNUZCYDSNJDSUDCXJZCYDSNZQSUQNUZBWSBNZQSUQNUDCXJCUBGSBXJDSUCTYVSUJQGWTBUJKCWSVLFGBKGSGZNLYJCBGJSZDGCHMSUCJCUQJLYSBXUMAUJCJMJCBGZCYDSNCGKDCZDSQZDVSJJSNCGJDSYVQCGJSOJCUNSYVQZSWALQVSJJSNUBTSXCOSWGMTASNBXYBUCJCBGUWBKGJDSQVYDQASJXBNSOQTYVSKCJDQUDCXJBXQKBMVWASNSYVQZSWALWAKBMVWASZBTSSQGWUBBGJDSTSJDBWCUGQTSWQXJSNRMVCMUZQSUQNKDBMUSWCJJBZBTTMGCZQJSKCJDDCUESGSNQVUJDSSGZNLYJCBGUJSYYSNXBNTSWALQZQSUQNZCYDSNCUBXJSGCGZBNYBNQJSWQUYQNJBXTBNSZBTYVSOUZDSTSUUMZDQUJDSICESGNSZCYDSNQGWUJCVVDQUTBWSNGQYYVCZQJCBGCGJDSNBJULUJSTQUKCJDQVVUCGEVSQVYDQASJUMAUJCJMJCBGZCYDSNUJDSZQSUQNZCYDSNCUSQUCVLANBFSGQGWCGYNQZJCZSBXXSNUSUUSGJCQVVLGBZBTTMGCZQJCBGUSZMNCJLUDQFSUYSQNSYNBWMZSWTBUJBXDCUFGBKGKBNFASJKSSGQGWDCUSQNVLYVQLUKSNSTQCGVLZBTSWCSUQGWDCUJBNCSUESGNSUDSNQCUSWJBJDSYSQFBXUBYDCUJCZQJCBGQGWQNJCUJNLALJDSSGWBXJDSUCOJSSGJDZSGJMNLGSOJDSKNBJSTQCGVLJNQESWCSUMGJCVQABMJCGZVMWCGEDQTVSJFCGEVSQNQGWTQZASJDZBGUCWSNSWUBTSBXJDSXCGSUJSOQTYVSUCGJDSSGEVCUDVQGEMQESCGDCUVQUJYDQUSDSKNBJSJNQECZBTSWCSUQVUBFGBKGQUNBTQGZSUQGWZBVVQABNQJSWKCJDBJDSNYVQLKNCEDJUTQGLBXDCUYVQLUKSNSYMAVCUDSWCGSWCJCBGUBXIQNLCGEHMQVCJLQGWQZZMNQZLWMNCGEDCUVCXSJCTSQGWCGJKBBXDCUXBNTSNJDSQJNCZQVZBVVSQEMSUYMAVCUDSWJDSXCNUJXBVCBQZBVVSZJSWSWCJCBGBXDCUWNQTQJCZKBNFUJDQJCGZVMWSWQVVAMJJKBBXJDSYVQLUGBKNSZBEGCUSWQUUDQFSUYSQNSU
QVJDBMEDGBQJJSGWQGZSNSZBNWUXBNJDSYSNCBWUMNICISTBUJACBENQYDSNUQENSSJDQJUDQFSUYSQNSKQUSWMZQJSWQJJDSFCGEUGSKUZDBBVCGUJNQJXBNWQXNSSUZDBBVZDQNJSNSWCGQABMJQHMQNJSNBXQTCVSXNBTDCUDBTSENQTTQNUZDBBVUIQNCSWCGHMQVCJLWMNCGEJDSSVCPQASJDQGSNQAMJJDSZMNNCZMVMTKQUWCZJQJSWALVQKJDNBMEDBMJSGEVQGWQGWJDSUZDBBVKBMVWDQISYNBICWSWQGCGJSGUCISSWMZQJCBGCGVQJCGENQTTQNQGWJDSZVQUUCZUQJJDSQESBXUDQFSUYSQNSTQNNCSWJDSLSQNBVWQGGSDQJDQKQLJDSZBGUCUJBNLZBMNJBXJDSWCBZSUSBXKBNZSUJSNCUUMSWQTQNNCQESVCZSGZSBGGBISTASNJKBBXDQJDQKQLUGSCEDABMNUYBUJSWABGWUJDSGSOJWQLQUUMNSJLJDQJJDSNSKSNSGBCTYSWCTSGJUJBJDSTQNNCQESJDSZBMYVSTQLDQISQNNQGESWJDSZSNSTBGLCGUBTSDQUJSUCGZSJDSKBNZSUJSNZDQGZSVVBNQVVBKSWJDSTQNNCQESAQGGUJBASNSQWBGZSCGUJSQWBXJDSMUMQVJDNSSJCTSUQGGSUYNSEGQGZLZBMVWDQISASSGJDSNSQUBGXBNJDCUUCOTBGJDUQXJSNJDSTQNNCQESUDSEQISACNJDJBQWQMEDJSNUMUQGGQKDBKQUAQYJCUSWBGTQLJKCGUUBGDQTGSJQGWWQMEDJSNRMWCJDXBVVBKSWQVTBUJJKBLSQNUVQJSNQGWKSNSAQYJCUSWBGXSANMQNLDQTGSJWCSWBXMGFGBKGZQMUSUQJJDSQESBXQGWKQUAMNCSWBGQMEMUJQXJSNJDSACNJDBXJDSJKCGUJDSNSQNSXSKDCUJBNCZQVJNQZSUBXUDQFSUYSQNSMGJCVDSCUTSGJCBGSWQUYQNJBXJDSVBGWBGJDSQJNSUZSGSCGASZQMUSBXJDCUEQYUZDBVQNUNSXSNJBJDSLSQNUASJKSSGQGWQUUDQFSUYSQNSUVBUJLSQNUACBENQYDSNUQJJSTYJCGEJBQZZBMGJXBNJDCUYSNCBWDQISNSYBNJSWTQGLQYBZNLYDQVUJBNCSUGCZDBVQUNBKSUDQFSUYSQNSUXCNUJACBENQYDSNNSZBMGJSWQUJNQJXBNWVSESGWJDQJUDQFSUYSQNSXVSWJDSJBKGXBNVBGWBGJBSUZQYSYNBUSZMJCBGXBNWSSNYBQZDCGEQGBJDSNSCEDJSSGJDZSGJMNLUJBNLDQUUDQFSUYSQNSUJQNJCGEDCUJDSQJNCZQVZQNSSNTCGWCGEJDSDBNUSUBXJDSQJNSYQJNBGUCGVBGWBGRBDGQMANSLNSYBNJSWJDQJUDQFSUYSQNSDQWASSGQZBMGJNLUZDBBVTQUJSNUBTSJKSGJCSJDZSGJMNLUZDBVQNUDQISUMEESUJSWJDQJUDQFSUYSQNSTQLDQISASSGSTYVBLSWQUQUZDBBVTQUJSNALQVSOQGWSNDBEDJBGBXVQGZQUDCNSQZQJDBVCZVQGWBKGSNKDBGQTSWQZSNJQCGKCVVCQTUDQFSUDQXJSCGDCUKCVVGBSICWSGZSUMAUJQGJCQJSUUMZDUJBNCSUBJDSNJDQGDSQNUQLZBVVSZJSWQXJSNDCUWSQJD
DSNSMYBGVSENQGWQNBUSKCJDQENQISQGWUJQJSVLQCNQGWANBMEDJTSJDSASSJVSXNBTQEVQUUZQUSCGKDCZDCJKQUSGZVBUSWCJKQUQASQMJCXMVUZQNQAQSMUQGWQJJDQJJCTSMGFGBKGJBGQJMNQVCUJUBXZBMNUSQENSQJYNCPSCGQUZCSGJCXCZYBCGJBXICSKJDSNSKSNSJKBNBMGWAVQZFUYBJUGSQNBGSSOJNSTCJLBXJDSAQZFQGWQVBGEBGSGSQNJDSBJDSNJDSUZQVSUKSNSSOZSSWCGEVLDQNWQGWEVBUULKCJDQVVJDSQYYSQNQGZSBXAMNGCUDSWEBVWJDSKSCEDJBXJDSCGUSZJKQUISNLNSTQNFQAVSQGWJQFCGEQVVJDCGEUCGJBZBGUCWSNQJCBGCZBMVWDQNWVLAVQTSRMYCJSNXBNDCUBYCGCBGNSUYSZJCGECJ
```

# Level 3 > Level 4

> Good job!

> You more than likely used some form of FA and some common sense to solve that one.

> So far we have worked with simple substitution ciphers. They have also been ‘monoalphabetic’, meaning using a fixed key, and giving a one to one mapping of plaintext (P) to ciphertext (C). Another type of substitution cipher is referred to as ‘polyalphabetic’, where one character of P may map to many, or all, possible ciphertext characters.

> An example of a polyalphabetic cipher is called a Vigenère Cipher. It works like this:

> If we use the key(K) ‘GOLD’, and P = PROCEED MEETING AS AGREED, then “add” P to K, we get C. When adding, if we exceed 25, then we roll to 0 (modulo 26).

``P P R O C E E D M E E T I N G A S A G R E E D\``   
``K G O L D G O L D G O L D G O L D G O L D G O\``   

> becomes:


``P 15 17 14 2 4 4 3 12 4 4 19 8 13 6 0 18 0 6 17 4 4 3\``   
``K 6 14 11 3 6 14 11 3 6 14 11 3 6 14 11 3 6 14 11 3 6 14\``   
``C 21 5 25 5 10 18 14 15 10 18 4 11 19 20 11 21 6 20 2 8 10 17\``   


> So, we get a ciphertext of:

``VFZFK SOPKS ELTUL VGUCH KR``

> This level is a Vigenère Cipher. You have intercepted two longer, english language messages. You also have a key piece of information. You know the key length!

> For this exercise, the key length is 6. The password to level five is in the usual place, encrypted with the 6 letter key.

> Have fun!

# Level 4 > Level 5

> FA can break a known key length as well. Lets try one last polyalphabetic cipher, but this time the key length is unknown.

> Enjoy.

# Level 5 > Level 6

> Hopefully by now its obvious that encryption using repeating keys is a bad idea. Frequency analysis can destroy repeating/fixed key substitution crypto.
> 
> A feature of good crypto is random ciphertext. A good cipher must not reveal any clues about the plaintext. Since natural language plaintext (in this case, English) contains patterns, it is left up to the encryption key or the encryption algorithm to add the ‘randomness’.
> 
> Modern ciphers are similar to older plain substitution ciphers, but improve the ‘random’ nature of the key.
> 
> An example of an older cipher using a complex, random, large key is a vigniere using a key of the same size of the plaintext. For example, imagine you and your confident have agreed on a key using the book ‘A Tale of Two Cities’ as your key, in 256 byte blocks.
> 
> The cipher works as such:
> 
> Each plaintext message is broken into 256 byte blocks. For each block of plaintext, a corresponding 256 byte block from the book is used as the key, starting from the first chapter, and progressing. No part of the book is ever re-used as key. The use of a key of the same length as the plaintext, and only using it once is called a “One Time Pad”.
> 
> Look in the krypton6 directory. You will find a file called ‘plain1’, a 256 byte block. You will also see a file ‘key1’, the first 256 bytes of ‘A Tale of Two Cities’. The file ‘cipher1’ is the cipher text of plain1. As you can see (and try) it is very difficult to break the cipher without the key knowledge.
> 
> (NOTE - it is possible though. Using plain language as a one time pad key has a weakness. As a secondary challenge, open README2)
> 
> If the encryption is truly random letters, and only used once, then it is impossible to break. A truly random “One Time Pad” key cannot be broken. Consider intercepting a ciphertext message of 1000 bytes. One could brute force for the key, but due to the random key nature, you would produce every single valid 1000 letter plaintext as well. Who is to know which is the real plaintext?!?
> 
> Choosing keys that are the same size as the plaintext is impractical. Therefore, other methods must be used to obscure ciphertext against frequency analysis in a simple substitution cipher. The impracticality of an ‘infinite’ key means that the randomness, or entropy, of the encryption is introduced via the method.
> 
> We have seen the method of ‘substitution’. Even in modern crypto, substitution is a valid technique. Another technique is ‘transposition’, or swapping of bytes.
> 
> Modern ciphers break into two types; symmetric and asymmetric.
> 
> Symmetric ciphers come in two flavours: block and stream.
> 
> Until now, we have been playing with classical ciphers, approximating ‘block’ ciphers. A block cipher is done in fixed size blocks (suprise!). For example, in the previous paragraphs we discussed breaking text and keys into 256 byte blocks, and working on those blocks. Block ciphers use a fixed key to perform substituion and transposition ciphers on each block discretely.
> 
> Its time to employ a stream cipher. A stream cipher attempts to create an on-the-fly ‘random’ keystream to encrypt the incoming plaintext one byte at a time. Typically, the ‘random’ key byte is xor’d with the plaintext to produce the ciphertext. If the random keystream can be replicated at the recieving end, then a further xor will produce the plaintext once again.
> 
> From this example forward, we will be working with bytes, not ASCII text, so a hex editor/dumper like hexdump is a necessity. Now is the right time to start to learn to use tools like cryptool.
> 
> In this example, the keyfile is in your directory, however it is not readable by you. The binary ‘encrypt6’ is also available. It will read the keyfile and encrypt any message you desire, using the key AND a ‘random’ number. You get to perform a ‘known ciphertext’ attack by introducing plaintext of your choice. The challenge here is not simple, but the ‘random’ number generator is weak.
> 
> As stated, it is now that we suggest you begin to use public tools, like cryptool, to help in your analysis. You will most likely need a hint to get going. See ‘HINT1’ if you need a kicktstart.
> 
> If you have further difficulty, there is a hint in ‘HINT2’.
> 
> The password for level 7 (krypton7) is encrypted with ‘encrypt6’.
> 
> Good Luck!
