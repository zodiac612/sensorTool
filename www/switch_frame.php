<?php

//include 'precheck.php';
$boolLCL = True;
if ( $boolLCL ) {
echo "<DIV class=\"webradio7\">\n";
echo "	  <table class=\"webradio7\">\n";// bgcolor=\"#FFFFFF\" Border=1>\n";
echo "	    <tr>\n";

#foreach ( $arrWebradio as $key => $element ) {
	#echo $key.'#'.var_dump($element);
#	$boolWebradioStationVisible = True;
#	if ( $vSwitchFrame == 'slideshow') {
#		$boolWebradioStationVisible = $element[9];
#	} else {
#		$boolWebradioStationVisible = $element[5];
#	}
	echo "	    <tr>\n";
   		echo "<td class=\"webradio7\">\n";
        echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
        echo "    <input type=\"hidden\" name=\"alarm\" value=\"True\">\n";
        echo "    <input type=\"hidden\" name=\"state\" value=\"0\">\n";  
		echo "    <input type=\"submit\" name=\"action\" value=\"Alarm Aus\"></input>";
		echo "	</form>\n";
		echo "</td>\n";	
        			echo "	    </tr>\n";
			echo "	    <tr>\n";
        echo "<td class=\"webradio7\">\n";
        echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
        echo "    <input type=\"hidden\" name=\"switchgroup\" value=\"wozi\">\n";
        echo "    <input type=\"hidden\" name=\"state\" value=\"0\">\n";
		echo "    <input type=\"submit\" name=\"action\" value=\"Wozi Aus\"></input>";
		echo "	</form>\n";
		echo "</td>\n";	
        			echo "	    </tr>\n";
			echo "	    <tr>\n";
        echo "<td class=\"webradio7\">\n";
        echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
        echo "    <input type=\"hidden\" name=\"switchgroup\" value=\"outdoor\">\n";
        echo "    <input type=\"hidden\" name=\"state\" value=\"0\">\n";
		echo "    <input type=\"submit\" name=\"action\" value=\"Outdoor Aus\"></input>";
		echo "	</form>\n";
		echo "</td>\n";	
        echo "	    </tr>\n";
        	echo "	    <tr>\n";
        echo "<td class=\"webradio7\">\n";
        echo "	<form action=\"switch_change.php\" method=\"post\" target=\"hidden-form\">\n";
        echo "    <input type=\"hidden\" name=\"switchgroup\" value=\"outdoor\">\n";
        echo "    <input type=\"hidden\" name=\"state\" value=\"1\">\n";
		echo "    <input type=\"submit\" name=\"action\" value=\"Outdoor An\"></input>";
		echo "	</form>\n";
		echo "</td>\n";	
        echo "	    </tr>\n";
	
#		if ( $vWebFrame == 'slideshow') {
#			echo "	    </tr>\n";
#			echo "	    <tr>\n";
#		}
#	}
}

echo "	  </table>\n";
echo "</DIV>\n";
?>
