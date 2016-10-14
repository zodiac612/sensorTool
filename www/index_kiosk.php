<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Status</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "  <link rel=\"stylesheet\" href=\"styledisplay.css\">";
echo "</head>\n";
echo "<body>\n";

include 'functions.php';

echo "<div  class=\"stframe\">\n";
    echo "<div  class=\"stleft\">\n";
        echo "<div  class=\"sttitle\">\n";
            echo "Raspberry PI SensorTool Status: ". date("d.m.Y",time())."\n";
        echo "</div>\n";
        echo "<div  class=\"stwebradio\">\n";
            include 'webradio7.php';
        echo "</div>\n";
        echo "<div  class=\"stsensor\">\n";
            include 'sensor7.php';
        echo "</div>\n";
        echo "<div  class=\"stfa\">\n";
            include 'fa7.php';
        echo "</div>\n";        
    echo "</div>\n";
    echo "<div  class=\"stright\">\n";
        echo "<div  class=\"stdiagAH\">\n";
            echo "<img class=\"chart\" alt=2_Absolute_Humidity.png src=2_Absolute_Humidity.png />\n";
        echo "</div>\n";
        echo "<div  class=\"stmodules\">\n";
            include 'module7.php';
        echo "</div>\n";
    echo "</div>\n";
    echo "<br style=\"clear:both;\" />\n";
    echo "<div  class=\"stbottom\">\n";
        echo "<div  class=\"stlink\">\n";
            include 'top_menue7.php';
        echo "</div>\n";
//        echo "<br style=\"clear:both;\" />\n";
    echo "</div>\n";
    echo "<div  class=\"stbottom\">\n";
//        echo "<div  class=\"stswitch\">\n";
//            echo "<form action=\"http://raspberrypi/switch7.php\">\n";
//                echo "<input type=\"submit\" value=\"Schalter\" />\n";
//            echo "</form>\n";
//        echo "</div>\n";
        echo "<div  class=\"sthistory\">\n";
            include 'loglatestentry7.php';
        echo "</div>\n";
    echo "</div>\n";
echo "</div>\n";
//include 'top_menue.php';
//include 'precheck.php';

//echo "<h4>Raspberry PI SensorTool Status: ". date("d.m.Y",time())."</h4>\n";
//echo "<BR />\n";

//2_Absolute_Humidity.png

//include 'webradio_short.php';
//if ( $boolLCL ) {
//}
//include 'loglatestentry.php';

//echo "<BR />\n";

//include 'sensor.php';

//echo "<BR />\n";

//include 'logdata.php';
//echo"</div>\n";
echo "</body>\n";
?>
