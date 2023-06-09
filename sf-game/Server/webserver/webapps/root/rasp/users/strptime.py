"""Implementation of time.strptime().

This version was written to work in Jython 2.1 .  If you are running CPython
2.2.x or newer, please use the version of Modules/timemodule.c and
Lib/_strptime.py as found in CVS for CPython 2.3.x (CPython 2.2.0 requires
defining ``True = 1; False = 0``).

The main changes from the version in CVS for CPython 2.3.x is a caching
mechanism which improves performance dramatically.  LocaleTime().timezone is
also a true set and thus does not require all the tweaking of using a version
of Python lacking iterators.  List comprehensions were also removed from the
code.  All date-calculating code was made conditional based on requiring
datetime.  If you need the calculations you can find the code in the Python CVS
repository in the datetime code or in the dead-tree version of the 'Python
Cookbook' under the recipe for strptime() (last recipe in the book).
Subclassing of object and dict were also removed.

$Last Edit: 2003-09-15 $

"""
import time
try:
    import locale
except ImportError:
    class FakeLocale:

        """Faked locale module (for Jython compatibility)."""

        LC_TIME = None
        
        def getlocale(self, whatever):
            return (whatever, whatever)

    locale = FakeLocale()
    
import calendar
from re import compile as re_compile
from re import IGNORECASE
# Get datetime from Python's CVS: /python/nondist/sandbox/datetime/
try:
    from datetime import date as datetime_date
except ImportError:
    datetime_date = None
from thread import allocate_lock as _thread_allocate_lock

__author__ = "Brett Cannon"
__email__ = "brett@python.org"

__all__ = ['strptime']

# ----- START Code to replace Python 2.3 functionality -----
True, False = 1, 0

def sets_ImmutableSet(iterable):
    sets_dict = {}
    for item in iterable:
        sets_dict[item] = None
    return sets_dict

def enumerate(iterable):
    """Python 2.1-compatible enumerate function.

    """
    enum_list = []
    count = 0
    for item in iterable:
        enum_list.append((count, item))
        count += 1
    return enum_list

# ----- END Code to replace Python 2.3 functionality -----

def _getlang():
    # Figure out what the current language is set to.
    return locale.getlocale(locale.LC_TIME)

