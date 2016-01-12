<?php
error_reporting(E_ALL); ini_set('display_errors', '1');
/* Libchart - PHP chart library
 * Copyright (C) 2005-2011 Jean-Marc Tr�meaux (jm.tremeaux at gmail.com)
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

/**
 * Line chart demonstration
 *
 */
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
echo "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
echo "<head>\n";
echo "	<title>Raspberry PI Overview</title>\n";
echo "	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n";
echo "</head>\n";
echo "<body bgcolor=\"#CCCCCC\">\n";

include "libchart/libchart/classes/libchart.php";
include("_db.php");

function funcAbsoluteHumidity ($Temperatur, $Humidity)
{
	//http://www.wetterochs.de/wetter/feuchte.html
	$r = $Humidity;
	$T = $Temperatur;
	$TK = $T + 273.15;
	//echo $r.'-'.$T.'-'.$TK.'<BR />';
	$a = 7.5;
	$b = 237.3;
	if ( $T < 0.0 )
	{
		$a = 7.6;
		$b = 240.7;
	}
	$vExp = ($a*$T)/($b+$T);
	//			echo $vExp;
	$SDD = 6.1078 * pow( 10, (($a*$T)/($b+$T)));
	// 			echo $r.'-'.$T.'-'.$TK.'-'.$a.'-'.$b.'-'.$SDD.'<BR />';
	$DD = $r/100 * $SDD;
	$v = log10($DD/6.1078);
	$TD = ($b*$v)/($a-$v);
	$AF = pow(10,5)*(18.016/8314.3)*($DD/$TK);
	//echo round($AF,2).'<BR />';

	$vArray = array("AF" => round($AF,2), "TD" => round($TD,2) );
	
	//var_dump($vArray);
	
	return $vArray;
}

// Create connection
$conn = mysqli_connect($DB_SERVER, $DB_USER, $DB_PASSWD, $DB_DATABASE);
// Check connection
if (!$conn) {
	die("Connection failed: " . mysqli_connect_error());
}

$ActTime = 0;
$ActTemp = 0;
$ActPres = 0;
$ActHumi = 0;
$ActRelaisStatus = 0;
$ActRelaisGPIO = 0;
$ActLedGPIO = 0;
$ActSensor1 = "";
$ActSensor1Time = "";
$ActSensor1T = 0;
$ActSensor1RH = 0;
$ActSensor2 = "";
$ActSensor2Time = "";
$ActSensor2T = 0;
$ActSensor2RH = 0;
$ActSensor3 = "";
$ActSensor3Time = "";
$ActSensor3T = 0;
$ActSensor3RH = 0;
$ActSensor4 = "";
$ActSensor4Time = "";
$ActSensor4T = 0;
$ActSensor4RH = 0;

$LastTime = 0;
$LastTemp = 0;
$LastPres = 0;
$LastHumi = 0;
$LastRelaisStatus = 0;
$LastRelaisGPIO = 0;
$LastLedGPIO = 0;
$LastSensor1 = "";
$LastSensor1Time = "";
$LastSensor1T = 0;
$LastSensor1RH = 0;
$LastSensor2 = "";
$LastSensor2Time = "";
$LastSensor2T = 0;
$LastSensor2RH = 0;
$LastSensor3 = "";
$LastSensor3Time = "";
$LastSensor3T = 0;
$LastSensor3RH = 0;
$LastSensor4 = "";
$LastSensor4Time = "";
$LastSensor4T = 0;
$LastSensor4RH = 0;


