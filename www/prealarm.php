<?php
$ipR = explode(".", $_SERVER["REMOTE_ADDR"]);
$ipS = explode(".", $_SERVER["SERVER_ADDR"]);

$boolLCL = False;
if ( $ipR[0] == $ipS[0] AND $ipR[1] == $ipS[1] AND $ipR[2] == $ipS[2] AND $ipR[3] < 200 )
{
		$boolLCL = True;
}

?>
