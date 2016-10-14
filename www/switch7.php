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

include 'top_menue7.php';

include 'precheck.php';

//echo "exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '". $_POST['SwitchID']."' '". $_POST['SwitchUnit'] ."' '". $_POST['SwitchAction'].")<br />\n";
//echo "<BR />SwitchID: ".isset($_POST['SwitchID']) . " AND ". !empty($_POST['SwitchID'])  ." <BR />SwitchUnit: ".isset($_POST['SwitchUnit'])." AND ".!empty($_POST['SwitchUnit'])."<BR />  SwitchAction: ".isset($_POST['SwitchAction'])." AND ".!empty($_POST['SwitchAction'])."<BR />\n"; 
        
//if (isset($_POST['SwitchID']) AND !empty($_POST['SwitchID']) AND isset($_POST['SwitchUnit']) AND !empty($_POST['SwitchUnit']) AND isset($_POST['SwitchAction']) AND !empty($_POST['SwitchAction']) ) {
$boolLCL = True;
if ( $boolLCL ) {
//    echo "<iframe\n";
//    echo "src=\"http://raspberrypi:5001\"\n";
//    echo "  width=\"780\" \n";
//    echo "  height=\"400\" \n";
//    echo "  name=\"pilight\">\n";

//    echo "  <p>Ihr Browser kann leider keine eingebetteten Frames anzeigen:\n";
//    echo "  Sie können die eingebettete Seite über den folgenden Verweis aufrufen: \n";
//    echo "  <a href=\"http://raspberrypi:5001\">SELFHTML</a>\n";
//    echo "  </p>\n";
//    echo "</iframe>\n";

	echo "  <BR />\n";
    include 'preswitch.php';
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