$sql = "Select a.timestamp, s0na, s0ti, s0te, s0rh, s0pa, s1na, s1ti, s1te, s1rh, s2na, s2ti, s2te, s2rh, s3na, s3ti, s3te, s3rh, s4na, s4ti, s4te, s4rh, relais, led from (Select timestamp, name as s0na, time as s0ti, temperature as s0te, humidity as s0rh, pressure as s0pa, led, relais from data where device_id = 0 and timestamp>=CURDATE()) a JOIN (Select timestamp, name as s1na, time as s1ti, temperature as s1te, humidity as s1rh from data where device_id = 1 and timestamp>=CURDATE()) b on a.timestamp = b.timestamp JOIN (Select timestamp, name as s2na, time as s2ti, temperature as s2te, humidity as s2rh from data where device_id = 2 and timestamp>=CURDATE()) c on a.timestamp = c.timestamp JOIN (Select timestamp, name as s3na, time as s3ti, temperature as s3te, humidity as s3rh from data where device_id = 3 and timestamp>=CURDATE()) d on a.timestamp = d.timestamp JOIN (Select timestamp, name as s4na, time as s4ti, temperature as s4te, humidity as s4rh from data where device_id = 4 and timestamp>=CURDATE()) e on a.timestamp = e.timestamp";

