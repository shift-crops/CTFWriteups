#!/usr/bin/php-cgi
<?php

if (isset($_GET['source']))
{
   show_source(__FILE__);
   exit();
}

$link = mysqli_connect('127.0.0.1:3306', 'user', 'pass', 'test');

//sleep(300);


$fh = fopen('php://stdin', 'r');
$input = fread($fh, 1000);

shellme($input);
exit();


?>

<html>

<form action="index.php" method=POST>
shell <input type=text name=shell required><br>
<input type=submit value="shell me">
</form>

<a href="?source">debug me</a> <br>

</html>
