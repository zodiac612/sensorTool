<?php
	$Counter = 0;
	$Zeilen = 0;
	
	// Einlesen der CSV(;) datei
	$arrData = readFileToArray('loglatestentry7.csv');
	$Zeilen = sizeof($arrData);
	$AnzahlDerFelder = sizeof($arrData[0])-1;

  echo "<TABLE class=\"sensor7\">\n";

	echo "<TBODY>\n";
	for($i = 0; $i < $Zeilen; $i++) {
        echo "<TR>\n";
        for($j = 0; $j < $AnzahlDerFelder; $j++ ) {
            if ( $j > 0 ) {
                echo "<TD>".$arrData[$i][$j]."</TD>\n";
            } else {
                echo "<TD><strong>".$arrData[$i][$j]."</strong></TD>\n";
            }
        }
		echo "</TR>\n";
	}
	echo "</TBODY>\n";
	
  echo "</TABLE>\n";

?>
