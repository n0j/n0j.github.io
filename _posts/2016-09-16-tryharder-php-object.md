---
layout: post
title:  "Kali Dojo :: PHP Object Challenge"
date:   2016-09-16
---

The following challenge is presumably from the folks at [OffSec](https://www.offensive-security.com/) as I saw it during the small CTF held next to the [Kali Dojo](https://www.kali.org/kali-linux-dojo-workshop/) at Black Hat USA 2016.

Lo, an innocuous-looking HTTP default content page.

![001](/img/tryharder-php-object/try-harder-001.png)

My first thought seeing this is usually that there's some other content either as loose files in the web root, or a site served inside some directory.  After some enumeration and finding nothing, I happen to notice...

![002](/img/tryharder-php-object/try-harder-002.png)

Oh, OK.  Thanks.

The PHP file returns nothing to a standard GET request from a browser, and the text file contains some PHP...

```php
<?php

class TryHarder {
	public $cmd=null;
	public function __destruct() {
		system($this->cmd);
	}
}

$offsec = unserialize($_GET['os']);

?>
```

The `TryHarder` class has a destructor which, for reasons beyond comprehension, executes the contents of the `cmd` member variable.  For folks not familiar with [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming), a constructor is a function which is called automatically when an instance of a class is created and a destructor is a function automatically called when an instance is destroyed.  In PHP these are denoted by `__construct()` and `__destruct()` in the class definition.

`tryharder.php` unserializes an objected passed in by the GET parameter `os`, stores it in the `$offsec` variable, and exits.  [Serialization](http://php.net/manual/en/language.oop5.serialization.php) is a process by which some object is converted into a form which is easily stored or passed.  Take an object, serialize it, put it on the disk or pass it over the network, unserialize it there, and - poof you're got a copy of that object on the other side.

So, we'd like to create an instance of `TryHarder` with some command stored in the `cmd` member variable and serialize it.  When the PHP script ends, the object instance will be destroyed as the program exits, and the destructor will be executed.

We'll URL encode everything to make it friendly just in case.  My script, go.php

```php
<?php

class TryHarder {
    public $cmd=null;
}

$o = new TryHarder();
$o->cmd = 'uname -a';
print urlencode(serialize($o));

?>
```

Note that our local version of the `TryHarder` class does not contain definitions of member functions.  This is intentional as they are not passed along with a serialized object, only the name of the class, member variables and their values, etc.

I tacked the serialized and encoded object into a request and send it out with `curl`.  Building and sending the request could have been down in the script obviously, but this was faster for contest purposes.  

![003](/img/tryharder-php-object/try-harder-003.png)

I did not take a screencap of this during the CTF, the above is a POC running locally on my Kali machine.  At the contest I used the command execution to download a shell, execute it, etc.