<?php
define('SENSORTOOLSERVER', 'raspberrypi3');
$vtop_menue = 'rpidisplay';

$arrWebradio[] = array ( "0", "sender1", "Radio 8'", 0, "http://stream.radio8.de:8000/live", True, True);
$arrWebradio[] = array ( "1", "sender2", "Bayern 3'", 10, "http://br-mp3-bayern3-m.akacast.akamaistream.net/7/442/142692/v1/gnl.akacast.akamaistream.net/br_mp3_bayern3_m", True, True);
$arrWebradio[] = array ( "2", "sender3", "Star FM'", 5, "http://87.230.53.43:8004", True, False);
$arrWebradio[] = array ( "3", "sender4", "Star FM 2'", 5, "http://91.250.82.237:8004", False, False);
$arrWebradio[] = array ( "4", "sender5", "Moda'", 5, "http://8743.live.streamtheworld.com/CRP_MODAAC_SC", False, False);

$arrSwitches[] = array ( "0", "Switch12", "TV", "intertechno_switch", 19524338, 1, "LED", "Wozi", True);
$arrSwitches[] = array ( "1", "Switch13", "Schrank", "intertechno_switch", 19524338, 2, "LED", "Wozi", False);
$arrSwitches[] = array ( "2", "Switch11", "Lichterkette", "intertechno_switch", 19524338, 7, "outdoor", "Wozi", False);
$arrSwitches[] = array ( "3", "Switch21", "GT_7000_1", "quigg_gt7000", 301, 0, "GT_7000", "None", False);
$arrSwitches[] = array ( "4", "Switch22", "GT_7000_2", "quigg_gt7000", 301, 1, "GT_7000", "None", False);
$arrSwitches[] = array ( "5", "Switch31", "AmazonFireTV", "quigg_gt9000", 658476, 3, "media", "Wozi", False);
$arrSwitches[] = array ( "6", "Switch32", "Wii", "quigg_gt9000", 658476, 10, "media", "Wozi", False);
$arrSwitches[] = array ( "7", "Switch33", "Vornado", "quigg_gt9000", 658476, 7, "Control", "None", False);
$arrSwitches[] = array ( "8", "Switch34", "rpi display", "quigg_gt9000", 658476, 13, "GT_9000", "None", False);
$arrSwitches[] = array ( "9", "Switch91", "radiators", "fritzactor", 87610073786, None, "Control", "None", False);


?>
