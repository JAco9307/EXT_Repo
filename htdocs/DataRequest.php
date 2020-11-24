<?php
$myfile = fopen("CranePos.txt", "r");
echo fgets($myfile);
fclose($myfile);
?>
