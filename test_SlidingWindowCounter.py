from SlidingWindowCounter import SlidingWindowCounter
from datetime import datetime, timedelta
from random import randint
from mock import MagicMock
from progress.bar import Bar
import time

def timing(func, *args):
    time1 = time.time()
    ret = func(*args)
    time2 = time.time()
    print '%s took %0.3f ms' % (func.func_name, (time2-time1)*1000.0)
    return ret

def naiveCounter(event_list, time):
    within_time = filter(lambda x: x > time, event_list)
    return len(within_time)

def test_naiveCounter():
    events = [ datetime.now() for x in range(100)]
    hr_ago = datetime.now() - timedelta(hours=1)
    assert len(events) == naiveCounter(events, hr_ago)

def test_SlidingWindowCounterHour():
    """this is a spesific edge case for counting hours over 0-23 hour interval"""
    startTime = datetime.strptime('Nov 8 2008 0:1:03', '%b %d %Y %H:%M:%S')
    window = startTime - timedelta(hours=1)
    swc = SlidingWindowCounter()

    while window < startTime:
        swc.now = MagicMock(return_value=window)
        swc.increnment()
        window += timedelta(minutes=1)

    assert swc.numLastHour() == 60


def test_SlidingWindowCounterMinute():
    """
        this is a spesific edge case for counting hours
        over 59-0 minute interval over diffrent hours
    """
    startTime = datetime.strptime('Nov 8 2008 0:0:05', '%b %d %Y %H:%M:%S')

    window = startTime - timedelta(minutes=1)
    swc = SlidingWindowCounter()

    while window < startTime:
        swc.now = MagicMock(return_value=window)
        swc.increnment()
        window += timedelta(seconds=1)

    assert swc.numLastMinute() == 60

def test_SlidingWindowCounterPruning():
    """
        test that the size of our index is never greater than 3
    """
    startTime = datetime.strptime('Nov 8 2008 0:0:05', '%b %d %Y %H:%M:%S')

    window = startTime - timedelta(hours=24)
    SlidingWindowCounter.now = MagicMock(return_value = window)
    swc = SlidingWindowCounter()

    while window < startTime:
        swc.now = MagicMock(return_value = window)
        swc.increnment()
        window += timedelta(minutes=20)

    assert len(swc.index) <= 3


def test_SlidingWindowCounter():
    """
        This integration test builds up a naive list and our data strucure
        and then adds events to both and then we output the diffrent
        runtimes and compare the results because they have to be the same.
        it also outputs the diffrent runtimes of th naive and SWC counting
        algorithims.
    """
    # test size and length
    TEST_HOURS = 3
    TEST_MAX_ENTRIES = 20

    print """Simulating 0-{0} events per second over a time period of {1} Hours,\
 This can take a moment""".format(TEST_MAX_ENTRIES,TEST_HOURS)

    startTime = datetime.now()
    window = datetime.now() - timedelta(hours = TEST_HOURS)

    eventList = []
    swc = SlidingWindowCounter()

    delta = timedelta(seconds = 1)
    bar = Bar('Generating', max=(60*60*TEST_HOURS))
    while window < startTime:
        window += delta
        r = randint(0,TEST_MAX_ENTRIES)
        for x in range(r):
            swc.now = MagicMock(return_value = window)
            swc.increnment()
            eventList.append(window)
        bar.next()
    bar.finish()

    lastSecond = startTime - timedelta(seconds = 1)
    lasMinute = startTime - timedelta(minutes = 1)
    lastHour = startTime - timedelta(hours = 1)

    swc.now = MagicMock(return_value = startTime)

    # Save the output from these fuctions but also print out the amount of
    # time that it took them to complete
    swcNumLastSecond = timing(swc.numLastSecond)
    naiveNumLastSecond = timing(naiveCounter, eventList, lastSecond)

    swcNumLastMinute = timing(swc.numLastMinute)
    naiveNumLastMinute = timing(naiveCounter, eventList, lasMinute)


    swcNumLastHour = timing(swc.numLastHour)
    naiveNumLastHour = timing(naiveCounter, eventList, lastHour)

    assert swcNumLastSecond == naiveNumLastSecond
    assert swcNumLastMinute == naiveNumLastMinute
    assert swcNumLastHour == naiveNumLastHour


if __name__ == '__main__':
    test_naiveCounter()
    test_SlidingWindowCounterPruning()
    test_SlidingWindowCounterHour()
    test_SlidingWindowCounterMinute()
    test_SlidingWindowCounter()
