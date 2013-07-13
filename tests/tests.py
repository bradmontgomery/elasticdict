"""

Run the tests with::

    nosetests --with-coverage

"""
from mock import Mock, patch
from nose.tools import assert_raises, eq_

from elasticdict import ElasticDict


class TestElasticDict:
    """Tests for the ``ElasticDict`` methods."""

    def setup(self):
        """Patch ``requests`` so we don't send real HTTP requests."""
        self.requests_patcher = patch("elasticdict.requests")
        self.mock_requests = self.requests_patcher.start()

    def teardown(self):
        self.mock_requests.reset_mock()
        self.requests_patcher.stop()

    def test__init__default(self):
        # With default parameters
        d = ElasticDict()
        eq_(d.es_host, "localhost")
        eq_(d.es_port, 9200)
        eq_(d.es_index, "elasticdict")
        eq_(d.es_type, "data")

        index_uri = "http://localhost:9200/elasticdict"
        self.mock_requests.put.assert_called_once_with(index_uri)

    def test__init__custom(self):
        # with custom parameters
        d = ElasticDict(
            es_host="example.com",
            es_port=4242,
            es_index="foo",
            es_type="thingies"
        )
        eq_(d.es_host, "example.com")
        eq_(d.es_port, 4242)
        eq_(d.es_index, "foo")
        eq_(d.es_type, "thingies")

        index_uri = "http://example.com:4242/foo"
        self.mock_requests.put.assert_called_once_with(index_uri)

    def test__uri(self):
        d = ElasticDict()
        result = d._uri("some_key")
        eq_(result, "http://localhost:9200/elasticdict/data/some_key")

    def test__get_key_from_elasticsearch(self):
        # Create a Mock response object
        config = {
            'status_code': 200,
            'content': """{
                "_index" : "es_index",
                "_type" : "es_type",
                "_id" : "es_id",
                "_version" : 1,
                "exists" : true,
                "_source": "RESULT"}""",
        }
        mock_response = Mock(**config)
        self.mock_requests.get.return_value = mock_response

        d = ElasticDict()
        result = d._get_key_from_elasticsearch("KEY")
        eq_(result, "RESULT")

        uri = "http://localhost:9200/elasticdict/data/KEY"
        self.mock_requests.get.assert_called_once_with(uri)

    def test__setitem__(self):
        d = ElasticDict()
        d['foo'] = 'bar'  # Set an item

        # super calls __setitem__(key, value); so we get keys/values just like
        # a regular dictionary
        eq_(d.values(), ['bar'])
        eq_(d.keys(), ['foo'])

        # Then the key/value is json-ified and posted to ElasticSearch
        self.mock_requests.post.assert_called_once_with(
            "http://localhost:9200/elasticdict/data/foo",
            data='{"foo": "bar"}'
        )

    def test__getitem__existing_values(self):
        """Tests ``__getitem__`` when there are existing values in the dict."""
        d = ElasticDict()
        d['foo'] = 'bar'

        result = d['foo']  # calls super class's __getitem__(key)
        eq_(result, 'bar')

    def test__getitem__es_values(self):
        """Tests ``__getitem__`` when there are no existing values in the dict,
        but there *are* matching values in ElasticSearch"""
        d = ElasticDict()
        d._get_key_from_elasticsearch = Mock(return_value={'foo': 'bar'})

        # verify that there are not items in the dict
        eq_(d.items(), [])

        # fetch an item
        result = d['foo']
        eq_(result, 'bar')  # value retrieved from ES
        eq_(d.items(), [('foo', 'bar')])  # and inserted into the dict

    def test__getitem__no_values(self):
        """Tests ``__getitem__`` when there are no existing values in the dict,
        and when there are no matching values in ElasticSearch"""
        d = ElasticDict()
        d._get_key_from_elasticsearch = Mock(return_value=None)

        # verify that there are not items in the dict
        eq_(d.items(), [])

        # fetch an item
        with assert_raises(KeyError):
            d['foo']

    def test__delitem__(self):
        # Create a Mock response object
        config = {
            'status_code': 200,
            'json.return_value': {
                u'_id': u'foo',
                u'_index': u'elasticdict',
                u'_type': u'data',
                u'_version': 1,
                u'found': True,
                u'ok': True
            }
        }
        mock_response = Mock(**config)
        self.mock_requests.delete.return_value = mock_response

        d = ElasticDict()
        d['foo'] = 'bar'  # make sure it's actually in the dictionary
        del d['foo']
        # It's deleted from ElasticSearch
        self.mock_requests.delete.assert_called_once_with(
            "http://localhost:9200/elasticdict/data/foo"
        )
        # It's removed from the dictionary
        eq_(d.items(), [])

    def test__delitem__fails(self):
        """Deleting a Non-existing item should raise a KeyError."""
        # Create a Mock response object
        config = {
            'status_code': 404,
            'json.return_value': {
                u'_id': u'nothing',
                u'_index': u'elasticdict',
                u'_type': u'data',
                u'_version': 1,
                u'found': False,
                u'ok': True
            }
        }
        mock_response = Mock(**config)
        self.mock_requests.delete.return_value = mock_response

        d = ElasticDict()
        with assert_raises(KeyError):
            del d['nothing']
            self.mock_requests.delete.assert_called_once_with(
                "http://localhost:9200/elasticdict/data/nothing"
            )


#def simple_test():
#    e = ElasticDict()
#    e['foo'] = 'bar'
#    eq_(e['foo'], 'bar')
#    eq_(e.keys(), ['foo'])
#    eq_(e.values(), ['bar'])
#    eq_(e.items(), [('foo', 'bar')])
#
#def complex_test():
#    e = ElasticDict()
#    e['names'] = ['Django Fett', 'Bobba Fett', 'Lando Calrissian']
#    eq_(e['names'], ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])
#    eq_(e.keys(), ['names'])
#    eq_(e.values(), [['Django Fett', 'Bobba Fett', 'Lando Calrissian']])
#    eq_(e.items(),
#       [('names', ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])])
#
#    del e # delete the dict and requery the results
#
#    d = ElasticDict()
#    eq_(d['names'], ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])
#    eq_(d.keys(), ['names'])
#    eq_(d.values(), [['Django Fett', 'Bobba Fett', 'Lando Calrissian']])
#    eq_(d.items(),
#       [('names', ['Django Fett', 'Bobba Fett', 'Lando Calrissian'])])