$result = mysqli_query($conn, $sql);
//echo mysqli_num_rows($result);
if (mysqli_num_rows($result) > 0) {
	// output data of each row
	$tempSet = new XYDataSet ();
	$presSet = new XYDataSet ();
	$humiSet = new XYDataSet ();
	$sensor0AF = new XYDataSet ();
	$sensor0TD = new XYDataSet ();
	$sensor1T = new XYDataSet ();
	$sensor1RH = new XYDataSet ();
	$sensor1AF = new XYDataSet ();
	$sensor1TD = new XYDataSet ();
	$sensor2T = new XYDataSet ();
	$sensor2RH = new XYDataSet ();
	$sensor3T = new XYDataSet ();
	$sensor3RH = new XYDataSet ();
	$sensor3AF = new XYDataSet ();
	$sensor3TD = new XYDataSet ();	
	$sensor4T = new XYDataSet ();
	$sensor4RH = new XYDataSet ();
	$relaisStatus = new XYDataSet ();
	$v60Border = new XYDataSet ();
	$v55Border = new XYDataSet ();
	$vRaster60 = new XYDataSet ();
	$vRaster80 = new XYDataSet ();

	$RowCounter = 0;
	while($row = mysqli_fetch_assoc($result)) {
		$RowCounter = $RowCounter + 1;

		if ( $RowCounter == 1 ) {
			$LastTime 	= substr ( $row["timestamp"], 11, 5 );
			$LastTemp 	= $row["s0te"];
			$LastPres 	= $row["s0pa"];
			$LastHumi 	= $row["s0rh"];
			$LastRelais = $row["relais"];
			$LastLed	= $row["led"];
			$LastName	     = $row["s0na"];
			$LastSensor1     = $row["s1na"];
			$LastSensor1Time = substr ( $row["s1ti"], 11, 5 );
			$LastSensor1T    = $row["s1te"];
			$LastSensor1RH   = $row["s1rh"];
			$LastSensor2     = $row["s2na"];
			$LastSensor2Time = substr ( $row["s2ti"], 11, 5 );
			$LastSensor2     = $row["s2te"];
			$LastSensor2RH   = $row["s2rh"];
			$LastSensor3     = $row["s3na"];
			$LastSensor3Time = substr ( $row["s3ti"], 11, 5 );
			$LastSensor3T    = $row["s3te"];
			$LastSensor3RH   = $row["s3rh"];
			$LastSensor4     = $row["s4na"];
			$LastSensor4Time = substr ( $row["s4ti"], 11, 5 );
			$LastSensor4T    = $row["s4te"];
			$LastSensor4RH   = $row["s4rh"];
		} else {
			$ActTime 	= substr ( $row["timestamp"], 11, 5 );
			$ActTemp 	= $row["s0te"];
			$ActPres 	= $row["s0pa"];
			$ActHumi 	= $row["s0rh"];
			$ActRelais  = $row["relais"];
			$ActLed	    = $row["led"];
			$ActName	    = $row["s0na"];
			$ActSensor1     = $row["s1na"];
			$ActSensor1Time = substr ( $row["s1ti"], 11, 5 );
			$ActSensor1T    = $row["s1te"];
			$ActSensor1RH   = $row["s1rh"];
			$ActSensor2     = $row["s2na"];
			$ActSensor2Time = substr ( $row["s2ti"], 11, 5 );
			$ActSensor2T    = $row["s2te"];
			$ActSensor2RH   = $row["s2rh"];
			$ActSensor3     = $row["s3na"];
			$ActSensor3Time = substr ( $row["s3ti"], 11, 5 );
			$ActSensor3T    = $row["s3te"];
			$ActSensor3RH   = $row["s3rh"];
			$ActSensor4     = $row["s4na"];
			$ActSensor4Time = substr ( $row["s4ti"], 11, 5 );
			$ActSensor4T    = $row["s4te"];
			$ActSensor4RH   = $row["s4rh"];
			
		}
		
		$arrSens0 = array();
		$arrSens1 = array();
		$arrSens3 = array();
		
		$arrSens0 = funcAbsoluteHumidity ($ActTemp, $ActHumi);
		$arrSens1 = funcAbsoluteHumidity ($ActSensor1T, $ActSensor1RH);
		$arrSens3 = funcAbsoluteHumidity ($ActSensor3T, $ActSensor3RH);
		
		//echo $arrSens0["AF"].'-'.$arrSens1["AF"].'-'.$arrSens3["AF"].'<BR />';
		//echo $arrSens0["TD"].'-'.$arrSens1["TD"].'-'.$arrSens3["TD"].'<BR />';
		
		$tempSet->addPoint   ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s0te"]    ) );
		$presSet->addPoint   ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s0pa"]    ) );
		$humiSet->addPoint   ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s0rh"]    ) );
		$sensor0AF->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens0["AF"] ) );
		$sensor0TD->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens0["TD"] ) );
		$sensor1T->addPoint  ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s1te"] ) );
		$sensor1RH->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s1rh"] ) );
		$sensor1AF->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens1["AF"] ) );
		$sensor1TD->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens1["TD"] ) );		
		$sensor2T->addPoint  ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s2te"] ) );
		$sensor2RH->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s2rh"] ) );
		$sensor3T->addPoint  ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s3te"] ) );
		$sensor3RH->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s3rh"] ) );
		$sensor3AF->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens3["AF"] ) );
		$sensor3TD->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $arrSens3["TD"] ) );		
		$sensor4T->addPoint  ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s4te"] ) );
		$sensor4RH->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["s4rh"] ) );
		$relaisStatus->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $row["relais"] ) );
		$v60Border->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), 60 ) );
		$v55Border->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), 55 ) );
		$vRasterWert = 0;
		$vRasterWert2 = 0;
		if (substr ( $row["timestamp"], 11, 5 ) < '09:00' ) {
			$vRasterWert = 0;
			$vRasterWert2 = 0;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '11:00' ) {
			$vRasterWert = 60;
			$vRasterWert2 = 80;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '13:00' ) {
			$vRasterWert = 0;
			$vRasterWert2 = 0;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '15:00' ) {
			$vRasterWert = 60;
			$vRasterWert2 = 80;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '17:00' ) {
			$vRasterWert = 0;
			$vRasterWert2 = 0;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '19:00' ) {
			$vRasterWert = 60;
			$vRasterWert2 = 80;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '21:00' ) {
			$vRasterWert = 0;
			$vRasterWert2 = 0;
		} elseif (substr ( $row["timestamp"], 11, 5 ) < '23:00' ) {
			$vRasterWert = 60;
			$vRasterWert2 = 80;
		}
		$vRaster60->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $vRasterWert ) );
		$vRaster80->addPoint ( new Point ( substr ( $row["timestamp"], 11, 5 ), $vRasterWert2 ) );

	}
	$dataSetKeller = new XYSeriesDataSet ();
	$dataSetKeller->addSerie ( "2h Raster", $vRaster80 );
	$dataSetKeller->addSerie ( "Grenzwert", $v55Border );
	$dataSetKeller->addSerie ( "Relais Status", $relaisStatus );
	$dataSetKeller->addSerie ( $ActSensor3 . "_T (" . $ActSensor3T . "C)", $sensor3T );    //Hasen
	$dataSetKeller->addSerie ( $ActSensor3 . "_RH (" . $ActSensor3RH . "%)", $sensor3RH ); //Hasen
	$dataSetKeller->addSerie ( $ActName . "_T (" . $ActTemp . "C)", $tempSet );            //Keller
	$dataSetKeller->addSerie ( $ActName . "_RH (" . $ActHumi . "%)", $humiSet );           //Keller
	
	$dataSetBad = new XYSeriesDataSet ();
	$dataSetBad->addSerie ( "2h Raster", $vRaster80 );
	$dataSetBad->addSerie ( "Grenzwert", $v60Border );
	$dataSetBad->addSerie ( $ActSensor3 . "_T (" . $ActSensor3T . "C)", $sensor3T );    //Hasen
	$dataSetBad->addSerie ( $ActSensor3 . "_RH (" . $ActSensor3RH . "%)", $sensor3RH ); //Hasen
	$dataSetBad->addSerie ( $ActSensor4 . "_T (" . $ActSensor4T . "C)", $sensor4T );    //Aussen
	$dataSetBad->addSerie ( $ActSensor1 . "_T (" . $ActSensor1T . "C)", $sensor1T );    //Bad
	$dataSetBad->addSerie ( $ActSensor1 . "_RH (" . $ActSensor1RH . "%)", $sensor1RH ); //Bad
	
	$dataSetAF = new XYSeriesDataSet ();
	$dataSetAF->addSerie ( $ActName .    "_AF", $sensor0AF );
	$dataSetAF->addSerie ( $ActSensor1 . "_AF", $sensor1AF );
	$dataSetAF->addSerie ( $ActSensor3 . "_AF", $sensor3AF );
	
	//var_dump($sensor0TD);
	
	$dataSetTD = new XYSeriesDataSet ();
	$dataSetTD->addSerie ( $ActName .    "_TD", $sensor0TD );
	$dataSetTD->addSerie ( $ActSensor1 . "_TD", $sensor1TD );
	$dataSetTD->addSerie ( $ActSensor3 . "_TD", $sensor3TD );	
	