class LocaleTime:
    """Stores and handles locale-specific information related to time.

    ATTRIBUTES:
        f_weekday -- full weekday names (7-item list)
        a_weekday -- abbreviated weekday names (7-item list)
        f_month -- full month names (13-item list; dummy value in [0], which
                    is added by code)
        a_month -- abbreviated month names (13-item list, dummy value in
                    [0], which is added by code)
        am_pm -- AM/PM representation (2-item list)
        LC_date_time -- format string for date/time representation (string)
        LC_date -- format string for date representation (string)
        LC_time -- format string for time representation (string)
        timezone -- daylight- and non-daylight-savings timezone representation
                    (2-item list of sets)
        lang -- Language used by instance (2-item tuple)
    """

    def __init__(self):
        """Set all attributes.
        
        Order of methods called matters for dependency reasons.

        The locale language is set at the offset and then checked again before
        exiting.  This is to make sure that the attributes were not set with a
        mix of information from more than one locale.  This would most likely
        happen when using threads where one thread calls a locale-dependent
        function while another thread changes the locale while the function in
        the other thread is still running.  Proper coding would call for
        locks to prevent changing the locale while locale-dependent code is
        running.  The check here is done in case someone does not think about
        doing this.

        Only other possible issue is if someone changed the timezone and did
        not call tz.tzset .  That is an issue for the programmer, though,
        since changing the timezone is worthless without that call.
        
        """
        self.lang = _getlang()
        self.__calc_weekday()
        self.__calc_month()
        self.__calc_am_pm()
        self.__calc_timezone()
        self.__calc_date_time()
        if _getlang() != self.lang:
            raise ValueError("locale changed during initialization")

    def __pad(self, seq, front):
        # Add '' to seq to either the front (is True), else the back.
        seq = list(seq)
        if front:
            seq.insert(0, '')
        else:
            seq.append('')
        return seq

    def __calc_weekday(self):
        # Set self.a_weekday and self.f_weekday using the calendar
        # module.
        a_weekday = [calendar.day_abbr[i].lower() for i in range(7)]
        f_weekday = [calendar.day_name[i].lower() for i in range(7)]
        self.a_weekday = a_weekday
        self.f_weekday = f_weekday

    def __calc_month(self):
        # Set self.f_month and self.a_month using the calendar module.
        a_month = [calendar.month_abbr[i].lower() for i in range(13)]
        f_month = [calendar.month_name[i].lower() for i in range(13)]
        self.a_month = a_month
        self.f_month = f_month

    def __calc_am_pm(self):
        # Set self.am_pm by using time.strftime().

        # The magic date (1999,3,17,hour,44,55,2,76,0) is not really that
        # magical; just happened to have used it everywhere else where a
        # static date was needed.
        am_pm = []
        for hour in (01,22):
            time_tuple = (1999,3,17,hour,44,55,2,76,0)
            am_pm.append(time.strftime("%p", time_tuple).lower())
        self.am_pm = am_pm

    def __calc_date_time(self):
        # Set self.date_time, self.date, & self.time by using
        # time.strftime().

        # Use (1999,3,17,22,44,55,2,76,0) for magic date because the amount of
        # overloaded numbers is minimized.  The order in which searches for
        # values within the format string is very important; it eliminates
        # possible ambiguity for what something represents.
        time_tuple = (1999,3,17,22,44,55,2,76,0)
        date_time = [None, None, None]
        date_time[0] = time.strftime("%c", time_tuple).lower()
        date_time[1] = time.strftime("%x", time_tuple).lower()
        date_time[2] = time.strftime("%X", time_tuple).lower()
        replacement_pairs = [('%', '%%'), (self.f_weekday[2], '%A'),
                    (self.f_month[3], '%B'), (self.a_weekday[2], '%a'),
                    (self.a_month[3], '%b'), (self.am_pm[1], '%p'),
                    ('1999', '%Y'), ('99', '%y'), ('22', '%H'),
                    ('44', '%M'), ('55', '%S'), ('76', '%j'),
                    ('17', '%d'), ('03', '%m'), ('3', '%m'),
                    # '3' needed for when no leading zero.
                    ('2', '%w'), ('10', '%I')]
        for tz_values in self.timezone:
            for tz in tz_values.keys():
                replacement_pairs.append((tz, "%Z"))
        for offset,directive in ((0,'%c'), (1,'%x'), (2,'%X')):
            current_format = date_time[offset]
            for old, new in replacement_pairs:
                # Must deal with possible lack of locale info
                # manifesting itself as the empty string (e.g., Swedish's
                # lack of AM/PM info) or a platform returning a tuple of empty
                # strings (e.g., MacOS 9 having timezone as ('','')).
                if old:
                    current_format = current_format.replace(old, new)
            time_tuple = (1999,1,3,1,1,1,6,3,0)
            if time.strftime(directive, time_tuple).find('00'):
                U_W = '%U'
            else:
                U_W = '%W'
            date_time[offset] = current_format.replace('11', U_W)
        self.LC_date_time = date_time[0]
        self.LC_date = date_time[1]
        self.LC_time = date_time[2] 

    def __calc_timezone(self):
        # Set self.timezone by using time.tzname.
        # Do not worry about possibility of time.tzname[0] == timetzname[1]
        # and time.daylight; handle that in strptime .
        try:
            time.tzset()
        except AttributeError:
            pass
        no_saving = sets_ImmutableSet(["utc", "gmt", time.tzname[0].lower()])
        if time.daylight:
            pass
            has_saving = sets_ImmutableSet([time.tzname[1].lower()])
        else:
            pass
            has_saving = {}#sets_ImmutableSet([time.tzname[1].lower()])
        self.timezone = (no_saving, has_saving) #was has_saving


