#!/usr/bin/env python
import collections
import csv
import os
import sys
import json

from mininet.topo import Topo


# adds the current dir i.e. src to system path
sys.path.append(os.path.dirname(__file__))
from joinHelpers import err
from joinHelpers import config


# xcui's test csv
CSV_BASE = config['CSV_BASE']
# CSV_BASE = 'csv/'

class Entity(object):
    foreign_keys = {}

    def __init__(self, store):
        self.store = store

    """
    Read the CSV file and dump the data in the store
    """
    def read(self):
        print >> sys.stderr, 'Loading %s...' % self.csv_name
        with open(CSV_BASE + '/%s.csv' % self.csv_name) as csv_file:
            # Parse the header row
            reader = csv.reader(csv_file, delimiter=',', quotechar='\'',
                                doublequote=False, escapechar='\\')
            header = next(reader, None)
            self.__class__.field_names = header

            for row in reader:
                id = str(row[0])
                id = self.csv_name + ':' + id
                rowVal = dict()
                for index, value in enumerate(row[1:]):
                    field = header[index + 1]
                    # Append the ID if we have a many-to-many relation or
                    # set the value directly otherwise
                    related = self.__class__.foreign_keys.get(field, None)
                    if related:
                        if field not in row:
                            rowVal[field] = []
                        rowVal[field].append(value)
                    else:
                        rowVal[field] = value
                self.store.set(id, rowVal)
            # print(json.dumps(self.store.data))
        print >> sys.stderr, 'Loading Completed for %s...' % self.csv_name

class User(Entity):
    csv_name = 'users'

class Item(Entity):
    csv_name = 'items'
    foreign_keys = {'seller': User}

class Store(object):
    """
    num is the total number of available bucket.
    sId is the server id, i.e. a server with ip 10.0.0.8 will have id of 7,
    since server 0 will have ip address 10.0.0.1.
    if sId is None, we store all the data in the current server.
    rFactor is the replication factor,
    each server will store data in bucket sId, (sId + 1) % num ... (sId + rFactor - 1) % num
    """
    def __init__(self, num, sId = None, rFactor = 1):
        self.sId = sId
        self.data = []
        for i in range(num):
            self.data.append({})
        if sId is not None:
            self.shard = [_ % num for _  in range(sId, sId + rFactor)]

    """
    Get the bucket associated with a given key
    """
    def bucket(self, key):
        return hash(key) % len(self.data)

    """
    Return the sIds for which have this key
    """
    def getServerIds(self, key):
        # We do not have replication at this stage, so we just return the hash
        return [self.bucket(key)]

    """
    Set the value for the given key
    """
    def set(self, key, value):
        curBucket = self.bucket(key)
        if self.sId is not None:
            if curBucket in self.shard:
                self.data[curBucket][key] = value
            else:
                # not part this store's bucket
                pass
        else:
            self.data[curBucket][key] = value

    """
    Add the value to the list in the given key
    """
    def append(self, key, value):
        curBucket = self.bucket(key)
        if self.sId is not None:
            if curBucket in self.shard:
                self.data[curBucket][key].append(value)
        else:
            self.data[curBucket][key].append(value)

    """
    Get the value for the given key
    """
    def get(self, key):
        bucket = self.bucket(key)
        # return (bucket, self.data[bucket])
        return self.data[bucket][key]

    """
    Return the number of keys stored in each bucket
    """
    def stats(self):
        return [len(bucket.keys()) for bucket in self.data]

"""
In the current implementation, Query only works when we join all
of the sharded tables together
"""
class Query(object):
    def __init__(self, entity, store, IDs):
        self.entity = entity
        self.store = store

    """
    Execute a query to fetch the entity with the given ID and all its
    fields and related entities
    """
    def execute(self, ids):
        for field in self.entity.field_names:
            if field in self.entity.foreign_keys:
                key = '%s:%s:%s' % (self.entity.__name__, field, id)
                keys = self.store.get(key)
                [Query(self.entity.foreign_keys[field], self.store) \
                        .execute(foreign_id) for foreign_id in keys[1]]
            else:
                key = '%s:%s:%s' % (self.entity.__name__, field, id)
                # print(key, store.get(key))

if __name__ == '__main__':
    # Read a couple entities, run some queries with known IDs
    # and print the distribution of data between buckets
    n = config['NUM_HOST']
    # topo = StarTopo(n)
    store0 = Store(n, 3, 1)
    users = User(store0).read()
    items = Item(store0).read()
    # print(store0.get('items:533721')[1]['seller'])
    print store0.stats()
