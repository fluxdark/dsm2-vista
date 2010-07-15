import sys
import vdss, vutils, vdisplay
import js_data
import logging
class PlotType:
    TIME_SERIES="timeseries"
    EXCEEDANCE="exceedance"
class PathnameMap:
    def __init__(self, name):
        self.var_name = name;
        self.report_type = "Average"
        self.path1 = None
        self.path2 = None
        self.var_category = ""
def open_dss(dssfile):
    group = vutils.opendss(dssfile)
    if group == None:
        print "No dss file named: %s found!" % (dssfile)
    return group
#
def get_ref(group, path, calculate_dts=0):
    if calculate_dts==1:
        return None # TBD:
    refs = vdss.findpath(group, path)
    if refs == None:
        print "No data found for %s and %s" % (group, path)
    else:
        return refs[0]
def get_units_of_ref(ref):
    if ref != None:
        d=ref.data
        return d.attributes.YUnits
    return ""
def get_units(ref1, ref2):
    if ref1==None:
        if ref2==None:
            return ""
        else:
            return get_units_of_ref(ref2)
    else:
        return get_units_of_ref(ref1)
def get_type_of_ref(ref):
    if ref != None:
        p=ref.pathname
        return p.getPart(p.C_PART)
    return ""
def get_type(ref1,ref2):
    if ref1==None:
        if ref2==None:
            return ""
        else:
            return get_type_of_ref(ref2)
    else:
        return get_type_of_ref(ref1)
def convert_to_date(time_val):
    from java.util import TimeZone, Date
    return Date(time_val.date.time - TimeZone.getDefault().getRawOffset())
def multi_iterator(dsarray, filter=None):
    from vista.set import MultiIterator, Constants
    if filter == None:
        iterator = MultiIterator(dsarray)
    else:
        iterator = MultiIterator(dsarray, filter)
    return iterator
def extract_name_from_ref(ref):
    p = ref.pathname
    return "%s @ %s" % (p.getPart(p.C_PART), p.getPart(p.B_PART))
def build_data_array(ref1, ref2):
    from vista.set import Constants
    from vtimeseries import time
    import math
    if (ref1==None and ref2==None):
        return []
    iterator = multi_iterator([ref1.data, ref2.data], Constants.DEFAULT_FLAG_FILTER)
    darray=[]
    time_str = None
    while not iterator.atEnd():
        index = iterator.getIndex();
        e = iterator.getElement();
        date = convert_to_date(time(e.getXString()))
        darray.append((date.time, e.getY(0), e.getY(1)))
        iterator.advance();
    return darray
def sort(ref):
    from vista.set import Constants
    from vista.set import ElementFilterIterator
    dx=[]
    iter=ElementFilterIterator(ref.data.iterator, Constants.DEFAULT_FLAG_FILTER)
    while not iter.atEnd():
        dx.append(iter.element.y)
        iter.advance()
    dx.sort()
    return dx
def build_exceedance_array(ref1, ref2):
    from java.lang import Math
    x1=sort(ref1)
    x2=sort(ref2)
    darray=[]
    i=0
    n=int(Math.min(len(x1),len(x2)))
    while i < n:
        darray.append((100.0-100.0*float(i)/(n+1),x1[i],x2[i]))
        i=i+1
    return darray
def parse_template_file(template_file):
    from gov.ca.dsm2.input.parser import Parser
    p = Parser()                                 
    tables = p.parseModel(template_file)
    #load scalars into a map
    scalar_table = tables.getTableNamed("SCALAR")
    scalar_values = scalar_table.getValues()
    nscalars = scalar_values.size()
    scalars = {}
    for i in range(nscalars):
        name = scalar_table.getValue(i, "NAME")
        value = scalar_table.getValue(i, "VALUE")
        scalars[name] = value
    # load pathname mapping into a map
    pathname_mapping_table = tables.getTableNamed("PATHNAME_MAPPING")
    pmap_values = pathname_mapping_table.getValues()
    nvalues = pmap_values.size()
    pathname_maps=[]
    for i in range(nvalues):
        var_name = pathname_mapping_table.getValue(i, "VARIABLE")
        path_map = PathnameMap(var_name)
        path_map.report_type = pathname_mapping_table.getValue(i, "REPORT_TYPE")
        path_map.path1 = pathname_mapping_table.getValue(i, "PATH1")
        path_map.path2 = pathname_mapping_table.getValue(i, "PATH2")
        path_map.var_category = pathname_mapping_table.getValue(i, "VAR_CATEGORY")
        if path_map.path2 == None:
            path_map.path2 = path_map.path1
        pathname_maps.append(path_map)
    timewindows = []
    timewindow_table = tables.getTableNamed("TIME_PERIODS")
    tw_values = timewindow_table.getValues();
    return scalars, pathname_maps, tw_values