import UserDict
class TimeRE(UserDict.UserDict):
    """Handle conversion from format directives to regexes."""

    def __init__(self, locale_time=None):
        """Create keys/values.
        
        Order of execution is important for dependency reasons.
        
        """
        if locale_time:
            self.locale_time = locale_time
        else:
            self.locale_time = LocaleTime()
        base = UserDict.UserDict
        base.__init__(self, {
            # The " \d" part of the regex is to make %c from ANSI C work
            'd': r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
            'H': r"(?P<H>2[0-3]|[0-1]\d|\d)",
            'I': r"(?P<I>1[0-2]|0[1-9]|[1-9])",
'j': r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            'm': r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            'M': r"(?P<M>[0-5]\d|\d)",
            'S': r"(?P<S>6[0-1]|[0-5]\d|\d)",
            'U': r"(?P<U>5[0-3]|[0-4]\d|\d)",
            'w': r"(?P<w>[0-6])",
            # W is set below by using 'U'
            'y': r"(?P<y>\d\d)",
            #XXX: Does 'Y' need to worry about having less or more than
            #     4 digits?
            'Y': r"(?P<Y>\d\d\d\d)",
            'A': self.__seqToRE(self.locale_time.f_weekday, 'A'),
            'a': self.__seqToRE(self.locale_time.a_weekday, 'a'),
            'B': self.__seqToRE(self.locale_time.f_month[1:], 'B'),
            'b': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
            'p': self.__seqToRE(self.locale_time.am_pm, 'p'),
            '%': '%'})
        temp_list = []
        for tz_names in self.locale_time.timezone:
            for tz in tz_names.keys():
                temp_list.append(tz)
        base.__setitem__(self, 'Z', self.__seqToRE(temp_list, 'Z'))
        base.__setitem__(self, 'W', base.__getitem__(self, 'U'))
        base.__setitem__(self, 'c', self.pattern(self.locale_time.LC_date_time))
        base.__setitem__(self, 'x', self.pattern(self.locale_time.LC_date))
        base.__setitem__(self, 'X', self.pattern(self.locale_time.LC_time))

    def __seqToRE(self, to_convert, directive):
        """Convert a list to a regex string for matching a directive.
        
        Want possible matching values to be from longest to shortest.  This
        prevents the possibility of a match occuring for a value that also
        a substring of a larger value that should have matched (e.g., 'abc'
        matching when 'abcdef' should have been the match).
        
        """
        for value in to_convert:
            if value != '':
                break
        else:
            return ''
        to_sort = [(len(item), item) for item in to_convert]
        to_sort.sort()
        to_sort.reverse()
        to_convert = [item for length, item in to_sort]
        regex = '|'.join(to_convert)
        regex = '(?P<%s>%s' % (directive, regex)
        return '%s)' % regex

    def pattern(self, format):
        """Return regex pattern for the format string.

        Need to make sure that any characters that might be interpreted as
        regex syntax are escaped.

        """
        processed_format = ''
        # The sub() call escapes all characters that might be misconstrued
        # as regex syntax.
        regex_chars = re_compile(r"([\\.^$*+?{}\[\]|])")
        format = regex_chars.sub(r"\\\1", format)
        whitespace_replacement = re_compile('\s+')
        format = whitespace_replacement.sub('\s*', format)
        while format.find('%') != -1:
            directive_index = format.index('%')+1
            processed_format = "%s%s%s" % (processed_format,
                                           format[:directive_index-1],
                                           self[format[directive_index]])
            format = format[directive_index+1:]
        return "%s%s" % (processed_format, format)

    def compile(self, format):
        """Return a compiled re object for the format string."""
        return re_compile(self.pattern(format), IGNORECASE)

_cache_lock = _thread_allocate_lock()
# DO NOT modify _TimeRE_cache or _regex_cache without acquiring the cache lock
# first!
_TimeRE_cache = TimeRE()
_CACHE_MAX_SIZE = 5 # Max number of regexes stored in _regex_cache
_regex_cache = {}

