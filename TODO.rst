TODO
====

These are just random ideas for features (in no particular order).

tests
    Aim for 100% coverage; Tests currently require a running instance of ES;
    Start using Mock, instead?

search
    support the ``key in d`` expression if ``d`` is an ``ElasticDict`` object.
    This would essentially be a search, and if performed, would load ``key``'s
    value into the dictionary.

``dict`` methods
    support sane operations for all of the expected ``dict`` methods (not
    everything works as expected):

    * __delitem__
    * __contains__ --- support for ``key in d`` expressions
    * get
    * items
    * iteritems
    * iterkeys
    * itervalues
    * keys
    * update
    * values
