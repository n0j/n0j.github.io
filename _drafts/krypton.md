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

# Level 0 > Level 1

> The password for level 2 is in the file ‘krypton2’. It is ‘encrypted’ using a simple rotation. It is also in non-standard ciphertext format. When using alpha characters for cipher text it is normal to group the letters into 5 letter clusters, regardless of word boundaries. This helps obfuscate any patterns. This file has kept the plain text word boundaries and carried them to the cipher text. Enjoy!

# Level 1 > Level 2

> Substitution ciphers are a simple replacement algorithm. In this example of a substitution cipher, we will explore a ‘monoalphebetic’ cipher. Monoalphebetic means, literally, “one alphabet” and you will see why.

> This level contains an old form of cipher called a ‘Caesar Cipher’. A Caesar cipher shifts the alphabet by a set number. For example:

> plain:  a b c d e f g h i j k ...   
> cipher: G H I J K L M N O P Q ...

> In this example, the letter ‘a’ in plaintext is replaced by a ‘G’ in the ciphertext so, for example, the plaintext ‘bad’ becomes ‘HGJ’ in ciphertext.

> The password for level 3 is in the file krypton3. It is in 5 letter group ciphertext. It is encrypted with a Caesar Cipher. Without any further information, this cipher text may be difficult to break. You do not have direct access to the key, however you do have access to a program that will encrypt anything you wish to give it using the key. If you think logically, this is completely easy.

> One shot can solve it!

> Have fun.

# Level 2 > Level 3

> Well done. You’ve moved past an easy substitution cipher.

> The main weakness of a simple substitution cipher is repeated use of a simple key. In the previous exercise you were able to introduce arbitrary plaintext to expose the key. In this example, the cipher mechanism is not available to you, the attacker.

> However, you have been lucky. You have intercepted more than one message. The password to the next level is found in the file ‘krypton4’. You have also found 3 other files. (found1, found2, found3)

> You know the following important details:

> The message plaintexts are in English (*** very important) - They were produced from the same key (*** even better!)

> Enjoy.

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
