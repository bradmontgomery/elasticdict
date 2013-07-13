TODO
====

These are just random ideas for features (in no particular order).


search
    support the ``key in d`` expression if ``d`` is an ``ElasticDict`` object.
    This would essentially be a search, and if performed, would load ``key``'s
    value into the dictionary.

deleting items
    deleting items from the dictionary should delete from ES;
    e.g. ``del d['foo']``

``dict`` methods
    support sane operations for all of the expected ``dict`` methods (not
    everything works as expected)
