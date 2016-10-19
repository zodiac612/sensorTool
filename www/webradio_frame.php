<?php
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

//var_dump($_POST);

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
//echo $result;
if ($result != "{}") {
    //echo $result;
    exec('/home/pi/webradio/updatewebradio.sh '.base64_encode($result));
    $arrConfig = readFileToArray($confFile);
}
var_dump($arrConfig);
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

foreach ( $arrWebradio as $key => $element ) {
	$boolWebradioStationVisible = True;
	if ( $vWebFrame == 'slideshow') {
		$boolWebradioStationVisible = $element[4];
	} else {
		$boolWebradioStationVisible = $element[3];
	}
	
	if ( $boolWebradioStationVisible ) {
		if ( $configName == $element[0]) {
		    echo "<td class=\"webradio7start\">\n";
		} else {
    		echo "<td class=\"webradio7\">\n";
		}
		echo "	<form method=\"post\">\n";
		echo "    <input type=\"hidden\" name=\"volume\" value=\"".$element[1]."\"></input>";
		echo "    <input type=\"hidden\" name=\"name\" value=\"".$element[0]."\"></input>";
		echo "    <input type=\"hidden\" name=\"stream\" value=\"".$element[2]."\"></input>";
		echo "    <input type=\"submit\" name=\"action\" value=\"".$element[0]."\"></input>";
		echo "	</form>\n";
		echo "</td>\n";		
	}
	if ( $vWebFrame == 'slideshow') {
		echo "	    </tr>\n";
		echo "	    <tr>\n";
	}
}
if ( $configAction == "stop") {
    echo "<td class=\"webradio7stop\">\n";
} else {
    echo "<td class=\"webradio7\">\n";
}
echo "	<form method=\"post\">\n";
echo "	  <input type=\"submit\" name=\"action\"value=\"stop\">";
echo "	</form>\n";
echo "</td>\n";
echo "	    </tr>\n";
echo "	  </table>\n";
echo "</DIV>\n";

//echo "</body>\n";
?>
