<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

include 'conf.php';
include 'functions.php';

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Status</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"styledisplay.css\">";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body width=\"470px\">\n";

$vMenueFrame = 'index';
include 'top_menue.php';

//include 'precheck.php';

echo "<h3>Raspberry PI SensorTool Status<BR />". date("d.m.Y",time())."</h3>\n";
//echo "<BR />\n";

//include 'webradio_short.php';
//if ( $boolLCL ) {
//}
include 'loglatestentry.php';

echo "<BR />\n";

$vSensor_Frame = 'index';
include 'sensor.php';

echo "<BR />\n";

include 'logdata.php';

echo "</body>\n";
?>
