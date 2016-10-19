<?php
	$Counter = 0;
	$Zeilen = 0;
	
// 	$AnzahlDerFelderList = 3;
//	$AnzahlDerFelder = $AnzahlDerFelderList;
//	$AnzahlNichtBenutzterFelder = 1;
//	$WikiSpalte = 999;
//	$MediaSpalte = 999; -->

	// Einlesen der CSV(;) datei
	$arrData = readFileToArray('sensor.csv');
	$Zeilen = sizeof($arrData);
	$AnzahlDerFelder = sizeof($arrData[0]) - 1;

    //echo $Zeilen.'#'.$AnzahlDerFelder;
	//debugShowArrayContent($arrData);

  if ($vSensor_Frame == 'index') {
	echo "<DIV class=\"sensor\"><TABLE class=\"sensor\"><TR>\n";
	echo "<TD>\n";
  }
  echo "<TABLE class=\"sensor7\">\n";
 // echo "<CAPTION>Sensor</CAPTION>\n";
	
	echo "<THEAD>\n";
	echo "<TR>\n";
	echo "<TH>Name</TH>\n";
    echo "<TH>Zeit</TH>\n";
    echo "<TH>T</TH>\n";
    echo "<TH>RH</TH>\n";
    echo "<TH>AH</TH>\n";
	echo "</TR>\n";
	echo "</THEAD>\n";
	
	echo "<TBODY>\n";
	for($i = 0; $i < $Zeilen; $i++) {
        echo "<TR>\n";
        for($j = 0; $j < $AnzahlDerFelder; $j++ ) {
            if ( $j > 0 ) {
                $vClass="";
                if ( $j == ($AnzahlDerFelder - 1) ) {
                    if ( $arrData[$i][$j] < 9.8 ) {
                        $vClass=" class=\"lightGreen\"";
                    } else if ( $arrData[$i][$j] <= 11 ) {
                        $vClass=" class=\"lightOrange\"";
                    } else if ( $arrData[$i][$j] < 11 ) {
                        $vClass=" class=\"lightRed\"";
                    }
                }
                if ( $j == ($AnzahlDerFelder - 3) ) {
                    if ( $arrData[$i][$j] < 4 ) {
                        $vClass=" class=\"lightBlue\"";
                    }else if (( $arrData[$i][$j] < 14 )){
                        $vClass=" class=\"lightGreen\"";
                    }else if (( $arrData[$i][$j] < 24 )){
                        $vClass=" class=\"lightOrange\"" ;
                    }else if (( $arrData[$i][$j] >= 24 )){
                        $vClass=" class=\"lightRed\"" ;                        
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
  
  if ($vSensor_Frame == 'index') {
	echo "</TD>\n";
	echo "<TD>\n";
		echo "<DIV class=\"sensor\"><TABLE class=\"sensor\">\n";
		echo "<TR>\n";
		echo "<TD>\n";
			include 'module.php';
		echo "</TD>\n";
		echo "</TR>\n";
		echo "<TR>\n";
		echo "<TD>\n";
			include 'fa.php';
		echo "</TD>\n";
		echo "</TR>\n";
		echo "</TABLE>\n";
		echo "</DIV>\n";
  	echo "</TD>\n";
  	echo "</TR>\n";
  	echo "</TABLE>\n";
  }
  

?>
