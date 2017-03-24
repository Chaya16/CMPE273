import bisect
import md5

class ConsistentHashRing(object):
    """Implement a consistent hashing ring."""

    def __init__(self, replicas=1):
        """Create a new ConsistentHashRing.

        :param replicas: number of replicas.

        """
        self.replicas = replicas
        self._keys = []
        self._nodes = {}

    def _hash(self, key):
        """Given a string key, return a hash value."""

        return long(md5.md5(key).hexdigest(), 16)

    def _repl_iterator(self, nodename):
        """Given a node name, return an iterable of replica hashes."""

        return (self._hash("%s:%s" % (nodename, i))
                for i in xrange(self.replicas))
    
    def __setitem__(self, nodename, node):
        hash_ = self._hash(str(nodename))
        if str(hash_) in self._nodes:
            raise ValueError("Node name %r is already present" % nodename)
        else:
            self._nodes[hash_] = node
            bisect.insort(self._keys, hash_)

    def __delitem__(self, nodename):
       hash_=self._hash(str(nodename))
       if str(hash_) in self._nodes:
            del self._nodes[hash_]
            index = bisect.bisect_left(self._keys, hash_)
            del self._keys[index]
       else:
            raise ValueError("Node name %r is "
                            "not present" % nodename)
    
    def __getitem__(self, key):
        hash_ = self._hash(key)
        start = bisect.bisect(self._keys, hash_)
        if start == len(self._keys):
            start = 0
        return self._nodes[self._keys[start]]
