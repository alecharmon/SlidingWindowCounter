from OrderedDefaultDict import OrderedDefaultDict
from TimeUnit import Hour
from datetime import datetime, timedelta

class SlidingWindowCounter(object):
    """
        SlidingWindowCounter:
        manages an index of hours and increments seconds
        get count of LastHour, LastMinute, and LastSecond Windows
    """
    def __init__(self):
        self.index = OrderedDefaultDict(lambda: Hour())
        self.lastPruned = self.now()

    def parseTime(self, time):
        time = time.strftime('%H:%M:%S')
        return map(int, time.split(':'))

    def pruneIndex(self):
        if len(self.index.keys()) > 2:
            keys = self.index.keys()[:-2]
            for key in keys:
                del self.index[key]

    def now(self):
        """
            Made a wrapper class method around datetime.now() for stubbing out
            return values for testing
        """
        return datetime.now()

    def increnment(self):
        """void increnment method"""
        now = self.now()
        hour, minute, second = self.parseTime(now)

        # increments a spesifc second
        self.index[hour][minute].increnment(second)

        # this is optinal but seemed like a good idea, keeping the tree as small
        # as possible
        if self.lastPruned < self.now() - timedelta(hours = 1):
            self.pruneIndex()
            self.lastPruned = self.now()

    def numLastSecond(self):
        secondAgo = self.now() - timedelta(seconds=1)
        hourSa, minuteSa, secondSa = self.parseTime(secondAgo)

        return self.index[hourSa][minuteSa].sumIndexGTET(secondSa)

    def numLastMinute(self):
        now = self.now()
        minuteAgo = now - timedelta(minutes=1)

        hour, minute, _ = self.parseTime(now)
        hourMa, minuteMa, secondMa = self.parseTime(minuteAgo)

        # Since since we know that we want everything from the last minute
        # we know that everything in the current (now) minute is included in
        # that count
        minutes = self.index[hour][minute].count

        seconds = self.index[hourMa][minuteMa].sumIndexGTET(secondMa)

        return minutes + seconds

    def numLastHour(self):
        now = self.now()
        hourAgo = now - timedelta(hours=1)

        hour, _, _ = self.parseTime(now)
        hourHa, minuteHa, secondHa = self.parseTime(hourAgo)

        # Simlar to what was seen in numLastMinute() we know that every count
        # in the current hour is a part of our final sum
        hours = self.index[hour].count
        # since we dont want to double count (a subsection of minuteHa is not in
        # our final) we exclude minuteHa and just count all the minutes after it
        # then we find the minutes count seperatly
        minutes = self.index[hourHa].sumIndexGTET(minuteHa+1)
        seconds = self.index[hourHa][minuteHa].sumIndexGTET(secondHa)

        return hours+minutes+seconds
