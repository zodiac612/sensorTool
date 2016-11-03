<?php
switch ($vMenueFrame) {
	case 'slideshow':
		
		echo "<div>\n";
		echo "  <form action=\"http://".SENSORTOOLSERVER."/index_kiosk.php\">\n";
		echo "    <input type=\"submit\" value=\"Home\" />\n";
		echo "  </form>\n";
		echo "</div>\n";
		echo "<div style=\"margin-top: 2px;\">\n";
		echo "  <form action=\"http://".SENSORTOOLSERVER."/slideshow.php\">\n";
		echo "    <input type=\"submit\" value=\"Refresh\" />\n";
		echo "  </form>\n";
		echo "</div>\n";
		break;
		
	default:
		$vtmStyle = 'topmenu';
		if ( $vMenueFrame == 'rpidisplay') {
			$vtmStyle = $vtmStyle.'7';
		}
		
		echo "<table class=\"".$vtmStyle."\">\n";
		echo "  <TR>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/index_kiosk.php\">\n";
		echo "        <input type=\"submit\" value=\"Home\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/switch.php\">\n";
		echo "        <input type=\"submit\" value=\"Schalter\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/slideshow.php\">\n";
		echo "        <input type=\"submit\" value=\"slideshow\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/overview.php\">\n";
		echo "        <input type=\"submit\" value=\"Diagramme\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/settings.php\">\n";
		echo "        <input type=\"submit\" value=\"Einstellungen\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";
		echo "    <TD class=\"".$vtmStyle."\">\n";
		echo "      <form action=\"http://".SENSORTOOLSERVER."/index.php\">\n";
		echo "        <input type=\"submit\" value=\"Index\" />\n";
		echo "      </form>\n";
		echo "    </TD>\n";

		
		if ( $vMenueFrame <> 'rpidisplay') 
		{
			echo "    <TD class=\"".$vtmStyle."\">\n";
			echo "      <form action=\"http://".SENSORTOOLSERVER."/picam.php\">\n";
			echo "        <input type=\"submit\" value=\"Picam\" />\n";
			echo "      </form>\n";
			echo "    </TD>\n";
			echo "    <TD class=\"".$vtmStyle."\">\n";
			echo "      <form action=\"http://".SENSORTOOLSERVER."/webradio.php\">\n";
			echo "        <input type=\"submit\" value=\"webradio\" />\n";
			echo "      </form>\n";
			echo "    </TD>\n";
		} 
		echo "  </TR>\n";
		echo "</table>\n";
	}

?>
