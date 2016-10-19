<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

include 'conf.php';

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI picam</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body bgcolor=\"#CCCCCC\">\n";

$vMenueFrame = 'picam';
include 'top_menue.php';
include 'precheck.php';


	echo "  <BR />\n";
    echo "<table class=\"overview\">\n";
    echo "<TR>\n";
    echo "<TD class=\"overview\">\n";
    echo "  <table><tr><td>\n";
	echo "  <form class=\"overview\" method=\"post\">\n";
    echo "    <fieldset>\n";
    echo "      <table><tr><td>\n";
    echo "      <input type=\"radio\" id=\"prl\" name=\"PicRes\" value=\"low\" checked><label for=\"prl\"> low</label>\n";
    echo "      </td><td>\n";
    echo "      <input type=\"radio\" id=\"prm\" name=\"PicRes\" value=\"med\"><label for=\"prm\"> medium</label>\n";
    echo "      </td></tr><tr><td>\n";
    echo "      <input type=\"radio\" id=\"prh\" name=\"PicRes\" value=\"high\"><label for=\"prh\"> high</label>\n";
    echo "      </td>\n";
    if ( $boolLCL ) {    
        echo "      <td>\n";
        echo "      <input type=\"radio\" id=\"prf\" name=\"PicRes\" value=\"full\"><label for=\"prh\"> full</label>\n";
        echo "      </td>\n";
    }
    echo "      </tr></table>\n";
    echo "    </fieldset>\n";
    echo "    </td><td>\n";
	echo "    <button class=\"overview\" type=\"submit\" name=\"TakePic\" value=\"1\">Take Picture</button>\n";
    echo "    </td></tr></table>\n";
	echo "  </form>\n";
    echo "</TD>\n";
    echo "<TD class=\"overview\">\n";
	if (isset($_POST['TakePic']) and isset($_POST['PicRes'])) {
 		exec('sudo /home/pi/sensorTool/sh/picam.sh '.$_POST['PicRes']);
		echo "<p>picam started [".$_POST['PicRes']."]</p>\n";
        unset($_POST['TakePic']);
	} else {
        echo "<BR />\n";
    }
    echo "</TD>\n";    
    echo "</TR>\n";
    echo "</TABLE>\n";

echo "  <br />\n";
echo "<table class=\"overview\"><TR>\n";
$iCount = 0;
if ($handle = opendir('.')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if(substr($entry, -4) == ".jpg") {
                echo "<TD class=\"overview\">".$entry."<br />\n";
                echo "<img class=\"overview\" alt=".$entry." src=".$entry." />\n";
                echo "</TD>\n";
                $iCount =  $iCount + 1;
                if ($iCount == 2 ) {
                    echo "</TR><TR>\n";
                    $iCount = 0;
                }
            }
            //echo "$entry\n";
        }
    }
    closedir($handle);
}
echo "</TR></table>\n";
echo "</body>\n";
?>
