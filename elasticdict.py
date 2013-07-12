import json
import requests


class ElasticDict(dict):
    """A dictionary that automatically dumps it's keys/values in Elastic
    Search. Everything is converted to JSON behind the scenes, then sent over
    the wire into ES.

    """

    def _uri(self, key=''):
        """A helper method to generate the REST API uris for elasticsearch."""
        data = {
            "host": self.es_host,
            "port": self.es_port,
            "index": self.es_index,
            "type": self.es_type,
            "id": key
        }
        return "http://{host}:{port}/{index}/{type}/{id}".format(**data)

    def __init__(self, es_host='localhost', es_port=9200,
                 es_index='elasticdict', es_type='data'):

        self.es_host = es_host
        self.es_port = es_port
        self.es_index = es_index
        self.es_type = es_type

        # Create an ES index. ES returns a 400 if the index already exists.
        index_data = {
            "host": self.es_host,
            "port": self.es_port,
            "index": self.es_index
        }
        requests.put("http://{host}:{port}/{index}".format(**index_data))

    def _get_key_from_elasticsearch(self, key):
        """Get the data associated with the given key from elasticsearch.
        The ES REST objects are available from ``/index/type/id/``.

        Sending a GET request returns JSON that looks like the following,
        where ``_source`` is the value associated with the given key.

        ::

            {
               "_index" : "es_index",
               "_type" : "es_type",
               "_id" : "es_id",
               "_version" : 1,
               "exists" : true,
               "_source":   ...    # thing we want!
            }

        """
        response = requests.get(self._uri(key))
        if response.status_code == 200:
            data = json.loads(response.content)
            return data["_source"]

    def __setitem__(self, key, value):
        super(ElasticDict, self).__setitem__(key, value)

        # Build a dict, convert to JSON, store on ES
        json_data = json.dumps({key: value})

        # Send the JSON representation to ES
        uri = self._uri(key)
        requests.post(uri, data=json_data)

    def __getitem__(self, key):
        try:
            # If the dictionary already contains the key, no need to hit ES
            return super(ElasticDict, self).__getitem__(key)
        except KeyError:
            # See if the key's data is in ES
            data = self._get_key_from_elasticsearch(key)
            if data and key in data:
                self[key] = data[key]  # update locally
                return self[key]
            else:
                raise KeyError