def do_processing(scalars, pathname_maps, tw_values):
    # open files 1 and file 2 and loop over to plot
    from java.util import Date
    dss_group1 = vutils.opendss(scalars['FILE1'])
    dss_group2 = vutils.opendss(scalars['FILE2'])
    output_file=scalars['OUTFILE']
    data_output_file = output_file.split(".")[0]+".js"
    fh=open(data_output_file,'w')
    print >> fh, """/*
    Comparison Output File
    Generated on : %s
    */"""%(str(Date()))
    js_data.write_begin_data_array(fh);
    if dss_group1 == None or dss_group2 == None:
        sys.exit(2);
    dataIndex=0
    for path_map in pathname_maps:
        dataIndex=dataIndex+1
        logging.debug('Working on index: %d'%dataIndex)
        if dataIndex>1:
            fh.write(",")
        #path_map = pathname_mapping[var_name]
        var_name = path_map.var_name
        calculate_dts=0
        if path_map.report_type == 'Exceedance_Post':
            calculate_dts=1
        ref1 = get_ref(dss_group1, path_map.path1,calculate_dts)
        ref2 = get_ref(dss_group2, path_map.path2,calculate_dts)
        if (ref1==None or ref2==None): 
            continue
        series_name = [scalars['NAME1'],scalars['NAME2']]
        data_units=get_units(ref1,ref2)
        data_type=get_type(ref1,ref2)
        if path_map.report_type == 'Average':
            write_plot_data(fh, build_data_array(ref1,ref2), dataIndex, "Average %s"%path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Time", PlotType.TIME_SERIES)
        elif path_map.report_type == 'Exceedance':
            write_plot_data(fh, build_exceedance_array(ref1,ref2), dataIndex, "Exceedance %s" %path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Percent at or above", PlotType.EXCEEDANCE)
        elif path_map.report_type == 'Avg_Excd':
            write_plot_data(fh, build_data_array(ref1,ref2), dataIndex, "Average %s"%path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Time", PlotType.TIME_SERIES)
            write_plot_data(fh, build_exceedance_array(ref1,ref2), dataIndex, "Exceedance %s"%path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Percent at or above", PlotType.EXCEEDANCE)
        elif path_map.report_type == 'Timeseries':
            write_plot_data(fh, build_data_array(ref1,ref2), dataIndex, "Average %s"%path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Time", PlotType.TIME_SERIES)
        elif path_map.report_type == 'Exceedance_Post':
            write_plot_data(fh, build_exceedance_array(ref1,ref2), dataIndex, "Exceedance %s"%path_map.var_name.replace('"',''), series_name, "%s(%s)"%(data_type,data_units), "Percent at or above", PlotType.EXCEEDANCE)
    js_data.write_end_data_array(fh);
    logging.debug('Writing end of data array')
    fh.close()
    # Generate the main html file
    fh=open(scalars['OUTFILE'],'w')
    print >> fh, """ 
<html>
<head>
<title>Calsim Report: %s vs %s</title>
<script type="text/javascript" src="%s"></script>
<script type="text/javascript" src="protovis-d3.3.js"></script>
<script type="text/javascript" src="plots.js"></script>
<script type="text/javascript" src="jquery-1.4.2.min.js"></script> 
<link rel="stylesheet" type="text/css" media="print" href="print.css" /> 
<link rel="stylesheet" type="text/css" media="screen" href="screen.css" /> 
</head>
"""%(scalars['NAME1'],scalars['NAME2'],data_output_file)
    write_water_balance_table(fh,dss_group1, dss_group2, scalars, pathname_maps,tw_values)
    print >> fh, """<script type="text/javascript"> 
    function clear_and_draw(sdate, edate){
        $('.plot').empty();
        n=data.length
        plot_diff = $('input[name=diff_plot]').is(':checked') ? 1 : 0 ;
        for(i=0; i < n; i++){
            var div_id = "fig"+(i+1);
            if (data[i]==null) continue;
            if ($("#"+div_id).length==0){
                $("body").append('<a href="#'+div_id+'"><div class="plot" id="'+div_id+'"></div></a>');
            }
            if (data[i].plot_type=="timeseries"){
                plots.time_series_plot(div_id,data[i],plot_diff,sdate,edate);
            }else if (data[i].plot_type=="exceedance"){
                plots.exceedance_plot(div_id,data[i],null,sdate,edate);
            }
        }
        // update links
    };
    $(document).ready(clear_and_draw(null,null));
    $('#system-water-balance-table tr').click(function(){
        var_name = $($(this).find('td')[0]).text();
        var svg_element = $('div').filter(function(){ return $(this).text().indexOf(var_name)>=0;})
        if (svg_element && svg_element.length > 0){
            anchor_name = $($(svg_element[0]).parent()).attr("href");
            window.location.href=window.location.href.split('#')[0]+anchor_name;
        }
    });
</script> 
<script type="text/javascript"> 
    function extract_date(date_str){
        date_fields=date_str.split(",");
        return new Date(date_fields[0],date_fields[1],date_fields[2]);
    }
    $('#time-window-select').change(function(){
        var changed_val = $('#time-window-select option:selected').val().split("-");
        clear_and_draw(extract_date(changed_val[0]),extract_date(changed_val[1]));
    });
    $('#threshold').change(function(){
        set_diff_threshold($('#threshold').val());
    });
    $('input[name=diff_plot]').change(function(){
        var changed_val = $('#time-window-select option:selected').val().split("-");
        clear_and_draw(extract_date(changed_val[0]),extract_date(changed_val[1]));
    });

    function set_diff_threshold(threshold){
        $('td').each(function(){ 
            if ($(this).text().search('%')>=0){
                if(Math.abs(parseFloat($(this).text().split('%')[0])) >= threshold){
                    $(this).addClass('large-diff');
                }else{
                    $(this).removeClass('large-diff');
                } 
            }
        });
    }
    set_diff_threshold($('#threshold').val());
</script> 
 
</body> 
 
</html>"""
    fh.close()    
    logging.debug('Closed out data file')
def cfs2taf(data):
    from vista.report import TSMath
    data_taf = TSMath.createCopy(data)
    TSMath.cfs2taf(data_taf)
    return data_taf
def sum(data, tw):
    import vmath
    try:
        return vmath.total(data.createSlice(tw))
    except:
        return float('nan')
def format_timewindow(tw):
    from vista.time import SubTimeFormat
    year_format = SubTimeFormat('yyyy')
    return tw.startTime.format(year_format) + "-" + tw.endTime.format(year_format)
def format_time_as_year_month_day(t):
    from java.util import Calendar, TimeZone
    gmtCal = Calendar.getInstance(TimeZone.getTimeZone('GMT'))
    gmtCal.setTime(t.date)
    return "%d,%d,%d"%(gmtCal.get(Calendar.YEAR),gmtCal.get(Calendar.MONTH),gmtCal.get(Calendar.DATE))
def timewindow_option_value(tw):
    return format_time_as_year_month_day(tw.startTime)+"-"+format_time_as_year_month_day(tw.endTime)
#
def write_water_balance_table(fh, dss_group1,dss_group2,scalars,pathname_maps,tw_values):
    import vtimeseries
    print >> fh, "<h1>System Water Balance Comparison: %s vs %s</h1>"%(scalars['NAME1'], scalars['NAME2'])
    print >> fh, '<div id="note">Note: %s</div>'%(scalars['NOTE'].replace('"',''))
    print >> fh, '<div id="assumptions">Assumptions: %s</div>'%(scalars['ASSUMPTIONS'].replace('"',''))
    
    print >> fh, """<div id="control-panel"> 
<select name="tw" id="time-window-select"> 
"""
    for i in range(len(tw_values)):
        if i==0:
            selected = 'selected="selected"'
        else:
            selected = ""
        print >> fh, '<option value="%s" %s>%s</option>'%(timewindow_option_value(vtimeseries.timewindow(tw_values[i][1].replace('"',''))), selected,tw_values[i][0].replace('"','')) 
    print >> fh, """ 
</select> 
<div>
    Show differences on plot:<input type="checkbox" name="diff_plot" value="1"/>
</div>
<div> 
    Threshold value to highlight differences
    <input type="text" id="threshold" value="50"/> 
</div> 
</div> 
    """
    time_windows = map(lambda val: val[1].replace('"',''), tw_values)
    tws = map(lambda x: vtimeseries.timewindow(x), time_windows)
    print >> fh, '<table id="system-water-balance-table" class="alt-highlight">'
    print >> fh, '<caption>System Water Balance Table</caption>'
    print >> fh, '<tr><td colspan="4"></td>'
    for i in range(len(tws)):
        print >> fh, '<td colspan="4" class="timewindow">%s</td>'%tw_values[i][0].replace('"','')
    print >> fh, "</tr>"
    print >> fh, '<tr><td colspan="4"></td>'
    for tw in tws:
        print >> fh, '<td colspan="4" class="timewindow">%s</td>'%format_timewindow(tw)
    print >> fh, "</tr>"
    index=0
    for path_map in pathname_maps:
        var_name = path_map.var_name
        calculate_dts=0
        if path_map.report_type == 'Exceedance_Post':
            calculate_dts=1
        ref1 = get_ref(dss_group1, path_map.path1,calculate_dts)
        ref2 = get_ref(dss_group2, path_map.path2,calculate_dts)
        print >> fh, '<tr class="%s">'%("d"+str(index%2))
        if (ref1==None or ref2==None):
            logging.debug("No data for %s"%path_map.var_name)
        if ref1 != None:
            logging.debug("No data for %s"%ref1)
            data1=cfs2taf(ref1.data)
        else:
            data1=None
        if ref2 != None:
            logging.debug("No data for %s"%ref2)
            data2=cfs2taf(ref2.data)
        else:
            data2=None
        if path_map.var_category in ("RF", "DI", "DO", "DE", "SWPSOD", "CVPSOD"):
            print >> fh, '<td colspan="4">%s</td>'%(path_map.var_name.replace('"',''))
            for tw in tws:
                s1=sum(data1, tw)
                s2=sum(data2, tw)
                diff=s2-s1
                if s1!=0:
                    pct_diff=diff/s1*100.0
                else:
                    pct_diff=float('nan')
                print >> fh, "<td>%0.1f</td><td>%0.1f</td><td>%0.1f</td><td>%0.1f %%</td>"%(s1,s2,diff,pct_diff)
        print >> fh, "</tr>"
        index=index+1
    print >> fh, '</table>'
#
def show_gui():
    """
    Shows a GUI to select dss files to compare and select an input file
    """
    from javax.swing import JPanel, JFrame, JButton, SpringLayout, JTextBox
    from javax.swing.border import LineBorder
    textBox1 = JTextBox()
    textBox2 = JTextBox()
    file1ChooseButton = JButton("Choose File")
    file2ChooseButton = JButton("Choose File")
    contentPane = JPanel(SpringLayout())
    contentPane.setBorder(LineBorder(Color.blue))
    contentPane.add(JLabel("Alternative DSS File"))
    contentPane.add(textBox1)
    contentPane.add(file1ChooseButton)
    contentPane.add(JLabel("Base DSS File"))
    contentPane.add(textBox2)
    contentPane.add(file2ChooseButton)
    fr = JFrame("Calsim Report Generator")
    fr.contentPane().add(contentPane)
    fr.pack();fr.show();
#
def write_plot_data(fh, data, dataIndex,  title, series_name, yaxis, xaxis, plot_type):
    js_data.write_file(fh, data, dataIndex, title, series_name, yaxis, xaxis, plot_type);
#
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) != 2:
        print 'Usage: dss_compare template.inp'
        exit(1)
    template_file = sys.argv[1]
    logging.debug('Parsing input template file %s'%template_file)
    #parse template file
    scalars, pathname_maps, tw_values = parse_template_file(template_file)
    # do processing
    do_processing(scalars, pathname_maps, tw_values)
    logging.debug('Done processing. The end!')
    sys.exit(0)
