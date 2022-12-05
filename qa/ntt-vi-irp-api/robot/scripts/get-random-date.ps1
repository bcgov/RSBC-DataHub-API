param(
[parameter(Mandatory=$True)][DateTime]$StartDate,
[parameter(Mandatory=$True)][DateTime]$EndDate,
[String]$Format
)

# The ${Format} parameter is optional. If not given, this script will return an ISO date (2022-11-10).
#
# If ${Format} is one character long, the date will be in a standard format described below. If
# ${Format} is more than one character long, it is taken as a custom date format string.
#
# For the one-character (standard) date format, these letters give these formats:
# https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-date-and-time-format-string
#
# - d: short date        2022-11-10
# - D: long date         Monday, April 19, 1948
# - f: full date         Saturday, December 17, 2005 17:23
# - F: long full date    Tuesday, March 17, 2009 08:01:41
# - g: general date      1930-04-07 16:08
# - G: long general date 1972-03-17 17:36:47
# - m: month date        January 12
# - o: round-trip        1938-07-29T10:01:31.3387264
# - r: RFC1123 date      Sun, 22 Sep 1946 04:59:11 GMT
# - s: sortable date     1986-03-25T17:19:20
# - t: time              14:03
# - T: more time         15:23:28
# - u: universal time    1934-08-19 23:49:45Z
# - U: more universal    Sunday, March 17, 1968 20:52:47
# - y: year date         July 1974
#
# For custom date strings, these are the formats:
# https://devblogs.microsoft.com/scripting/create-custom-date-formats-with-powershell/
#
#
# c       Date and time    Fri Jun 16 10:31:27 2015    
# D       Date in mm/dd/yy format    06/14/06    
# x       Date in standard format for locale    09/12/15 for English-US    
# C       Century    20 for 2015    
# Y, G    Year in 4-digit format    2015    
# y, g    Year in 2-digit format    15    
# b, h    Month name – abbreviated    Jan    
# B       Month name – full    January    
# m       Month number    06    
# W, U    Week of the year – zero based    00-52    
# V       Week of the year – one based    01-53    
# a       Day of the week – abbreviated name    Mon    
# A       Day of the week – full name    Monday    
# u, w    Day of the week – number    Monday = 1    
# d       Day of the month – 2 digits    05    
# e       Day of the month – digit preceded by a space     
# 5       j    Day of the year    1-366    
# p       AM or PM     PM    
# r       Time in 12-hour format    09:15:36 AM    
# R       Time in 24-hour format – no seconds    17:45    
# T, X    Time in 24 hour format    17:45:52    
# Z       Time zone offset from Universal Time Coordinate UTC    07    
# H, k    Hour in 24-hour format    17    
# I, l    Hour in 12 hour format    05    
# M       Minutes    35    
# S       Seconds    05    
# s       Seconds elapsed since January 1, 1970    00:00:00 1150451174.95705    
# n       newline character    n    
# t       Tab character    t
#
# In this example, format the date for NTT VIPS integration APIs:
# .\get-random-date.ps1 "1930-01-01" "2012-01-01" "%Y-%m-%dT00:00:00.000%Z:00" 
# 1959-09-26T00:00:00.000-07:00
#
#
    # From: https://gist.github.com/emyann/826d9f799fb5f0d115ac3b9eaaa3a958
    function Get-RandomDateBetween{
        <#
        .EXAMPLE
        Get-RandomDateBetween -StartDate (Get-Date) -EndDate (Get-Date).AddDays(15) -Format "d"
        #>
        [Cmdletbinding()]
        param(
            [parameter(Mandatory=$True)][DateTime]$StartDate,
            [parameter(Mandatory=$True)][DateTime]$EndDate,
            [String]$DateFormat
            )

        process{
            if ([string]::IsNullOrEmpty(${DateFormat}))
            {
                return Get-Random -Minimum $StartDate.Ticks -Maximum $EndDate.Ticks | Get-Date -Format 'd'
            }
            elseif (${Format}.Length -gt 1)
            {
                return Get-Random -Minimum $StartDate.Ticks -Maximum $EndDate.Ticks | Get-Date -UFormat ${Format}
            }
            else
            {
               return Get-Random -Minimum $StartDate.Ticks -Maximum $EndDate.Ticks | Get-Date -Format ${Format}
            }
        }
    }

    
    function Get-RandomTimeBetween{
      <#
        .EXAMPLE
        Get-RandomTimeBetween -StartTime "08:30" -EndTime "16:30"
        #>
         [Cmdletbinding()]
        param(
            [parameter(Mandatory=$True)][string]$StartTime,
            [parameter(Mandatory=$True)][string]$EndTime
            )
        begin{
            $minuteTimeArray = @("00","15","30","45")
        }    
        process{
            $rangeHours = @($StartTime.Split(":")[0],$EndTime.Split(":")[0])
            $hourTime = Get-Random -Minimum $rangeHours[0] -Maximum $rangeHours[1]
            $minuteTime = "00"
            if($hourTime -ne $rangeHours[0] -and $hourTime -ne $rangeHours[1]){
                $minuteTime = Get-Random $minuteTimeArray
                return "${hourTime}:${minuteTime}"
            }
            elseif ($hourTime -eq $rangeHours[0]) { # hour is the same as the start time so we ensure the minute time is higher
                $minuteTime = $minuteTimeArray | ?{ [int]$_ -ge [int]$StartTime.Split(":")[1] } | Get-Random # Pick the next quarter
                #If there is no quarter available (eg 09:50) we jump to the next hour (10:00)
                return (.{If(-not $minuteTime){ "${[int]hourTime+1}:00" }else{ "${hourTime}:${minuteTime}" }})               
             
            }else { # hour is the same as the end time
                #By sorting the array, 00 will be pick if no close hour quarter is found
                $minuteTime = $minuteTimeArray | Sort-Object -Descending | ?{ [int]$_ -le [int]$EndTime.Split(":")[1] } | Get-Random
                return "${hourTime}:${minuteTime}"
            }
        }
    }

${RANDOM_DATE} = Get-RandomDateBetween -StartDate ${StartDate} -EndDate ${EndDate} -DateFormat ${Format}
${RANDOM_DATE}