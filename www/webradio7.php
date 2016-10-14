<?php
//error_reporting(E_ALL); ini_set('display_errors', '1');

//echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
//echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
//echo "<head>\n";
//echo "	<title>Raspberry PI Webradio</title>\n";
//echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
//echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
//echo "</head>\n";
//echo "<body bgcolor=\"#CCCCCC\">\n";

//include 'top_menue.php';
//include 'precheck.php';

function readConfigToArray($File) {
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

$arrConfig = readConfigToArray($confFile);

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
    //echo $result;
    exec('/home/pi/webradio/updatewebradio.sh '.base64_encode($result));
    $arrConfig = readFileToArray($confFile);
}
//var_dump($arrConfig);
$configName="";
$configAction="";

//echo "<p>\n";
//echo "Webradio: <BR />";
foreach ($arrConfig as $vKey => $vValue)
{
    //echo $vValue[0].": ". $vValue[1]."<BR />";
    if ($vValue[0] == "name") 
    {
        //echo $vValue[1]."<BR />";
        $configName = $vValue[1];
    }
    if ($vValue[0] == "action") 
    {
        //echo $vValue[1]."<BR />";
        $configAction = $vValue[1];
    }
}
//echo "</p>\n";
//echo $configName;
//echo $configAction;
echo "<DIV class=\"webradio7\">\n";
echo "	  <table class=\"webradio7\">\n";// bgcolor=\"#FFFFFF\" Border=1>\n";
//echo "	        <thead>Webradio</thead>\n";
//echo "	    <tr>\n";
//echo"<td class=\"webradio7\">Webradio: </td>\n";
if ( $configName == "Radio 8") {
    echo "<td class=\"webradio7start\">\n";
} else {
    echo "<td class=\"webradio7\">\n";
}
echo "	<form method=\"post\">\n";
echo "    <input type=\"hidden\" name=\"volume\" value=\"0\"></input>";
echo "    <input type=\"hidden\" name=\"name\" value=\"Radio 8\"></input>";
echo "    <input type=\"hidden\" name=\"stream\" value=\"http://stream.radio8.de:8000/live\"></input>";
echo "    <input type=\"submit\" name=\"action\" value=\"Radio 8\"></input>";
echo "	</form>\n";
echo "</td>\n";
if ( $configName == "Bayern 3") {
    echo "<td class=\"webradio7start\">\n";
} else {
    echo "<td class=\"webradio7\">\n";
}
echo "	<form method=\"post\">\n";
echo "    <input type=\"hidden\" name=\"volume\" value=\"0\"></input>";
echo "    <input type=\"hidden\" name=\"name\" value=\"Bayern 3\"></input>";
echo "    <input type=\"hidden\" name=\"stream\" value=\"http://br-mp3-bayern3-m.akacast.akamaistream.net/7/442/142692/v1/gnl.akacast.akamaistream.net/br_mp3_bayern3_m\"></input>";
echo "    <input type=\"submit\" name=\"action\" value=\"Bayern 3\"></input>";
echo "	</form>\n";
echo "</td>\n";
if ( $configName == "Star FM") {
    echo "<td class=\"webradio7start\">\n";
} else {
    echo "<td class=\"webradio7\">\n";
}
echo "	<form method=\"post\">\n";
echo "    <input type=\"hidden\" name=\"volume\" value=\"0\"></input>";
echo "    <input type=\"hidden\" name=\"name\" value=\"Star FM\"></input>";
echo "    <input type=\"hidden\" name=\"stream\" value=\"http://87.230.53.43:8004\"></input>";
echo "    <input type=\"submit\" name=\"action\" value=\"Star FM\"></input>";
echo "	</form>\n";
echo "</td>\n";
if ( $configAction == "stop") {
    echo "<td class=\"webradio7stop\">\n";
} else {
    echo "<td class=\"webradio7\">\n";
}
echo "	<form method=\"post\">\n";
//echo "    <input type=\"hidden\" name=\"name\" value=\"stop\"></input>";
echo "	  <input type=\"submit\" name=\"action\"value=\"stop\">";
echo "	</form>\n";
echo "</td>\n";
echo "	    </tr>\n";
echo "	  </table>\n";
echo "</DIV>\n";

//echo "</body>\n";
?>
