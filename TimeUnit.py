from OrderedDefaultDict import OrderedDefaultDict
class AbstractTimeUnit(object):
    """Abstract Class For Time Units"""
    def __init__(self, parrent=None):
        super(AbstractTimeUnit, self).__init__()
        self.parrent = parrent
        self.count = 0
        self.index = None


    def increnment(self, key=None):
        """Increments itself and Parrent, if there is a key increment that value"""
        self.count += 1
        if key: self.index[key] += 1
        if self.parrent: self.parrent.increnment()

    def sumIndex(self, comp):
        """Sum index values if their respective keys pass a given comp"""
        summation = 0
        for key, value in self.index.iteritems():
            if comp(key):
                temp = value + summation
                summation = temp
        return summation

    def sumIndexGTET(self, x):
        """Sum the all index values Greater Than or Equal To x"""
        return self.sumIndex(lambda y: x <= y)

    def sumIndexLTET(self, x):
        """Sum the all index values Less Than or Equal To x"""
        return self.sumIndex(lambda y: x <= y)

    def __getitem__(self, key):
        """Allows access values of each subunit as unit[subunit]"""
        return self.index[key]

    def __add__(self, other):
        """Overides addition for more generaic procedures like in sumIndex()"""
        if isinstance(other, int):
            return self.count + other
        else:
            return self.count + other.count


class Minute(AbstractTimeUnit):
    """
       Parrent of Seconds:
       second_count = Minute[Second]
    """
    def __init__(self, parrent):
        AbstractTimeUnit.__init__(self, parrent)
        self.index = OrderedDefaultDict(int)


class Hour(AbstractTimeUnit):
    """
       Parrent of Minutes:
       second_count = Hour[Minute][Second]
    """
    def __init__(self):
        AbstractTimeUnit.__init__(self)
        self.index = OrderedDefaultDict(lambda: Minute(self))
