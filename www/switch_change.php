<?php
    include 'conf.php';
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
            }
       }
    } else if (isset($_POST['SwitchID']) AND isset($_POST['SwitchProtocol']) AND isset($_POST['SwitchAction'])){
        if ( isset($_POST['SwitchUnit']  ) ) {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $_POST['SwitchProtocol'] .' '. $_POST['SwitchID'] .' '. $_POST['SwitchUnit'] .' '. $_POST['SwitchAction']);
            echo "<p>Switch ". $_POST['SwitchID'] ."-". $_POST['SwitchUnit'] ." new state ". $_POST['SwitchAction'].".</p>\n";
        } else {
            exec('sudo /home/pi/sensorTool/sh/pilightservice.sh '. $_POST['SwitchProtocol'] .' '. $_POST['SwitchID'] .' '. $_POST['SwitchAction']);
            echo "<p>Switch ". $_POST['SwitchID'] ." new state ". $_POST['SwitchAction'].".</p>\n";
        }
    }
    
?>
