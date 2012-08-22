Sampy
=====

Estimates the performance of a distributed system based on a sample set of data.

* Redis backed.
* It's meant to be simple; pretty much all you get is an increment operation.

Creating a Sample Set
---------------------

This should only be done once, for each performance metric that will be tracked.

```python
sampy = Sampy()

sampy.create_sample_set(
    name='sample_set_name',
	recording_frequency=0.5
)
```

* **name** the name of the sample set.
* **recording\_frequency** how frequently should we actually write the metric to Redis? 0.5 indicates that we will record the metric 50% of the time. 5% is the default.

Recording Performance Data
---------------------------

Once you have created a sample set, workers in the distributed begin recording performance data to it.

Writes will be performed to Redis with the probability set when creating the sample set.

```python
sampy = Sampy()
sampy.record('sample_set_name')
```

Reading Performance Data
------------------------

While there are multiple workers, there should be a single reader of performance data. A good use-case might be a Ganglia plugin.

**Getting the timestamp and operation count**

```python
sampy = Sampy()
timestamp, operation_count = sampy.read('sample_set_name')
```

* **timestamp** is the unix time since sampy started tracking performance information.
* **operation\_count** the estimated number of operations that have occurred since **timestamp**.

**Reseting timestamp and operation count**

```python
sampy = Sampy()
sampy.reset('sample_set_name')
```

This sets **timestamp** to the current time, and **operation\_count** back to zero.