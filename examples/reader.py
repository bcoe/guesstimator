"""
This example demonstrates what a reader that consumes sampy's data might look like.

in the wild this might be a Ganglia or Munin plugin.
"""
import time
from sampy import Sampy
from redis import Redis

sampy = Sampy(environment='example')
sample_set_name = 'count-operations'
redis = Redis('localhost')

# Initialize a sample set, this should only be done once.
if not sample_set_name in sampy.list_sample_sets():
    sampy.create_sample_set(
        name=sample_set_name
    )

while True:
    time.sleep(10)
    operations = float( redis.get('sampy_example_actual_operation_count') )
    timestamp, estimated_operations = sampy.read(sample_set_name)
    print "Metrics:\n\toperation count: \t\033[32m%s\033[m\n\testimated count:\t\033[31m%s\033[m\n\n\tOperations per-second:\t%s\n---------" % (
        operations,
        estimated_operations,
        ( operations / (time.time() - timestamp) )
    )
    
    sampy.reset(sample_set_name)
    redis.set('sampy_example_actual_operation_count', 0)    