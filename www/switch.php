<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

include 'conf.php';
include 'functions.php';

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Overview</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body>\n";

$vMenueFrame = 'switch';
include 'top_menue.php';

//include 'precheck.php';
$boolLCL = True;
if ( $boolLCL ) {
	echo "  <BR />\n";
	$vSwitchFrame='main';
	include 'switch_frame.php';
    //include 'preswitch.php';
	echo "  <br />\n";
	
	if (isset($_POST['SwitchID']) AND isset($_POST['SwitchProtocol']) AND isset($_POST['SwitchAction'])  ) {
		// echo " <p>Relais: ".$_POST['relais']."<BR /></p>\n";
		// bash pilightservice.sh 19524338 2 0
        if ( isset($_POST['SwitchUnit']  ) ) {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $_POST['SwitchProtocol'] .' '. $_POST['SwitchID'] .' '. $_POST['SwitchUnit'] .' '. $_POST['SwitchAction']);
            echo "<p>Switch ". $_POST['SwitchID'] ."-". $_POST['SwitchUnit'] ." new state ". $_POST['SwitchAction'].".</p>\n";
        } else {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $_POST['SwitchProtocol'] .' '. $_POST['SwitchID'] .' '. $_POST['SwitchAction']);
            echo "<p>Switch ". $_POST['SwitchID'] ." new state ". $_POST['SwitchAction'].".</p>\n";
        }
        
	}
} else {
	echo "<p>Only available when you are on site!</p>\n";
}
echo "</body>\n";
?>
