# Introduction #

Time functions are available in the [vista.time](http://dsm2-vista.googlecode.com/svn/trunk/vista/doc/vista/time/package-summary.html) package. These functions provide ability to define a [time point](http://dsm2-vista.googlecode.com/svn/trunk/vista/doc/vista/time/Time.html), a [time interval](http://dsm2-vista.googlecode.com/svn/trunk/vista/doc/vista/time/TimeInterval.html) (in minutes) and a [time window](http://dsm2-vista.googlecode.com/svn/trunk/vista/doc/vista/time/TimeWindow.html).

# Time Formatting #

To read in a time from a string in jython in [java's DateFormat](http://java.sun.com/j2se/1.4.2/docs/api/java/text/SimpleDateFormat.html)
```
>>> t1 = time('20041219','yyyyMMdd')
```

To convert it to a time using standard format (military style)
```
>>> t2 = time(t1)
```

To get the string representation of the time
```
>>> print 'Time in original format: ', str(t1), ' & the same time in standard format: ', str(t2) 
Time in original format:  20041219  & the same time in standard format:  18DEC2004 2400
```

To get the string representation applying  different format style
```
>>> from vista.time import DefaultTimeFormat
>>> t1.format(DefaultTimeFormat('yyyyMMdd hhmm'))
u'20060101 0116'
```
**Note**: The above returns a "unicode" string. use the str() function on it to get a typical string


To get the equivalent (java.util.Date) in TimeZone GMT do as follows
```
>>> print t1.date
Sun Dec 19 00:00:00 PST 2004
```

if you want to convert this to a local timezone use the following to get offset in millisecs
```
>>> offset=TimeZone.getDefault().getOffset(t1.date.time)
>>> from java.util import Date
>>> Date(t1.date.time-offset)
Mon Jan 01 01:00:00 PST 1990
```

To get time from TimeElement te
```
>>> time(long(te.x)).date
```