// 	$dataSetWozi = new XYSeriesDataSet ();
// 	$dataSetWozi->addSerie ( "2h Raster", $vRaster80 );
// 	$dataSetWozi->addSerie ( "Grenzwert", $v55Border );
// 	$dataSetWozi->addSerie ( $ActSensor2 . "_T (" . $ActSensor2T . "C)", $sensor2T );
// 	$dataSetWozi->addSerie ( $ActSensor2 . "_RH (" . $ActSensor2RH . "%)", $sensor2RH );

// 	$dataSetHasen = new XYSeriesDataSet ();
// 	$dataSetHasen->addSerie ( "2h Raster", $vRaster80 );
// 	$dataSetHasen->addSerie ( $ActSensor3 . "_T (" . $ActSensor3T . "C)", $sensor3T );
// 	$dataSetHasen->addSerie ( $ActSensor3 . "_RH (" . $ActSensor3RH . "%)", $sensor3RH );
// 	$dataSetHasen->addSerie ( $ActSensor4 . "_T (" . $ActSensor4T . "C)", $sensor4T );
// 	// $dataSetHasen->addSerie($ActSensor4."_RH (".$ActSensor4RH."%)", $sensor4RH);
// 	// $dataSet->addSerie("Pressure", $presSet);
	
	$chart1 = new LineChart ( 600, 320 );
	$chart1->setDataSet ( $dataSetKeller );
	$chart1->setTitle ( $ActName );
	$chart1->getPlot ()->getPalette ()->setLineColor ( array (
			new Color ( 200, 200, 200 ),      // grau (Raster)
			new Color ( 200, 50, 50 ),        // rot (Grenzlinie)
			new Color ( 255, 255, 0 ),        // gelb (Relais Status)
			new Color ( 255, 170, 130 ),		  // (haseT)
			new Color ( 255, 150, 60 ),        // (haseRH)
			new Color ( 20, 150, 255 ),        // (KellerT)
			new Color ( 50, 90, 255 )        // (KellerRH)   
	) );
	$chart1->render ( "generated/keller.png" );
	
	$chart2 = new LineChart ( 600, 320 );
	$chart2->setDataSet ( $dataSetBad );
	$chart2->setTitle ( $ActSensor1 );
	$chart2->getPlot ()->getPalette ()->setLineColor ( array (
			new Color ( 200, 200, 200 ),// grau (Raster)
			new Color ( 200, 50, 50 ),          // rot (Grenzlinie)
			new Color ( 255, 170, 130 ),		  // (haseT)
			new Color ( 255, 150, 60 ),        // (haseRH)
			new Color ( 130, 200, 210 ),        // Aussen			
			new Color ( 255, 128, 255 ),       // (BadT)
			new Color ( 128, 0, 255 )         // (BadRH)			

	) );
	$chart2->render ( "generated/bad.png" );

