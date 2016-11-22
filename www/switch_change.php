<?php
    error_reporting(E_ALL); ini_set('display_errors', '1');
    include 'conf.php';
    include 'functions.php';
    
    // Einlesen der CSV(;) datei
	$arrData = readFileToArray('switchstate.csv');
	$Zeilen = sizeof($arrData);
	$AnzahlDerFelder = sizeof($arrData[0]) - 1;
    
	//vardump($POST)
    if ( isset($_POST['alarm']) AND isset($_POST['state'] )  ) {
        foreach ( $arrSwitches as $key => $element ) {
            if ( $element[8] ) {
                if ( $element[5] !== "None"  ) {
                    exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $element[3] .' '. $element[4] .' '.$element[5] .' '. $_POST['state']);
                    echo "<p>Switch ". $element[3] ."-". $element[4] ." new state ". $_POST['state'].".</p>\n";
                } else {
                    exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $element[3] .' '. $element[4] .' '. $_POST['state']);
                    echo "<p>Switch ". $_POST['SwitchID'] ." new state ". $_POST['SwitchAction'].".</p>\n";
                }   
                $arrData[$key][2] = $_POST['state'];
            }
       }
    } else if ( isset($_POST['switchgroup']) AND isset($_POST['state'] )  ) {
        foreach ( $arrSwitches as $key => $element ) {
            if ( $element[7] ==  $_POST['switchgroup'] ) {
                if ( $element[5] !== "None"   ) {
                    exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $element[3] .' '. $element[4] .' '.$element[5] .' '. $_POST['state']);
                    echo "<p>Switch ". $element[3] ."-". $element[4] ." new state ". $_POST['state'].".</p>\n";
                } else {
                    exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $element[3] .' '. $element[4] .' '. $_POST['state']);
                    echo "<p>Switch ". $_POST['SwitchID'] ." new state ". $_POST['SwitchAction'].".</p>\n";
                } 
                $arrData[$key][2] = $_POST['state'];  
            }
       }
    } else if ( isset($_POST['switch'])  AND isset($_POST['state']) ) {
        if ( $arrSwitches[$_POST['switch']][5] !== "None"  ) {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '.  $arrSwitches[$_POST['switch']][3] .' '. $arrSwitches[$_POST['switch']][4] .' '. $arrSwitches[$_POST['switch']][5] .' '. $_POST['state']);
            echo "<p>Switch ". $arrSwitches[$_POST['switch']][4] ."-". $arrSwitches[$_POST['switch']][5] ." new state ". $_POST['state'].".</p>\n";
        } else {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $arrSwitches[$_POST['switch']][3] .' '. $_POST['SwitchID'] .' '. $_POST['state']);
            echo "<p>Switch ". $arrSwitches[$_POST['switch']][4] ." new state ". $_POST['state'].".</p>\n";
        }
        echo $_POST['switch']."-".$_POST['state'];
        //var_dump($arrData);
        $arrData[$_POST['switch']][2] = $_POST['state'];
        //var_dump($arrData);
    }
    
    writeFileFromArray('switchstate.csv', $arrData);
    
?>
