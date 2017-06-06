from collections import OrderedDict, defaultdict

# Combination of OrderedDict and defaultdict
class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default