// 	$chart3 = new LineChart ( 600, 320 );
// 	$chart3->setDataSet ( $dataSetWozi );
// 	$chart3->setTitle ( $ActSensor2 );
// 	$chart3->getPlot ()->getPalette ()->setLineColor ( array (
// 			new Color ( 200, 200, 200 ),
// 			new Color ( 255, 0, 0 ),
// 			//new Color ( 255, 255, 0 ),
// 			//new Color ( 46, 86, 54 ),
// 			//new Color ( 34, 79, 123 ),
// 			new Color ( 47, 208, 55 ),
// 			new Color ( 0, 128, 255 )
// 	) );
// 	$chart3->render ( "generated/wozi.png" );
	
// 	$chart4 = new LineChart ( 600, 320 );
// 	$chart4->setDataSet ( $dataSetHasen );
// 	$chart4->setTitle ( $ActSensor3 );
// 	$chart4->getPlot ()->getPalette ()->setLineColor ( array (
// 			new Color ( 200, 200, 200 ),
// 			//new Color ( 255, 0, 0 ),
// 			//new Color ( 255, 255, 0 ),
// 			new Color ( 47, 208, 55 ),
// 			//new Color ( 34, 79, 123 ),
// 			//new Color ( 47, 208, 55 ),
// 			new Color ( 0, 128, 255 ),
// 			new Color ( 46, 86, 54 )
// 	) );
// 	$chart4->render ( "generated/aussen.png" );

	$chart5 = new LineChart ( 600, 320 );
	$chart5->setDataSet ( $dataSetAF );
	$chart5->setTitle ( "Absolute Feuchte (AF)" );
  	$chart5->getPlot ()->getPalette ()->setLineColor ( array (
 			new Color ( 255, 0, 0 ),      // grau (Raster)
 			new Color ( 0, 255, 0 ),        // rot (Grenzlinie)
 			new Color ( 0, 0, 255 )        // gelb (Relais Status)
// 			new Color ( 255, 100, 100 ),		  // (haseT)
// 			new Color ( 100, 255, 100 ),        // (haseRH)
// 			new Color ( 255, 100, 255 )       // (KellerT)
  	));
	$chart5->render ( "generated/af.png" );
 	
	//var_dump($dataSetTD);
 	$chart6 = new LineChart ( 600, 320 );
 	$chart6->setDataSet ( $dataSetTD );
 	$chart6->setTitle ( "Taupunkt (TD)" );
