About
-----
ElasticDict provides a python ``dict``-like object that transparently
stores it's keys and values in ElasticSearch.

*Warning!* This is a Work in Progress. At the moment, this is just an
experiment. You probably don't want to use this for anything even remotely
serious. If you need a real library for ElasticSearch, check out one of these:

* `pyelasticsearch <https://github.com/rhec/pyelasticsearch>`_
* `pyes <https://github.com/aparo/pyes>`_

Usage
-----
To get started, `download elasticsearch <http://www.elasticsearch.org/download/>`_,
extract it, and run it locally::

    $./bin/elasticsearch -f

Then, fire up a python shell, and create an instance of ``ElasticDict``, and
treat it like a regular python dictionary::

    >>> d = ElasticDict()
    >>> d['foo'] = 'bar'
    >>> d['foo']
    bar
    >>> d.keys()
    ['foo']
    >>> d.values()
    ['bar']
    >>> d.items()
    [('foo', 'bar')]

Remove this object, and start all over::

    >>> del d
    >>> d = ElasticDict()
    >>> d['foo']
    bar

Hey! Our ``bar`` value is still there!

This assumes elasticsearch is running on localhost using the default ports.
You could also query elasticsearch locally::

    $ curl -XGET 'http://localhost:9200/elasticdict/data/foo?pretty=true'
    {
      "_index" : "tst",
      "_type" : "foo",
      "_id" : "1",
      "_version" : 1,
      "exists" : true, "_source" : {"foo":"bar"}
    }


Tests
-----
There are a few tests for this, though they are woefully incomplete. To run
them, use::

    $ nosetests


Requirements
------------

* Python 2.6+
* `requests <http://python-requests.org>`_
* `nose <http://pypi.python.org/pypi/nose/>`_


What Next?
---------

Look at the source; There's obviously not much here at the moment. Right now
the `ElasticDict` class just persists data to Elasticsearch, but there's a lot
more that could be done:

* support for all of the `dict` methods (not everything works as expected)
* Search! Elasticsearch is for... search. How should that fit into a
  dictionary?

Other ideas? Reach out on twitter (`@bkmontgomery <http://twitter.com/bkmontgomery>`_)
or email me.


License
-------

This work is available under the terms of the MIT license. See the ``LICENSE``
file for details.
