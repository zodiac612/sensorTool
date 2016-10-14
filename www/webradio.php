<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Webradio</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body bgcolor=\"#CCCCCC\">\n";

include 'top_menue.php';
//include 'precheck.php';

function readFileToArray($File) {
	// Param String $File (Pfad zur Datei)
	$arrFiles=array();
	$readDatei = fopen($File, "r");
	while(($Daten = fgetcsv($readDatei, 100, "=")) !== FALSE) {
		if ( count($Daten) == 2 ) {
	        if ( $Daten[0][0] != "#" ) 
	        {
	            $arrDatenSpalten = array();
	            for($i = 0; $i < 2; $i++) {
	                $arrDatenSpalten[$i] = trim($Daten[$i]);
	            }
	            $arrFiles[]=$arrDatenSpalten;
	        }
		}
	}
	fclose($readDatei);
	return $arrFiles;
}

$confFile = './webradio.station';

$arrConfig = readFileToArray($confFile);

$result = "{";
foreach ($arrConfig as $vKey => $vValue)
{
    //echo $vValue[0]."<BR />";
    if ( isset($_POST[$vValue[0]])  ) {
        $result = $result."\"".$vValue[0]."\": \"".$_POST[$vValue[0]]."\", ";
        //echo " <p>Relais: ".$_POST['relais']."<BR /></p>\n";
        //exec('python /var/sensorTool/www/updateconf.py '. $_POST['relais_active'] .' '. $_POST['relais_threshold_humidity']); 
    }
}
$result = $result."}";
#echo $result;
if ($result != "{}") {
    //exec('python /var/sensorTool/www/updateconf.py '. $_POST['relais_active'] .' '. $_POST['relais_threshold_humidity']);
    //echo $result."<BR />";
    //echo "exec('/home/pi/sensorTool/sh/webradio.sh '".base64_encode($result).")";
    exec('/home/pi/webradio/updatewebradio.sh '.base64_encode($result));
    $arrConfig = readFileToArray($confFile);
}

echo "<p>\n";
echo "Webradio: <BR />";
foreach ($arrConfig as $vKey => $vValue)
{
    echo $vValue[0].": ". $vValue[1]."<BR />";
}
echo "</p>\n";

echo "	<form method=\"post\">\n";
echo "	  <table width=400 bgcolor=\"#FFFFFF\" Border=1>\n";
echo "	        <thead>Webradio</thead>\n";
echo "	    <tr>\n";
echo "			<td width=40%>Volume</td>\n";
echo "<td>\n";
echo "<input type=\"radio\" name=\"volume\" value=\"-10\">-10db</input><BR />";
echo "<input type=\"radio\" name=\"volume\" value=\"-5\">-5db</input><BR />";
echo "<input type=\"radio\" checked name=\"volume\" value=\"0\">+-0db</input><BR />";
echo "<input type=\"radio\" name=\"volume\" value=\"2\">+2db</input><BR />";
echo "<input type=\"radio\" name=\"volume\" value=\"5\">+5db</input><BR />";
echo "<input type=\"radio\" name=\"volume\" value=\"10\">+10db</input><BR />";
echo "</td>\n";
echo "	    <tr>\n";
echo "			<td width=40%>Station</td>\n";
echo "<td>\n";
echo "<input type=\"radio\" checked name=\"stream\" value=\"http://stream.radio8.de:8000/live\">Radio 8</input><BR />";
echo "<input type=\"radio\" name=\"stream\" value=\"http://87.230.53.43:8004\">Star FM 1</input><BR />";
echo "<input type=\"radio\" name=\"stream\" value=\"http://91.250.82.237:8004\">Star FM 2</input><BR />";
echo "<input type=\"radio\" name=\"stream\" value=\"http://8743.live.streamtheworld.com/CRP_MODAAC_SC\">Moda</input><BR />";
echo "<input type=\"radio\" name=\"stream\" value=\"http://br-mp3-bayern3-m.akacast.akamaistream.net/7/442/142692/v1/gnl.akacast.akamaistream.net/br_mp3_bayern3_m\">Bayern 3</input><BR />";
echo "	    <tr>\n";
echo "	      <td colspan=\"2\" style=\"text-align: center;\">";
echo "	         <input type=\"submit\" name=\"action\" value=\"start\">";
echo "	         <input type=\"submit\" name=\"action\"value=\"stop\">";
echo "	      </td>\n";
echo "	    </tr>\n";
echo "	  </table>\n";
echo "	</form>\n";
echo "  <br />\n";  

echo "</body>\n";
?>