// 	$chart6->getPlot ()->getPalette ()->setLineColor ( array (
// //  	// 			new Color ( 255, 0, 0 ),      // grau (Raster)
// //  	// 			new Color ( 0, 255, 0 ),        // rot (Grenzlinie)
// //  	// 			new Color ( 0, 0, 255 ),        // gelb (Relais Status)
//  		new Color ( 255, 100, 100 ),		  // (haseT)
//  		new Color ( 100, 255, 100 ),        // (haseRH)
//  		new Color ( 255, 100, 255 )       // (KellerT)
// 	));
 	$chart6->render ( "generated/td.png" ); 	

	echo "<table padding=\"2\" bgcolor=\"#FFFFFF\" Border=1>\n";
	echo "<caption>" . ( string ) date ( "Y-m-d", time () ) . "</caption>\n";
	echo "<thead>\n";
	echo "  <tr>\n";
	echo "    <th><BR /></th>\n";
	echo "    <th colspan=3>" . $ActName . "</th>\n";
	echo "    <th colspan=3>" . $ActSensor1 . "</th>\n";
	echo "    <th colspan=3>" . $ActSensor2 . "</th>\n";
	echo "    <th colspan=3>" . $ActSensor3 . "</th>\n";
	echo "    <th colspan=3>" . $ActSensor4 . "</th>\n";
	echo "    <th colspan=2>GPIO</th>\n";
	echo "  </tr>\n";
	echo "    <td>Timestamp</td>\n";
	echo "    <td>T</td>\n";
	echo "    <td>RH</td>\n";
	echo "    <td>PA</td>\n";
	echo "    <td>Time</td>\n";
	echo "    <td>T</td>\n";
	echo "    <td>RH</td>\n";
	echo "    <td>Time</td>\n";
	echo "    <td>T</td>\n";
	echo "    <td>RH</td>\n";
	echo "    <td>Time</td>\n";
	echo "    <td>T</td>\n";
	echo "    <td>RH</td>\n";
	echo "    <td>Time</td>\n";
	echo "    <td>T</td>\n";
	echo "    <td>RH</td>\n";
	echo "    <td>relais</td>\n";
	echo "    <td>led</td>\n";
	echo "  </tr>\n";
	echo "</thead>\n";
	echo "<tbody>\n";
	echo "  <tr>\n";
	echo "    <td>" . $ActTime . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActTemp . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActHumi . "</td>\n";
	echo "    <td>" . $ActPres . "</td>\n";
	echo "    <td>" . $ActSensor1Time . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor1T . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor1RH . "</td>\n";
	echo "    <td>" . $ActSensor2Time . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor2T . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor2RH . "</td>\n";
	echo "    <td>" . $ActSensor3Time . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor3T . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor3RH . "</td>\n";
	echo "    <td>" . $ActSensor4Time . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor4T . "</td>\n";
	echo "    <td bgcolor=\"#FFFFAA\">" . $ActSensor4RH . "</td>\n";
	echo "    <td>" . $ActRelais . "</td>\n";
	echo "    <td>" . $ActLed . "</td>\n";
	echo "  </tr>\n";
	echo "  <tr>\n";
	echo "    <td>" . $LastTime . "</td>\n";
	echo "    <td>" . $LastTemp . "</td>\n";
	echo "    <td>" . $LastHumi . "</td>\n";
	echo "    <td>" . $LastPres . "</td>\n";
	echo "    <td>" . $LastSensor1Time . "</td>\n";
	echo "    <td>" . $LastSensor1T . "</td>\n";
	echo "    <td>" . $LastSensor1RH . "</td>\n";
	echo "    <td>" . $LastSensor2Time . "</td>\n";
	echo "    <td>" . $LastSensor2T . "</td>\n";
	echo "    <td>" . $LastSensor2RH . "</td>\n";
	echo "    <td>" . $LastSensor3Time . "</td>\n";
	echo "    <td>" . $LastSensor3T . "</td>\n";
	echo "    <td>" . $LastSensor3RH . "</td>\n";
	echo "    <td>" . $LastSensor4Time . "</td>\n";
	echo "    <td>" . $LastSensor4T . "</td>\n";
	echo "    <td>" . $LastSensor4RH . "</td>\n";
	echo "    <td>" . $LastRelais . "</td>\n";
	echo "    <td>" . $LastLed . "</td>\n";
	echo "  </tr>\n";
	echo "</tbody>\n";
	echo "</table>\n";
	echo "<BR />\n";
} else {
	echo "0 results";
}

// echo "<pre>";
// var_dump($_POST);
// echo "</pre>";

