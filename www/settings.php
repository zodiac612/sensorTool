<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

include 'conf.php';

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Settings</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body bgcolor=\"#CCCCCC\">\n";

$vMenueFrame = 'settings';
include 'top_menue.php';
include 'precheck.php';

function readFileToArray($File) {
	// Param String $File (Pfad zur Datei)
	$arrFiles=array();
	$readDatei = fopen($File, "r");
	while(($Daten = fgetcsv($readDatei, 100, "=")) !== FALSE) {
		//var_dump($Daten);
		//echo "<BR />\n";
		//echo count($Daten)."<BR />\n";
		if ( count($Daten) == 2 ) {
			//echo count($Daten)."<BR />\n";
	        if ( $Daten[0][0] != "#" ) 
	        {
	            $arrDatenSpalten = array();
	            for($i = 0; $i < 2; $i++) {
	                //echo $Daten[$i]. "; ";
	                $arrDatenSpalten[$i] = trim($Daten[$i]);
	            }
	            //echo "<BR />\n";
	            $arrFiles[]=$arrDatenSpalten;
	        }
		}
	}
	fclose($readDatei);
	return $arrFiles;
}

$confFile = './dynamic.conf';

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
    //echo "exec('/home/pi/sensorTool/sh/updateconf.sh '".base64_encode($result).")";
    exec('/home/pi/sensorTool/sh/updateconf.sh '.base64_encode($result));
    $arrConfig = readFileToArray($confFile);
}

echo "	<form method=\"post\">\n";
echo "	  <table width=400 bgcolor=\"#FFFFFF\" Border=1>\n";
foreach ($arrConfig as $vKey => $vValue)
{
	echo "	    <tr>\n";
	echo "			<td width=40%>".$vValue[0]."</td>\n";
	echo "			<td width=40%>".$vValue[1]."</td>\n";
	if ( $vValue[1] == 'True' OR $vValue[1] == 'False') 
	{
		if ($vValue[1] == 'True') {
			echo "			<td width=20%>";
			echo "<input type=\"radio\" checked=\"checked\" name=\"".$vValue[0]."\" value=\"True\">An</input>";
			echo "<input type=\"radio\" name=\"".$vValue[0]."\" value=\"False\">Aus</input>";
			echo "</td>\n";
		} else {
			echo "			<td width=20%>";
			echo "<input type=\"radio\" name=\"".$vValue[0]."\" value=\"True\">An</input>";
			echo "<input type=\"radio\" checked=\"checked\" name=\"".$vValue[0]."\" value=\"False\">Aus</input>";
			echo "</td>\n";
		}
			
	} else {
		echo "			<td width=20%>";
		echo "<input type=\"text\" name=\"".$vValue[0]."\" value=\"".$vValue[1]."\">";
		echo "</td>\n";
	}
	echo "	    </tr>\n";
}


echo "	    <tr>\n";
echo "	      <td style=\"text-align: center;\">Relais</td>\n";
echo "	      <td style=\"text-align: center;\">";
//echo "	         <button type=\"submit\" name=\"relais_active\" value=\"true\">An</button>";
//echo "	         <button type=\"submit\" name=\"relais_active\" value=\"false\">Aus</button>";
echo "	      </td>\n";
echo "	      <td style=\"text-align: center;\">";
echo "	         <input type=\"submit\" value=\"Einstellung aendern\">";
echo "	      </td>\n";
echo "	    </tr>\n";
echo "	  </table>\n";
echo "	</form>\n";
echo "  <br />\n";  

echo "</body>\n";
?>
