"""
This example demonstrates using sampy to estimate the number of times an operation is executed.

sampy.record() is called 20 times more frequently than a write to Redis actually occurs (this is the default configuration).
"""
from sampy import Sampy

sampy = Sampy(environment='example')

# Initialize a sample set, this should only be done once.
sampy.create_sample_set(
    name='example-sample-set'
)

operations = 0
while True:
    operations += 1
    
    # Record that an operation has occurred.
    sampy.record('example-sample-set')
    
    if (operations % 10000) == 0:
        
        # Read the timestamp since metrics started being tracked.
        # and the estimated number of samples taken.
        timestamp, samples_taken = sampy.read('example-sample-set')
        
        print "Metrics:\n\toperation count: \t\033[32m%s\033[m\n\testimated count:\t\033[31m%s\033[m\n\n\tredis writes:\t\t%s\n---------" % (
            operations,
            samples_taken,
            sampy.writes_performed
        )