if (isset($_POST['relais_active']) AND !empty($_POST['relais_active']) AND isset($_POST['relais_threshold_humidity']) AND !empty($_POST['relais_threshold_humidity']) ) {
	//echo " <p>Relais: ".$_POST['relais']."<BR /></p>\n";
	exec('python /home/pi/inmonitor/www/switchrelais.py '. $_POST['relais_active'] .' '. $_POST['relais_threshold_humidity']); 
}

$arrFiles=array();
$readDatei = fopen('./RelaisStat.cfg', "r");
while(($Daten = fgetcsv($readDatei, 100, "=")) !== FALSE) {
	//var_dump($Daten);
	//echo "<BR />\n";
	//echo count($Daten)."<BR />\n";
	if ( count($Daten) == 2 ) {
		//echo count($Daten)."<BR />\n";
		$arrDatenSpalten = array();
		for($i = 0; $i < 2; $i++) {
			//echo $Daten[$i]. "; ";
			$arrDatenSpalten[$i] = trim($Daten[$i]);
		}
		//echo "<BR />\n";
		$arrFiles[]=$arrDatenSpalten;
	}
}
fclose($readDatei);

echo "	<form method=\"post\">\n";
echo "	  <table width=400 bgcolor=\"#FFFFFF\" Border=1>\n";
foreach ($arrFiles as $vKey => $vValue)
{
	echo "	    <tr>\n";
	echo "			<td width=40%>".$vValue[0]."</td>\n";
	echo "			<td width=40%>".$vValue[1]."</td>\n";
	if ( $vValue[1] == 'True' OR $vValue[1] == 'False') 
	{
		if ($vValue[1] == 'True') {
			echo "			<td width=20%>";
			echo "<input type=\"radio\" checked=\"checked\" name=\"relais_active\" value=\"True\">An</input>";
			echo "<input type=\"radio\" name=\"relais_active\" value=\"False\">Aus</input>";
			echo "</td>\n";
		} else {
			echo "			<td width=20%>";
			echo "<input type=\"radio\" name=\"relais_active\" value=\"True\">An</input>";
			echo "<input type=\"radio\" checked=\"checked\" name=\"relais_active\" value=\"False\">Aus</input>";
			echo "</td>\n";
		}
			
	} else {
		echo "			<td width=20%>";
		echo "<input type=\"text\" name=\"relais_threshold_humidity\" value=\"".$vValue[1]."\">";
		echo "</td>\n";
	}
	echo "	    </tr>\n";
}


echo "	    <tr>\n";
echo "	      <td style=\"text-align: center;\">Relais</td>\n";
echo "	      <td style=\"text-align: center;\">";
//echo "	         <button type=\"submit\" name=\"relais_active\" value=\"true\">An</button>";
//echo "	         <button type=\"submit\" name=\"relais_active\" value=\"false\">Aus</button>";
echo "	      </td>\n";
echo "	      <td style=\"text-align: center;\">";
echo "	         <input type=\"submit\" value=\"Einstellung aendern\">";
echo "	      </td>\n";
echo "	    </tr>\n";
echo "	  </table>\n";
echo "	</form>\n";
echo "  <br />\n";

echo "	<img alt=\"Line chart\" src=\"generated/keller.png\" style=\"border: 1px solid gray;\"/>\n";
echo "	<img alt=\"Line chart\" src=\"generated/bad.png\" style=\"border: 1px solid gray;\"/>\n";
// echo "	<img alt=\"Line chart\" src=\"generated/wozi.png\" style=\"border: 1px solid gray;\"/>\n";
// echo "	<img alt=\"Line chart\" src=\"generated/aussen.png\" style=\"border: 1px solid gray;\"/>\n";
echo "	<img alt=\"Line chart\" src=\"generated/af.png\" style=\"border: 1px solid gray;\"/>\n";
echo "	<img alt=\"Line chart\" src=\"generated/td.png\" style=\"border: 1px solid gray;\"/>\n";
echo "</body>\n";
?>
