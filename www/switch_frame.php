<?php
//include 'conf.php';
//$vSwitchFrame='slideshow';
//include 'precheck.php';



$boolLCL = True;
if ( $boolLCL ) {

    // Einlesen der CSV(;) datei
	$arrSwitchState = readFileToArray('switchstate.csv');
	$Zeilen = sizeof($arrSwitchState);
	$AnzahlDerFelder = sizeof($arrSwitchState[0]) - 1;


    echo "<DIV class=\"webradio7\">\n";
    echo "	  <table class=\"webradio7\">\n";// bgcolor=\"#FFFFFF\" Border=1>\n";
    //echo "	    <tr>\n";

    //alarm
    foreach ( $arrSwitches as $key => $element ) {
        if ( $vSwitchFrame == 'slideshow' And $element[8] ) {
            echo "<tr>\n";
            echo "<td class=\"webradio7\">\n";
            echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
            echo "    <input type=\"hidden\" name=\"alarm\" value=\"True\">\n";
            echo "    <input type=\"hidden\" name=\"state\" value=\"0\">\n";
            echo "    <input type=\"submit\" name=\"action\" value=\"Alarm ".$element[2]." Aus\"></input>";
            echo "	</form>\n";
            echo "</td>\n";	
            echo "</tr>\n";  
        }
    }

    //switchgroups
    foreach ( $arrSwitchGroups as $key => $element ) {
        if ( $vSwitchFrame == 'slideshow' And $element[3] ) {
//            if ($element[4]) {
//                echo "<tr>\n";
//                echo "<td class=\"webradio7\">\n";
//                echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
//                echo "    <input type=\"hidden\" name=\"switchgroup\" value=\"".$element[2]."\">\n";
//                echo "    <input type=\"hidden\" name=\"state\" value=\"1\">\n";
//                echo "    <input type=\"submit\" name=\"action\" value=\"".$element[2]." An\"></input>";
//                echo "	</form>\n";
//                echo "</td>\n";	
//                echo "</tr>\n";
//            }
            echo "<tr>\n";
            echo "<td class=\"webradio7\">\n";
            echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
            echo "    <input type=\"hidden\" name=\"switchgroup\" value=\"".$element[2]."\">\n";
            echo "    <input type=\"hidden\" name=\"state\" value=\"0\">\n";
            echo "    <input type=\"submit\" name=\"action\" value=\"".$element[2]." Aus\"></input>";
            echo "	</form>\n";
            echo "</td>\n";	
            echo "</tr>\n";  
        }
    }

    //switches
    foreach ( $arrSwitches as $key => $element ) {
        if ( $vSwitchFrame == 'slideshow' And $element[9] ) {
            $vAction = 0;
            $vActionName = 'Aus';
            if ($element[10] AND $arrSwitchState[$element[0]][2] == 0 ) {
                $vAction = 1;
                $vActionName = 'An';
            }
            echo "<tr>\n";
            echo "<td class=\"webradio7\">\n";
            echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
            echo "    <input type=\"hidden\" name=\"switch\" value=\"".$element[0]."\">\n";
            echo "    <input type=\"hidden\" name=\"state\" value=\"".$vAction."\">\n";
            echo "    <input type=\"submit\" name=\"action\" value=\"".$element[2]." ".$vActionName."\"></input>";
            echo "	</form>\n";
            echo "</td>\n";	
            echo "</tr>\n";  
        }
    }   
}
echo "	  </table>\n";
echo "</DIV>\n";
?>
