<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Status</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <meta http-equiv=\"refresh\" content=\"90\" >";
//echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
//echo "  <link rel=\"stylesheet\" href=\"styledisplay.css\">";
echo "  <script language=\"JavaScript\" type=\"text/javascript\">\n";
echo "	// Anzeigezeit in ms\n";
echo "    var WechselZeit = 15000\n";
echo "    ImageArr = new Array()\n";
if ($handle = opendir('./pcis/')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if(substr($entry, -4) == ".JPG") {
echo "    ImageArr[ImageArr.length] = \"pcis/".$entry."\";\n";
            }
        }
    }
    closedir($handle);
}
echo "    var xAnzahl = ImageArr.length;\n";
echo "    var xCounter=-1;\n";
echo "    function Bildwechsel01() {\n";
echo "      xCounter = xCounter+1;\n";
echo "      if (xCounter < xAnzahl) {\n";
echo "        document.getElementById('Foto01').src = ImageArr[xCounter];\n";
echo "        setTimeout (\"Bildwechsel01()\",WechselZeit);\n";
echo "      } else {\n";
echo "        xCounter = -1;\n";
echo "        Bildwechsel01();\n";
echo "      }\n";
echo "    }\n";
echo "    // Startverzögerung\n";
echo "    setTimeout('Bildwechsel01()', 5000);\n";
//echo "    function bildwechsel(Bildname)\n";
//echo "    {\n";
//echo "	  if(document.getElementById(Bildname).src.indexOf('1_Modules.png') == -1)\n";
//echo "      {\n";
//echo "         document.getElementById(Bildname).src = \"1_Modules.png\"\n";
//echo "      } else {\n";
//echo "         document.getElementById(Bildname).src = \"2_Absolute_Humidity.png\"\n";
//echo "      }\n";
//echo "    }\n";
echo "  </script>\n";
echo "</head>\n";
echo "<body margin=0 padding=0 bgcolor=\"#000000\">\n";

include 'functions.php';

echo "<div  class=\"stframe\" bgcolor=\"#000000\">\n";
  echo "<div style=\"float:left\" class=\"stpics\" bgcolor=\"#000000\">\n";
    echo "<img id=\"Foto01\" src=\"pcis/100_7549.JPG\" height=465 border=0 alt=\"\">\n";
//    echo "<img class=\"chart\" src=2_Absolute_Humidity.png name=\"grafik\" id=\"grafik\" onClick=\"bildwechsel(this.name)\" />\n";
  echo "</div>\n";
  echo "<div style=\"float:left\" class=\"stbottom\" bgcolor=\"#000000\">\n";
echo "      <form action=\"http://raspberrypi/index_kiosk.php\">\n";
echo "        <input type=\"submit\" value=\"Home\" />\n";
echo "      </form>\n";
//    echo "<div  class=\"stlink\" bgcolor=\"#000000\">\n";
//      include 'top_menue7.php';
//    echo "</div>\n";
  echo "</div>\n";
echo "</div>\n";

echo "</body>\n";
?>
