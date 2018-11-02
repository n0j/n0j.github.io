---
layout: post
title:  "OWASP Juice Shop v7.3.0 - Level 2"
date:   2018-08-01
---

[OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project)

![level 2](/img/owasp-juice-shop-v7.3.0/juice016.png)

## Basket Access

> Access someone else's basket.

Pretty simple, when you click on your basket a request goes out like this,

```
GET /rest/basket/5 HTTP/1.1
[...]
```

Intercept and modify the request or modify and replay the request (with headers, there's some authorization here) with a value other than 5.

![basket](/img/owasp-juice-shop-v7.3.0/juice017.png)

## Christmas Special

> Order the Christmas special offer of 2014.

Earlier I noticed that juice-shop.min.js contains an occasionally hilarious nesting of `catch` statements and logging to the JS console. For instance, from the `SearchResultController` controller,

```
              }).catch (function (e) {
                console.log(e)
              })
            }).catch (function (e) {
              console.log(e)
            })
          }).catch (function (e) {
            console.log(e)
```

I've kept the console open hoping to catch such output and it was indispensable for this challenge. Submitting a single tick to a search box is on the "definitely always try it" list but it didn't work here. A single tick followed by practically anything, however, throws a nice SQLite error into the console. A search for `'foo`, for example...

![sqlite](/img/owasp-juice-shop-v7.3.0/juice018.png)

So we know we're working with the following SQL statement, where `<>` is the user input.

```
SELECT * FROM Products WHERE ((name LIKE '%<>%' OR description LIKE '%<>%') AND deletedAt IS NULL) ORDER BY name
```

We'd like to remove the part about `deletedAt`, with the hopes that 'deleted' items are actually still in the database just with this column as a non-null to mark removal. Even better, it would be great if the 2014 Christmas product is such an item.

A tick to close the quotes and two parenthesis to close them. Follow with a comment to get rid of the rest, like this `'))--`.


The database receives this pile of weirdness,

```
SELECT * FROM Products WHERE ((name LIKE '%'))--%' OR description LIKE '%'))--%') AND deletedAt IS NULL) ORDER BY name
```

But only cares about,

```
SELECT * FROM Products WHERE ((name LIKE '%'))
```

Sure enough, in the results page after searching `'))--`,

![christmas](/img/owasp-juice-shop-v7.3.0/juice019.png)

The normal buttons on the product listing are broken and we can't click to add it to the cart. To feel out adding it by another means, observe the request when a regular item is added.

```
POST /api/BasketItems/ HTTP/1.1
[...]

{"ProductId":1,"BasketId":"5","quantity":1}
```

So, we might just need the ProductId of the Christmas item. Looking back at the search results, the item above is #9, the item below doesn't work either, and the one below that is #12. Maybe it's just 9, 10 (xmas), 11, 12? Replaying the above POST with a ProductID of 10 - bingo.

![christmas](/img/owasp-juice-shop-v7.3.0/juice020.png)

From here the basket appears to function normally and an invoice is generated after clicking the checkout button.

![christmas](/img/owasp-juice-shop-v7.3.0/juice021.png)

![christmas](/img/owasp-juice-shop-v7.3.0/juice022.png)

## Deprecated Interface

> Use a deprecated B2B interface that was not properly shut down.

Solving this one relies totally on having done a thorough job clicking through the application and looking at the source of each page. On the complaint form, the file uploader has some attributes set to '.pdf' but '.pdf,.xml' on another.

```
<input ngf-select="" ng-model="file" id="file" name="file" ngf-pattern="'.pdf,.xml'" ngf-accept="'.pdf'" ngf-max-size="100KB" class="ng-pristine ng-untouched ng-valid ng-empty" accept=".pdf" type="file">
```

The end result is that the file selection dialog which opens is limited to PDF files by default, but the server accepts PDF or XML submissions.

![b2b](/img/owasp-juice-shop-v7.3.0/juice025.png)

Using my favorite sad test file,

![b2b](/img/owasp-juice-shop-v7.3.0/juice026.png)

The upload succeeds and triggers challenge completion.

![b2b](/img/owasp-juice-shop-v7.3.0/juice027.png)

## Five-Star Feedback

> Get rid of all 5-star customer feedback.

![review](/img/owasp-juice-shop-v7.3.0/juice023.png)

Not much going on here. Go to the admin page we found in level 1 at `/#/administration` and click to delete the 5-star reviews. There were only a few for me and I think most were from my own experimenting earlier.

![review](/img/owasp-juice-shop-v7.3.0/juice024.png)

## Login Admin

> Log in with the administrator's user account.

We know the administrator's email address from the previously discovered admin page.

![admin](/img/owasp-juice-shop-v7.3.0/juice028.png)

This challenge was a good lesson in thinking about assumptions and getting stuck with tunnel vision. Because I had the email address, I focused all effort on finding some kind of injection in the password field only. This ended up being totally fruitless and I wasted a bunch of time without even an error response to show for it. The simplest possible trick in the email field is all I needed - the classic single tick.

![admin](/img/owasp-juice-shop-v7.3.0/juice029.png)

We can see why injecting the password field failed; the password appears to be hashed by the client before inclusion in SQL. D'oh.

```
SELECT * FROM Users WHERE email = '<user>' AND password = '<hash>'
```

There's not much we can do with the password field being hashed. Whatever value we enter, the SQL server is just going to get a string of letters and numbers. We can try getting rid of the statement after the username with a comment, though, with the username `admin@juice-sh.op'--` and any password.

![admin](/img/owasp-juice-shop-v7.3.0/juice030.png)

## Login MC SafeSearch

> Log in with MC SafeSearch's original user credentials without applying SQL Injection or any other bypass.

The hovertext hint on the scoreboard has you find this pretty amazing YouTube video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/v59CX2DiX0Y?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

First time through this caught my eye, but it doesn't work.

![mc](/img/owasp-juice-shop-v7.3.0/juice031.png)

After a more careful listening, he says his password is the name of his dog, Mr. Noodles, and that he likes to change out O's for zeros. I'd been using Burp Repeater to make guesses, eventually...

```
POST /rest/user/login HTTP/1.1
[...]

{"email":"mc.safesearch@juice-sh.op","password":"Mr. N00dles"}
```

![mc](/img/owasp-juice-shop-v7.3.0/juice032.png)

## Password Strength

> Log in with the administrator's user credentials without previously changing them or applying SQL Injection.

I was not able to guess this one and the password did not appear in the Burp list, Nmap list, or the first 50K or so entries of the rockyou list. So much for easily brute-forced or guessed, oops.

Finding the hash turned out to be very easy.

![hash](/img/owasp-juice-shop-v7.3.0/juice036.png)

The request which populates the information above looks like this.

```
GET /api/Users/1 HTTP/1.1
[...]
```

And the response,

```
HTTP/1.1 200 OK
[...]

{"status":"success","data":{"id":1,"email":"admin@juice-sh.op","password":"0192023a7bbd73250516f069df18b500","createdAt":"2018-08-01T17:33:44.292Z","updatedAt":"2018-08-01T17:33:44.292Z"}}
```

The best way to crack easy hashes is by Google'ing them and we find that 'admin123' has the MD5 hash 0192023a7bbd73250516f069df18b500.

![security.txt](/img/owasp-juice-shop-v7.3.0/juice037.png)

Out of curiosity I looked in rockyou and was surprised how far down the list the first three of these are.

```
root@kali /u/s/wordlists# grep -n admin123 rockyou.txt 
90006:admin123
318348:admin1234
701602:admin123456
3031689:tvadmin123
4992710:ntadmin1234
7946967:gasoadmin123
10357626:admin123bob
10357627:admin1232
10357628:admin1230
10357629:admin123*
```

## Security Policy

> Behave like any "white-hat" should.

Access the site's security.txt file. Looking at [securitytxt.org](https://securitytxt.org/), I wasn't aware you're supposed to put things in a `.well-known` directory, fortunately for me this is not the case in Juice Shop.

![security.txt](/img/owasp-juice-shop-v7.3.0/juice033.png)

![security.txt](/img/owasp-juice-shop-v7.3.0/juice034.png)

## Weird Crypto

> Inform the shop about an algorithm or library it should definitely not use the way it does.

I submitted the comment "MD5 is shit!" and well, yea that did it.

![security.txt](/img/owasp-juice-shop-v7.3.0/juice035.png)