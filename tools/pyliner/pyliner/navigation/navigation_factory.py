from abc import abstractmethod

from pyliner.util import Loggable, OverlayDict


NotSet = type('NotSet', (object,), {'__repr__': lambda s: 'NotSet'})()
"""Indicate a kwarg that is not set (different than None). Use responsibly.
You probably shouldn't re-assign this."""


class NavigationFactory(Loggable):
    """Base class for any kind of navigation producer.

    NavigationFactories should follow SRP and do one thing well. Example
    implementations are Lnav and Vnav, which do only lateral and vertical
    motion, respectively. The primary way to access this ability is by calling
    the factory (aka via __call__), which takes a superset of all the parameters
    that the operation uses, and performs an action based on the provided
    arguments.

    Developers are free to add convenience methods which fill in arguments for
    the user. __call__ and all convenience methods should return self to allow
    for chained calls if such an operation makes sense for the factory.
    """
    def __init__(self, navigation, **kwargs):
        """Construct with navigation as the base app and default kwargs."""
        super(NavigationFactory, self).__init__(navigation.vehicle.logger)
        self._nav = navigation
        self._default = OverlayDict(kwargs, self._nav.defaults)

    @abstractmethod
    def __call__(self, **kwargs):
        # type: (object) -> NavigationFactory
        """Perform the requested operation and return self."""
        raise NotImplementedError

    def resolve(self, item, name):
        """If item is NotSet fall back on Navigation defaults."""
        try:
            return item if item is not NotSet else self._default[name]
        except KeyError as e:
            raise KeyError('No default set for unset parameter '
                           '"{}".'.format(name))
