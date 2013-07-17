TODO
====

These are just random ideas for features (in no particular order).

tests
    Aim for 100% coverage; Tests currently require a running instance of ES;
    Start using Mock, instead?

``dict`` methods
    support sane operations for all of the expected ``dict`` methods (not
    everything works as expected):

    * get -- should use the custom __getitem__
    * items -- should load keys/values from ES
    * keys -- should load keys from ES
    * values -- should load values from ES
    * update
    * iteritems
    * iterkeys
    * itervalues
