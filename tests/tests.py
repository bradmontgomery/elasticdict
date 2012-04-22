"""
NOTE: To run these tests, you need an instance of
elasticsearch running locally. Download and extract
it `here <http://www.elasticsearch.org/download/>`_

Then ``cd`` into the created directory and run::

    ./bin/elasticsearch -f

Run the tests with::
    
    nosetests tests

"""

from nose.tools import eq_
from elasticdict import ElasticDict

def simple_test():
    e = ElasticDict()
    e['foo'] = 'bar'
    eq_(e['foo'], 'bar')
    eq_(e.keys(), ['foo'])
    eq_(e.values(), ['bar'])
    eq_(e.items(), [('foo', 'bar')])

def complex_test():
    e = ElasticDict()
    e['names'] = ['Django Fett', 'Bobba Fett', 'Lando Calrissian']
    eq_(e['names'], ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])
    eq_(e.keys(), ['names'])
    eq_(e.values(), [['Django Fett', 'Bobba Fett', 'Lando Calrissian']])
    eq_(e.items(), [('names', ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])])

    del e # delete the dict and requery the results

    d = ElasticDict()
    eq_(d['names'], ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])
    eq_(d.keys(), ['names'])
    eq_(d.values(), [['Django Fett', 'Bobba Fett', 'Lando Calrissian']])
    eq_(d.items(), [('names', ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])])