def strptime(data_string, format="%a %b %d %H:%M:%S %Y"):
    """Return a time struct based on the input string and the format string."""
    global _TimeRE_cache
    _cache_lock.acquire()
    try:
        time_re = _TimeRE_cache
        locale_time = time_re.locale_time
        if _getlang() != locale_time.lang:
            _TimeRE_cache = TimeRE()
        if len(_regex_cache) > _CACHE_MAX_SIZE:
            _regex_cache.clear()
        format_regex = _regex_cache.get(format)
        if not format_regex:
            format_regex = time_re.compile(format)
            _regex_cache[format] = format_regex
    finally:
        _cache_lock.release()
    found = format_regex.match(data_string)
    if not found:
        raise ValueError("time data did not match format:  data=%s  fmt=%s" %
                         (data_string, format))
    if len(data_string) != found.end():
        raise ValueError("unconverted data remains: %s" %
                          data_string[found.end():])
    year = 1900
    month = day = 1
    hour = minute = second = 0
    tz = -1
    # weekday and julian defaulted to -1 so as to signal need to calculate values
    weekday = julian = -1
    found_dict = found.groupdict()
    for group_key in found_dict.keys():
        if group_key == 'y':
            year = int(found_dict['y'])
            # Open Group specification for strptime() states that a %y
            #value in the range of [00, 68] is in the century 2000, while
            #[69,99] is in the century 1900
            if year <= 68:
                year += 2000
            else:
                year += 1900
        elif group_key == 'Y':
            year = int(found_dict['Y'])
        elif group_key == 'm':
            month = int(found_dict['m'])
        elif group_key == 'B':
            month = locale_time.f_month.index(found_dict['B'].lower())
        elif group_key == 'b':
            month = locale_time.a_month.index(found_dict['b'].lower())
        elif group_key == 'd':
            day = int(found_dict['d'])
        elif group_key == 'H':
            hour = int(found_dict['H'])
        elif group_key == 'I':
            hour = int(found_dict['I'])
            ampm = found_dict.get('p', '').lower()
            # If there was no AM/PM indicator, we'll treat this like AM
            if ampm in ('', locale_time.am_pm[0]):
                # We're in AM so the hour is correct unless we're
                # looking at 12 midnight.
                # 12 midnight == 12 AM == hour 0
                if hour == 12:
                    hour = 0
            elif ampm == locale_time.am_pm[1]:
                # We're in PM so we need to add 12 to the hour unless
                # we're looking at 12 noon.
                # 12 noon == 12 PM == hour 12
                if hour != 12:
                    hour += 12
        elif group_key == 'M':
            minute = int(found_dict['M'])
        elif group_key == 'S':
            second = int(found_dict['S'])
        elif group_key == 'A':
            weekday = locale_time.f_weekday.index(found_dict['A'].lower())
        elif group_key == 'a':
            weekday = locale_time.a_weekday.index(found_dict['a'].lower())
        elif group_key == 'w':
            weekday = int(found_dict['w'])
            if weekday == 0:
                weekday = 6
            else:
                weekday -= 1
        elif group_key == 'j':
            julian = int(found_dict['j'])
        elif group_key == 'Z':
            # Since -1 is default value only need to worry about setting tz if
            # it can be something other than -1.
            found_zone = found_dict['Z'].lower()
            for value, tz_values in enumerate(locale_time.timezone):
                if found_zone in tz_values:
                    # Deal with bad locale setup where timezone names are the
                    # same and yet time.daylight is true; too ambiguous to
                    # be able to tell what timezone has daylight savings
                    if time.tzname[0] == time.tzname[1] and \
                       time.daylight:
                            break
                    else:
                        tz = value
                        break
    # Cannot pre-calculate datetime_date() since can change in Julian
    #calculation and thus could have different value for the day of the week
    #calculation
    if datetime_date:
        if julian == -1:
            # Need to add 1 to result since first day of the year is 1, not 0.
            julian = datetime_date(year, month, day).toordinal() - \
                      datetime_date(year, 1, 1).toordinal() + 1
        else:  # Assume that if they bothered to include Julian day it will
               #be accurate
            datetime_result = datetime_date.fromordinal((julian - 1) + datetime_date(year, 1, 1).toordinal())
            year = datetime_result.year
            month = datetime_result.month
            day = datetime_result.day
        if weekday == -1:
            weekday = datetime_date(year, month, day).weekday()
    return (year, month, day, hour, minute, second, weekday, julian, tz)