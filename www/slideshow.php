<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

include 'conf.php';
include 'functions.php';

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Status</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylewebradio.css\">";
echo "  <link rel=\"stylesheet\" href=\"styleslide.css\">";
//echo "  <meta http-equiv=\"refresh\" content=\"90\" >";
echo "</head>\n";

$strAlarm = readFileToArray("alarm.csv");
$boolAlarm = False;
//VAR_DUMP($strAlarm);
if ($strAlarm[0][0] == "True" ) {
  $boolAlarm = True;
}

if ($boolAlarm) {
 echo "<body class=\"stinfoAlarm\">\n";
} else {
 echo "<body>\n";
}

$arrPictures[] = array ();
if ($handle = opendir('./pcis/')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if(substr($entry, -4) == ".JPG") {
            	$arrPictures[]="pcis/".$entry;
            }
        }
    }
    closedir($handle);
}
$iArray=sizeof($arrPictures);

$vRandomPic = mt_rand(0, $iArray - 1);
$vRandomLayout = mt_rand(1, 10);

//include 'functions.php';

  echo "<div  class=\"stframe\">\n";
  if ( $boolAlarm )  {
      echo "<div  class=\"stbottom\">\n";
        echo "<div  class=\"sthistory\">\n";
            include 'loglatestentry7.php';
        echo "</div>\n";
	  echo "</div>\n";
  }
  if ( $vRandomLayout < 6) {
	echo "<div style=\"float:left\" class=\"stpics\">\n";
	  echo "<img id=\"".$arrPictures[$vRandomPic]."\" src=\"".$arrPictures[$vRandomPic]."\" height=465 border=0 alt=\"\">\n";
    echo "</div>\n";
    echo "<div style=\"float:left\" >\n";
  } else {
	if ($boolAlarm) {
      echo "<div style=\"float:left; width=100px \" class=\"stinfoAlarm\" >\n";
	} else {
      echo "<div style=\"float:left; width=100px \" class=\"stinfo\" >\n";
	}
  }
	   	$vMenueFrame = 'slideshow';  
	   	include 'top_menue.php';
	  echo "<br />\n";
	  	$vWebFrame = 'slideshow';
	    include 'webradio_frame.php';
        echo "<br />\n";
        $vSwitchFrame = 'slidshow';
        include 'switch_frame.php';
	  echo "</div>\n";
	echo "</div>\n";
  if ( $vRandomLayout > 5) {
	echo "<div style=\"float:both\" class=\"stpics\">\n";
	  echo "<img id=\"".$arrPictures[$vRandomPic]."\" src=\"".$arrPictures[$vRandomPic]."\" height=465 border=0 alt=\"\">\n";
	echo "</div>\n";
  }  
  echo "</div>\n";
  
  echo "<IFRAME style=\"display:none\" name=\"hidden-form\"></IFRAME>\n";

echo "</body>\n";
?>
