from google.cloud import datastore
import datetime


datastore_client = datastore.Client()
kind = 'Reviews'


def new_reviews(name, review):
    entity = datastore.Entity(key=datastore_client.key(kind))
    entity['name'] = name
    entity['review'] = review
    entity['time'] = datetime.datetime.now()
    datastore_client.put(entity)


def query():
    query = datastore_client.query(kind=kind)
    query.order = ['-time']
    return list(query.fetch())