"""
This exmaple demonstrates how guesstimator might be used by a worker in a distributed system.

guesstimator.record() is called 20 times more frequently than a write to Redis actually occurs (this is the default configuration).
"""
from guesstimator import Guesstimator
from redis import Redis

guesstimator = Guesstimator(environment='example')
sample_set_name = 'count-operations'
redis = Redis('localhost')
last_operations_count = 0

# Initialize a sample set, this should only be done once.
if not sample_set_name in guesstimator.list_sample_sets():
    guesstimator.create_sample_set(
        name=sample_set_name
    )

while True:

    # Record that an operation has occurred.
    guesstimator.record(sample_set_name)
    
    # our operation happens to be an increment in Redis, it could be anything.
    # this is a convenient operation because it lets us keep track of the
    # true number of total operations across multiple workers.
    operations = redis.incr('guesstimator_example_actual_operation_count')
    
    # reader.py must have reset the operation count.
    if last_operations_count > operations:
        guesstimator.writes_performed = 0
        last_operations_count = operations
    
    if (operations % 10000) == 0:
        
        # Read the timestamp since metrics started being tracked.
        # and the estimated number of samples taken.
        timestamp, estimated_operations = guesstimator.read(sample_set_name)
        
        # Using the operation count and the frequency that we record metrics we can guestimate how
        # many workers are currently in the system.
        estimated_worker_count = int( (float(operations) / (float(guesstimator.writes_performed) / 0.05)) + 0.5 )
        
        print "Metrics:\n\toperation count: \t\033[32m%s\033[m\n\testimated count:\t\033[31m%s\033[m\n\n\tredis writes performed:\t\t%s\n\testimated worker count: \t%s\n---------" % (
            operations,
            estimated_operations,
            guesstimator.writes_performed,
            estimated_worker_count
        )
        last_operations_count = operations