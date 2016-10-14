<?php
	$Counter = 0;
	$Zeilen = 0;
	
// 	$AnzahlDerFelderList = 3;
//	$AnzahlDerFelder = $AnzahlDerFelderList;
//	$AnzahlNichtBenutzterFelder = 1;
//	$WikiSpalte = 999;
//	$MediaSpalte = 999; -->

	// Einlesen der CSV(;) datei
	$arrData = readFileToArray('fa7.csv');
	$Zeilen = sizeof($arrData);
	$AnzahlDerFelder = sizeof($arrData[0]) - 1;

	//debugShowArrayContent($arrDVDData);

		
  echo "<TABLE class=\"sensor7\">\n";
//  echo "<CAPTION>Sensor</CAPTION>\n";
	
	echo "<THEAD>\n";
	echo "<TR>\n";
	echo "<TH>Name</TH>\n";
    echo "<TH>Zeit</TH>\n";
    echo "<TH>Status</TH>\n";
    echo "<TH>T</TH>\n";
    echo "<TH>Wh</TH>\n";
	echo "</TR>\n";
	echo "</THEAD>\n";
	
	echo "<TBODY>\n";
	for($i = 0; $i < $Zeilen; $i++) {
        echo "<TR>\n";
        for($j = 0; $j < $AnzahlDerFelder; $j++ ) {
            if ( $j > 0 ) {
                $vClass="";
                if ( $j == ($AnzahlDerFelder - 3) ) {
                    if ( $arrData[$i][$j] == "on" ) {
                        $vClass=" class=\"lightGreen\"";
                    }
                }
                if ( $j == ($AnzahlDerFelder - 1) ) {
                    if ( $arrData[$i][$j] > 0 ) {
                        $vClass=" class=\"lightGreen\"";
                    }else if (( $arrData[$i][$j] > 5.5 )){
                        $vClass=" class=\"lightOrange\"";
                    }else if (( $arrData[$i][$j] > 10.5 )){
                        $vClass=" class=\"lightRed\"";
                    }
                }
                echo "<TD".$vClass.">".$arrData[$i][$j]."</TD>\n";
            } else {
                echo "<TD><strong>".$arrData[$i][$j]."</strong></TD>\n";
            }
        }
		echo "</TR>\n";
	}
	echo "</TBODY>\n";
	
  echo "</TABLE>\n";

?>
