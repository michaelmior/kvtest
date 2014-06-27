import collections
import csv
import os
import sys

# Add mininet to the path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                'mininet'))

from mininet.topo import Topo

class StarTopo(Topo):
    def __init__(self, count):
        self.count = count
        Topo.__init__(self)

        hosts = ['h%d' % i for i in range(count)]
        switch = self.addSwitch('s')
        for host in hosts:
            self.addHost(host)
            self.addLink(host, switch)

class Entity(object):
    foreign_keys = {}

    def __init__(self, store):
        self.store = store

    """
    Read the CSV file and dump the data in the store
    """
    def read(self):
        print >> sys.stderr, 'Loading %s...' % self.csv_name
        with open('csv/%s.csv' % self.csv_name) as csv_file:
            # Parse the header row
            reader = csv.reader(csv_file, delimiter=',', quotechar='\'',
                                doublequote=False, escapechar='\\')
            header = next(reader, None)
            self.__class__.field_names = header

            for row in reader:
                id = row[0]
                for index, value in enumerate(row[1:]):
                    field = header[index + 1]

                    # Append the ID if we have a many-to-many relation or
                    # set the value directly otherwise
                    related = self.__class__.foreign_keys.get(field, None)
                    if related:
                        self.store.append('%s:%s:%s' %
                                (self.__class__.__name__, field, id), value)
                    else:
                        self.store.set('%s:%s:%s' %
                                (self.__class__.__name__, field, id), value)

class User(Entity):
    csv_name = 'users'

class Item(Entity):
    csv_name = 'items'
    foreign_keys = {'seller': User}

class Store(object):
    def __init__(self, num):
        self.data = [collections.defaultdict(lambda: []) for _ in range(num)]

    """
    Get the bucket associated with a given key
    """
    def bucket(self, key):
        return hash(key) % len(self.data)
    """
    Set the value for the given key
    """

    def set(self, key, value):
        self.data[self.bucket(key)][key] = value

    """
    Add the value to the list in the given key
    """
    def append(self, key, value):
        self.data[self.bucket(key)][key].append(value)

    """
    Get the value for the given key
    """
    def get(self, key):
        bucket = self.bucket(key)
        return (bucket, self.data[bucket].get(key))

    """
    Return the number of keys stored in each bucket
    """
    def stats(self):
        return [len(bucket.keys()) for bucket in self.data]

class Query(object):
    def __init__(self, entity, store):
        self.entity = entity
        self.store = store

    """
    Execute a query to fetch the entity with the given ID and all its
    fields and related entities
    """
    def execute(self, id):
        for field in self.entity.field_names:
            if field in self.entity.foreign_keys:
                key = '%s:%s:%s' % (self.entity.__name__, field, id)
                keys = self.store.get(key)
                [Query(self.entity.foreign_keys[field], self.store) \
                        .execute(foreign_id) for foreign_id in keys[1]]
            else:
                key = '%s:%s:%s' % (self.entity.__name__, field, id)

if __name__ == '__main__':
    # Read a couple entities, run some queries with known IDs
    # and print the distribution of data between buckets
    n = 4
    topo = StarTopo(n)
    store = Store(topo.count)
    users = User(store).read()
    items = Item(store).read()

    for id in range(500001, 500001 + 100 + 1):
        Query(Item, store).execute(str(id))

    print store.stats()
