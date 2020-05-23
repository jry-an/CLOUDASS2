from google.cloud import datastore
import datetime


datastore_client = datastore.Client()
kind = 'News'


def new_news(title, content):
    entity = datastore.Entity(key=datastore_client.key(kind))
    entity['title'] = title
    entity['content'] = content
    entity['time'] = datetime.datetime.now()
    datastore_client.put(entity)


def query():
    query = datastore_client.query(kind=kind)
    query.order = ['-time']
    return list(query.fetch())