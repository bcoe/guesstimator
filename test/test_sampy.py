import random
import unittest
from redis import Redis
from sampy import Sampy

class MockTime(object):
    
    def __init__(self, time=1345571389.86):
        self.time = time
    
    def __call__(self):
        return self.time
        
class MockRandom(object):
    
    def __init__(self):
        random.seed(1)
    
    def __call__(self):
        return random.random()

class TestSampy(unittest.TestCase):
    
    def setUp(self):
        self.redis = Redis('localhost')
        self._delete_sampy_data()
    
    def _delete_sampy_data(self):
        sampy = Sampy(redis_host='localhost', environment='test')
        self.redis.delete( sampy._sample_set_list_key )
        for sample_set_name in sampy.list_sample_sets():
            self.redis.delete(sampy._get_hash_key(sample_set_name))
    
    def test_list_sample_set_lists_all_sample_sets_currently_being_written_to(self):
        sampy = Sampy(redis_host='localhost', environment='test')
        self.redis.lpush( sampy._sample_set_list_key, 'user-message-queue' )
        self.redis.lpush( sampy._sample_set_list_key, 'user-background-jobs' )
        self.assertTrue( 'user-background-jobs' in sampy.list_sample_sets() )
        self.assertTrue( 'user-message-queue' in sampy.list_sample_sets() )
        
    def test_create_sample_set_creates_populates_sample_set_list(self):
        sampy = Sampy(redis_host='localhost', environment='test')
        self.assertEqual( self.redis.type( sampy._sample_set_list_key ), 'none')
        sampy.create_sample_set('foobar-sample')
        self.assertTrue( 'foobar-sample' in sampy.list_sample_sets() )
    
    def test_create_sample_set_populates_hash_with_parameters_provided(self):
        mock_time = MockTime()
        sampy = Sampy(redis_host='localhost', time=mock_time, environment='test')
        sampy.create_sample_set(
            name='foobar-sample',
            recording_frequency=0.05
        )
        self.assertEqual( '0.05', self.redis.hget( sampy._get_hash_key('foobar-sample'), 'recording_frequency' ) )
        self.assertEqual( '0', self.redis.hget( sampy._get_hash_key('foobar-sample'), 'samples_taken' ) )
        self.assertEqual( '%s' % mock_time.time, self.redis.hget( sampy._get_hash_key('foobar-sample'), 'sample_start_time' ) )
        
    def test_record_increments_the_number_of_samples_taken_with_the_appropriate_frequency(self):
        sampy = Sampy(redis_host='localhost', random=MockRandom(), environment='test')
        sampy.create_sample_set(
            name='100-percent-sample',
            recording_frequency=1.0
        )
        
        sampy.record('100-percent-sample')
        sampy.record('100-percent-sample')
        self.assertEqual( '2', self.redis.hget( sampy._get_hash_key('100-percent-sample'), 'samples_taken' ) )

        sampy.create_sample_set(
            name='50-percent-sample',
            recording_frequency=0.5
        )        
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        self.assertEqual( '3', self.redis.hget( sampy._get_hash_key('50-percent-sample'), 'samples_taken' ) )

        sampy.create_sample_set(
            name='25-percent-sample',
            recording_frequency=0.25
        )        
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        self.assertEqual( '2', self.redis.hget( sampy._get_hash_key('25-percent-sample'), 'samples_taken' ) )
        
    def test_read_returns_a_timestamp_and_an_estimation_of_the_number_of_samples_taken(self):
        mock_time = MockTime()
        sampy = Sampy(redis_host='localhost', random=MockRandom(), time=mock_time, environment='test')
        sampy.create_sample_set(
            name='50-percent-sample',
            recording_frequency=0.5
        )        
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        sampy.record('50-percent-sample')
        timestamp, samples_taken = sampy.read('50-percent-sample')
        self.assertEqual(4, samples_taken)
        self.assertEqual(mock_time.time, timestamp)

        sampy.create_sample_set(
            name='25-percent-sample',
            recording_frequency=0.25
        )        
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        sampy.record('25-percent-sample')
        timestamp, samples_taken = sampy.read('25-percent-sample')
        self.assertEqual(8, samples_taken)
    
    def test_reset_resets_timestamp_and_samples_taken(self):
        mock_time = MockTime()
        new_time = 1345576088.71
        sampy = Sampy(redis_host='localhost', random=MockRandom(), time=mock_time, environment='test')
        
        sampy.create_sample_set(
            name='100-percent-sample',
            recording_frequency=1.0
        )
        sampy.record('100-percent-sample')
        sampy.record('100-percent-sample')
        
        timestamp, samples_taken = sampy.read('100-percent-sample')
        self.assertEqual( '2', self.redis.hget( sampy._get_hash_key('100-percent-sample'), 'samples_taken' ) )
        self.assertFalse( timestamp == new_time )
        
        mock_time.time = new_time
        sampy.reset('100-percent-sample')
        timestamp, samples_taken = sampy.read('100-percent-sample')
        
        self.assertEqual( '0', self.redis.hget( sampy._get_hash_key('100-percent-sample'), 'samples_taken' ) )
        self.assertEqual( new_time, timestamp )

