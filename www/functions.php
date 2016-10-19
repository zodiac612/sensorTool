<?php
  function debugShowArrayContent($arrData) {
    echo count($arrData)."x".sizeof($arrData[0])."<BR>";
    for ( $i = 0; $i < sizeof($arrData); $i++ ) {
     for ( $j = 0; $j < sizeof($arrData[$i]); $j++) {
      echo $arrData[$i][$j].";";
     }
     echo "<BR>\n";
    }
    return 0;
  }
  
  function boolDateiDa( $strDatei ) {
  	$DateiDa=false;
  	if ( is_file($strDatei) ) {
  		$DateiDa=true;
  	} else {
  		if ( is_readable($strDatei) ) {
  			$DateiDa=true;
  		} elseif ( file_exists($strDatei) ){
  			$DateiDa=true;
  		}
  	}
    return $DateiDa;
  }
  
  function readFileToArray($File) {

    // Param String $File (Pfad zur Datei)
    // Param Int $NichtBenutzeSpalteVonRechts ( Spalten von Rechts die ignoriert werden sollen )
    $arrFiles=array();
    if ( boolDateiDa( $File ) ) {
	    $readDatei = fopen($File, "r");
	    while(($Daten = fgetcsv($readDatei, 10000, ";")) !== FALSE) {
		 $iKommentar = strpos(trim($Daten[0]), "//");		 
		  if ( strcmp($iKommentar,"0") != 0 ) {
			  $Spaltenanzahl =  count($Daten);// - $NichtBenutzeSpalteVonRechts;
			  $arrDatenSpalten = array();
			  for($i = 0; $i < $Spaltenanzahl; $i++) {
				$arrDatenSpalten[$i] = $Daten[$i];
				}
			  $arrFiles[]=$arrDatenSpalten;
		  }
	    }
	    fclose($readDatei);
  	} else {
    	$arrFiles[]="File not found";
    	echo "<p>File [".$File."] not found </p>\n";
  	}
    return $arrFiles; 
  }
?>
