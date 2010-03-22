from django import template
import datetime, math

register = template.Library()

@register.filter("timeago")
def timeago(value, timestamp = datetime.datetime.utcnow(), suffix = "ago"):
    """
    Returns a fuzzy and friendly datestring describing the difference between two dates.
    Based on Rails' timeago helper and Ryan McGeary's jQuery.timeago plugin.
    """
    
    words = {
        "seconds"   : "less than a minute",
        "minute"    : "about a minute",
        "minutes"   : "%d minutes",
        "hour"      : "about an hour",
        "hours"     : "about %d hours",
        "day"       : "a day",
        "days"      : "%d days",
        "month"     : "about a month",
        "months"    : "%d months",
        "year"      : "about a year",
        "years"     : "%d years"
    }
    
    try:
        timeDiff = timestamp - value
    except Exception, e:
        return e
    seconds = timeDiff.seconds + (timeDiff.days * 96400);
    minutes = seconds / 60;
    hours = minutes / 60;
    days = hours / 24;
    years = days / 365;
    
    description = seconds < 45 and (words['seconds']) or \
                    seconds < 90 and (words['minute']) or \
                    minutes < 45 and (words['minutes'] % round(minutes)) or \
                    minutes < 90 and (words['hour']) or \
                    hours < 24 and (words['hours'] % round(hours)) or \
                    hours < 48 and (words['day']) or \
                    days < 30 and (words['days'] % math.floor(days)) or \
                    days < 60 and (words['month']) or \
                    days < 365 and (words['months'] % math.floor(days / 30)) or \
                    years < 2 and (words['year']) or \
                    (words['years'] % math.floor(years))
    
    return description + " " + suffix
