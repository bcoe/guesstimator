from time import time
from random import random
from redis import Redis

class Guesstimator(object):
    
    SAMPY_PREFIX = 'guesstimator'
    SAMPLE_SET_LIST_SUFFIX = 'sample_sets'
    SAMPLE_SET_CACHE = {}

    def __init__(self, redis_host='localhost', environment='production', random=random, time=time):
        self.writes_performed = 0
        self.redis = Redis(redis_host)
        self.environment = environment
        self.random = random
        self.time = time
        
    def create_sample_set(self, name=None, recording_frequency=0.05):
        self.redis.lpush(self._sample_set_list_key, name)
        self.redis.hset(self._get_hash_key(name), 'recording_frequency', recording_frequency)
        self.redis.hset(self._get_hash_key(name), 'sample_start_time', self.time())
        self.redis.hset(self._get_hash_key(name), 'samples_taken', 0)
    
    def list_sample_sets(self):
        return self.redis.lrange(self._sample_set_list_key, 0, 9999)
        
    def record(self, sample_set_name):
        
        # Lookup the recording frequency in the cache.
        key = self._get_hash_key(sample_set_name)
        if not Guesstimator.SAMPLE_SET_CACHE.get(key, None):
            sample_set = self.redis.hgetall(key)
            
            # Create a sample set if it doesn't exist.
            if not sample_set:
                self.create_sample_set(sample_set_name)
                sample_set = self.redis.hgetall(key)
            
            # Populate the cache.
            Guesstimator.SAMPLE_SET_CACHE[key] = sample_set
        
        recording_frequency = float( Guesstimator.SAMPLE_SET_CACHE[key]['recording_frequency'] )
        
        if self.random() <= recording_frequency:
            self.writes_performed += 1
            self.redis.hincrby(self._get_hash_key(sample_set_name), 'samples_taken', 1)
    
    def read(self, sample_set_name):
        sample_set_dict = self.redis.hgetall(self._get_hash_key(sample_set_name))
        estimated_samples_taken = float(sample_set_dict['samples_taken']) / float(sample_set_dict['recording_frequency'])
        return ( float(sample_set_dict['sample_start_time']), int(estimated_samples_taken + 0.5) )
    
    def reset(self, sample_set_name):
        self.redis.hset(self._get_hash_key(sample_set_name), 'sample_start_time', self.time())
        self.redis.hset(self._get_hash_key(sample_set_name), 'samples_taken', 0)
    
    @property
    def _sample_set_list_key(self):
        return '%s_%s_%s' % (self.SAMPY_PREFIX, self.environment, self.SAMPLE_SET_LIST_SUFFIX)
        
    def _get_hash_key(self, sample_set_name):
        return '%s_%s_%s' % (self.SAMPY_PREFIX, self.environment, sample_set_name)