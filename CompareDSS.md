For more details, please visit **[VISTA Add-on Tools](http://dsm2-vista.googlecode.com/svn/trunk/vista/doc/scripts/index.html)** for online documents.



# Introduction #
This tool automates the comparison process and produces report to share with others. It reduces duplicate effort for routine procedures, avoids human operation errors, and provides a systematic way for result comparison. The tool reads DSS files and generates a HTML report based on instructions in a configuration file. There are five modes available for output options. They are 1) observed data only 2) modeled data only 3) two model comparison 4) calibration and 5) calibration comparison for two model outputs. The interactive time series plot gives users the options to adjust time windows, overlay water year types and view the differences.

# Basic Setup #
1. Open a new folder and prepare a configuration file inside this folder. For example, dsm2\_output.inp.<br>
2. Run command prompt from this folder and type:<br>
<pre><code>   &gt; compare_dss dsm2_output.inp<br>
</code></pre>
3. All the output files will be generated in the directory specified in SCALAR::OUTDIR.<br>
<br>
<h1>Configuration File</h1>
Here is the instruction for how to prepare the configuration file.<br>
There are 5 blocks inside the configuration file. They are:<br>
<pre><code>  * GLOBAL_CONTROL<br>
  * SCALAR<br>
  * VARIABLE<br>
  * OUTPUT<br>
  * TIME_PERIODS<br>
</code></pre>

<h2>GLOBAL_CONTROL</h2>
Two columns: CONTROLLER, MODE<br>
<br>
<b><i>PLOT_ORIGINAL_TIME_INTERVAL (default: OFF)</i></b><br>
By default, data with time interval less than one day will be converted to daily as minimum time interval. This is an option for users who want to display the original data in the original time scales, such as 15 minutes.  Note that this is not recommended for more than half year simulation.<br>
<br>
<b><i>CALCULATE_SPECIFIED_RMSE_ONLY  (default: OFF)</i></b>    <br>
By default, RMS differences for all the matched time series in two DSS file will be calculated. Turn this on if users only have interest in the location specified in the OUTPUT block.<br>
<br>
<b><i>DONOT_SORT_STATION_NAME (default: OFF)</i></b>     <br>
By default, station names are sorted alphabetically. If users want the plot presented as the order in OUTPUT block, please turn this on.<br>
<br>
<b><i>DEFAULT_TIME_INTERVAL (default: 15MIN)</i></b><br>
In case of multiple time interval for same location, this is a filter for PART E.<br>
<br>
<b><i>COMPARE_MODE</i></b> <br>
<pre><code>1: observation only<br>
2: one model output only<br>
3: two model comparison<br>
4: one model output calibration<br>
5: two model output calibration comparison<br>
</code></pre>
For example,<br>
<pre><code>GLOBAL_CONTROL<br>
CONTROLLER                           MODE<br>
PLOT_ORIGINAL_TIME_INTERVAL           OFF<br>
CALCULATE_SPECIFIED_RMSE_ONLY         OFF<br>
DONOT_SORT_STATION_NAME               OFF<br>
COMPARE_MODE                          2<br>
DEFAULT_TIME_INTERVAL                 15MIN<br>
END <br>
</code></pre>
<h2>SCALAR</h2>
Two columns: NAME, VALUE<br>
<pre><code>*_FILE0:_*   Full path for observed DSS file<br>
*_NAME0:_*   A brief name for the observed data<br>
*_FILE1:_*   Full path for modeled DSS file<br>
*_NAME1:_*   A brief name for the modeled output<br>
*_FILE2:_*   Full path for the other modeled DSS file<br>
*_NAME2:_*   A brief name for the other modeled output<br>
*_OUTDIR:_*  Report output directory<br>
*_OUTFILE:_* Output HTML report name<br>
*_NOTE:_*    Notes for this report<br>
*_ASSUMPTIONS:_* Assumptions for this report<br>
*_MODELER_*:_* Name for the modeler  <br>
</code></pre>
For example,<br>
<pre><code>SCALAR<br>
NAME		VALUE<br>
FILE0		D:/delta/dsm2_v8/report/dssfiles/Apple.dss #input file 1<br>
NAME0		Observation<br>
FILE1		D:/delta/dsm2_v8/report/dssfiles/Apple.dss #input file 1<br>
NAME1		Apple<br>
FILE2		D:/delta/dsm2_v8/report/dssfiles/Banana.dss # input file 2<br>
NAME2		Banana<br>
OUTDIR      D:/delta/dsm2_v8/report/case2<br>
OUTFILE		DSM2_compare.html<br>
NOTE		"A long funny note"<br>
ASSUMPTIONS "I am assuming this is defined"<br>
MODELER 	Monkey<br>
END<br>
</code></pre>

<h2>VARIABLE</h2>
Four columns: NAME, REF0, REF1, REF2<br>
<br>
For example,<br>
<pre><code>VARIABLE <br>
NAME                         REF0                                REF1                                         REF2<br>
TEST1   FILE2:://RMID040/FLOW//15MIN//   FILE1:://RMID040/FLOW//15MIN//  FILE2:://RMID040/FLOW//15MIN//<br>
TEST2   FILE1:://RMID015/FLOW//15MIN//   FILE1:://ROLD034/FLOW//15MIN//  FILE2:://ROLD024/FLOW//15MIN//<br>
TEST3   FILE1:://ROLD024/FLOW//15MIN//   FILE2:://ROLD024/FLOW//15MIN//  FILE2:://ROLD024/EC//15MIN//   <br>
END<br>
</code></pre>

<h2>OUTPUT</h2>
One column: NAME<br>
<br>
<br>
For example,<br>
<pre><code>OUTPUT<br>
NAME<br>
TEST1<br>
TEST2<br>
TEST3<br>
ROLD024_FLOW<br>
ROLD034_FLOW<br>
RMID015_FLOW<br>
RMID040_FLOW<br>
RSAC054_STAGE<br>
RSAC075_STAGE<br>
RSAC081_STAGE<br>
RSAN018_EC<br>
RSAN032_EC<br>
ROLD024_EC<br>
END<br>
</code></pre>

<h2>TIME_PERIODS</h2>
Two columns: NAME, TIMEWINDOW<br>
<br>
<br>
For example,<br>
<pre><code>TIME_PERIODS<br>
NAME			TIMEWINDOW<br>
"Long Term"		"01OCT1974 0100 - 30SEP1982 2400"<br>
"Period 1"	"01OCT1974 0100 - 30SEP1978 2400"<br>
"Period 2"	"01OCT1978 0100 - 30SEP1982 2400"<br>
END<br>
</code></pre>