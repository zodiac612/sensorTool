<?php
error_reporting(E_ALL); ini_set('display_errors', '1');

echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Overview</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "  <link rel=\"stylesheet\" href=\"stylesheet.css\">";
echo "</head>\n";
echo "<body>\n";

include 'top_menue.php';
//include 'precheck.php';

echo "<h3>Raspberry PI SensorTool Status<BR />". date("d.m.Y",time())."</h3>\n";
echo "<BR />\n";

echo "<table class=\"chart\"><TR>\n";
// Read the pngs from filesystem
$arrFiles=array();
$iCount = 0;
if ($handle = opendir('.')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if(substr($entry, -4) == ".png") {
                $arrFiles[]=$entry;
            }
            //echo "$entry\n";
        }
    }
    closedir($handle);
}
//sort the pngs
sort($arrFiles);
//generate the html
foreach ($arrFiles as $vKey => $vValue)
{
    echo "<TD class=\"chart\">".$vValue."<br />\n";
    echo "<img class=\"chart\" alt=".$vValue." src=".$vValue." />\n";
    echo "</TD>\n";
    //echo $vKey."---".$vValue."<br />\n";
    $iCount =  $iCount + 1;
#    if ($iCount == 2 ) {
    echo "</TR><TR>\n";
#        $iCount = 0;
#    }    
}

echo "<td>h</td>\n";
echo "</TR></table>\n";
echo "</body>\n";
?>
