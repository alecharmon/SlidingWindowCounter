## Prompt
This is a counter which
keeps track of how many events have occurred in a given window of time. For the
purposes of this test, we'll assume that we want to know how many events have
occurred in the last: - second - minute - hour
An event is completely absent of any state. We only want to record that an event
occurred at a given time. Please implement four functions:

- `increment()`, which records that an event occurred at the current time (time.Now() in whatever programming language you're using), and returns nothing.
-`numLastSecond()` which returns the number of increment events which have occurred in the last second.
- `numLastMinute()` which returns the number of increment events which have occurred in the last minute.
- `numLastHour()` which returns the number of increment events which have occurred in the last hour.
We'll assume that we don't want to know about anything which happened over an hour
ago, but your solution should take into account that we might want to extend this
counter to support any arbitrary amount of time, and to do it relatively efficiently

## USAGE
The module was designed to just be imported
```
from SlidingWindowCounter import SlidingWindowCounter
swc = SlidingWindowCounter()
swc.increnment()
```

## TESTING
In order to run the integration tests run `python test_SlidingWindowCounter.y`, though the implementation of the module only uses pythons core modules, I did import some extra classes here so use `pip install -rrequirements.txt` install. The most important being `mock` which allowed me to stub out the calls to `datetime.now()`. This was prompted from the time-based nature of the assignment it was important to have tests that could demonstrate that the module did what it is supposed to without actually having to wait for more than a minute or so.

## Data Structures Used
So each level of precision is contained within its own `TimeUnit` node which, has its own collection of children called here an index along with their own count.This is because each time unit is inherently the aggregate of all of the smaller units of time that composes it. Because of this and the child/parent structure, it was possible to never have to worry about the incrementing intermediary levels but rather just increment the bottom level and pass chain the increment functions to automatically increment all of the lowest level's parent.


The other major decision was to use what is called here an `OrderedDefaultDict`, which is a combination of `OrderedDict` and `defaultdict`. This lets us create children nodes with ease because if we try to increment a second that has not been created the programmer doesn't have to worry about creating it, the same goes for hours and minutes. It also only creates objects in memory when absolutely necessary. The ordered component is also important because we only increment the count for a time if it is currently that time. since the current time is always greater than the time before it implies we are essentially already getting it in order. So by using an OrderedDict, we make sure we can reference each second really fast because we already have the key but also we can iterate over the values of each time unit without having to worry about sorting them based on their keys first.

## Thoughts About Input Data
I actually got very distracted when writing my tests because I kept on increasing the input size or the window size to see how the performance of the module changed. Since it was a pretty constant operation in increment the bottom most node it was able to do about 5 thousand increments per second (my laptop is a bit outdated though).  What the performance tests show is that a number of operations that we have to perform are bounded by the window of time rather than a number of events created. The worst case for our memory usage is if there is at least one event for each second of two hours which would be about 7,200 ints or about 14k which is a pretty reasonable worse case scenario. Although the choice of using ints here was just an assumption, we could easily use longs or shorts if that fit our needs better.

## Accommodating Longer Windows of Time
Yhe `TimeUnit ` structure really lends itself well to if we wanted to add days or use units smaller than seconds. If we wanted to add days we would essentially have our SWC control an index of days which have hour type children. We would also have to add a  `numLastDay()` function which would pretty much mimic the procedure of the previously defined counting functions.

if we wanted to maintain a larger amount of input we could implement a map reduce type distribution of the module across multiple machines. If there was a load balancer sitting between this machine nodes the `increment` calls could be relayed randomly to each machine. In this way when a `numLastDay()` call was made they could each find their own value for this and then those values could be summed. This distributed structure would also be helpful if we wanted to record more than 5 thousand events per second.

## Thanks 👋
Thank you for taking the time and looking through my work. I am eager to hear back.
-- Alec Harmon Blumenfeld
tel: 610-585-3444
email: alec.blumenfeld@mail.mcgill.ca
