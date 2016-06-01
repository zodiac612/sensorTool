<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Overview</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body>\n";

include 'top_menue.php';
//include 'precheck.php';

echo "<h3>Raspberry PI SensorTool Status<BR />". date("d.m.Y",time())."</h3>\n";
echo "<BR />\n";

echo "<table><TR><TD>\n";
echo "<img class=\"chart \" alt=\"Line chart\" src=\"Bad.png\" />\n";
echo "</TD><TD>\n";
echo "<img class=\"chart \" alt=\"Line chart\" src=\"EG.png\" />\n";
echo "</TD></TR><TR><TD>\n";
echo "<img class=\"chart \" alt=\"Line chart\" src=\"Aussen.png\" />\n";
echo "</TD><TD>\n";
echo "<img class=\"chart \"alt=\"Line chart\" src=\"Hasen.png\" />\n";
echo "</TD></TR><TR><TD>\n";
echo "<img class=\"chart \" alt=\"Line chart\" src=\"Keller.png\" />\n";
echo "</TD><TD>\n";
echo "<img class=\"chart \"alt=\"Line chart\" src=\"WC.png\" />\n";
echo "</TD></TR></table>\n";

echo "</body>\n";
?>
