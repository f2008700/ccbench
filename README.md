ccbench
=======

ccbench is a tool for measuring the cache-coherence latencies of a processor, i.e., the latencies of `loads`, `stores`, `compare-and-swap (CAS)`, `fetch-and-increment (FAI)`, `test-and-set (TAS)`, and `swap (SWAP)`. The latencies that ccbench measures can be used to understand and predict the behavior of sharing and synchronization on the underlying hardware platform.

* Website             : http://lpd.epfl.ch/site/ccbench
* Author              : Vasileios Trigonakis <vasileios.trigonakis@epfl.ch>
* Related Publications: ccbench is a part of the SSYNC synchronization suite
  (http://lpd.epfl.ch/site/ssync):  
  Everything You Always Wanted to Know about Synchronization but Were Afraid to Ask,   
  Tudor David, Rachid Guerraoui, Vasileios Trigonakis (alphabetical order),   
  SOSP '13 - Proceeding of the 24th ACM Symposium on Operating Systems Principles


Installation:
-------------

Please refer to the `INSTALL` file.


Using ccbench:
--------------

Execute:
	`./ccbench -h`
to get the parameters and the supported events of ccbench


Details:
--------
ccbench brings a single cache line L in the desired MESI state and position in the processor and then 
performs that target operation on L. In more details, ccbench takes the following steps:
	 1 It uses one (or more) cores to bring L in the desired state and position, 
	    e.g., in a Modified state in the local caches of core 0 in node 0.
	 2 It then uses another core in order to perform the target operation, e.g., load from a
	    modified state that is on the local caches of a core that is on the same node.



Limitations:
------------

Measuring latencies at this low level is not easy. Most of the events work as intended on all platforms.
However, there are some subtle details that one should be aware of in order to "successfully" use
ccbench:
* The memory fences to be used are related to the memory consistency model of the underlying platform. For instance, on an `AMD Opteron Magny-Cours` we can measure both `loads` and `stores` without using any fences (`ccbench -e0`). Contrarily, on an `Intel Xeon Westmere-EX`, we can measure the loads with a `load fence`, but a store needs a full fence (so, `ccbench -e8`).
* The stride parameter is used to try to fool the hardware prefetchers. This is also a hardware dependent parameter.
* There are certain cases where you might need to compile ccbench with `-O0` flag instead of the default `-O3` to be able to get the results. Known cases:
  * on the Tile-GX36, you probably need to compile with `-O0` to get sensible number for the atomic ops
  * on UltraSPARC T2, you probably need to compile with `-O0` for all operations 
	      	except the atomic ops


Interpreting the results:
-------------------------

The comments prefixed with "#>>" explain the results.

<pre>
#>> settings:
test: LOAD_FROM_MODIFIED / #cores: 2 / #reps: 1000 / stride: 4096 / fence: load/full
core1:   1 / core2:   2

#>> warnings regarding the profiler correction. If the calculation fails for 10 times 
#>> (i.e, the correction calculation does not have a low std deviation, the correction 
#>> is manually set to a given (in src/pfd.c) platform-specific value. If the default 
#>> value is not set, the avg corrections are still used. 
#>> (This approach works OK in my experience.)

* warning: avg pfd correction is 20.2 with std deviation: 16.3%. Recalculating.
* warning: setting pfd correction manually
 -- pfd correction: 20 (std deviation: 22.2%)
* warning: avg pfd correction is 20.3 with std deviation: 17.0%. Recalculating.
* warning: setting pfd correction manually
 -- pfd correction: 20 (std deviation: 22.2%)

#>> results

[00]  *** Core  0 ***************************************************************

 ---- statistics:

#>> global avg and deviations

[00]  avg : 111.5      abs dev : 2.5        std dev : 4.5        num     : 1000
[00]  min : 32.0       (element:    779)    max     : 136.0      (element:    415)

#>> clustering of values around the global avg. This approach is used as an easy way 
#>> of remove outlier measurements. The columns represent:
#>> % group / num of samples / % of the total num of samples / avg of the cluster /
#>> absolute deviation of the cluster / standard deviation of the cluster

[00]   0-10% : 987 ( 98.7% | avg: 111.5 | abs dev:  2.3 | std dev:  3.0 =   2.7%)
[00]  10-25% : 11  (  1.1% | avg: 126.2 | abs dev:  3.5 | std dev:  4.2 =   3.3%)
[00]  25-50% : 1   (  0.1% | avg:  65.0 | abs dev:  0.0 | std dev:  0.0 =   0.0%)
[00]  50-75% : 1   (  0.1% | avg:  32.0 | abs dev:  0.0 | std dev:  0.0 =   0.0%)
[00] 75-100% : 0   (  0.0% | avg:  -nan | abs dev: -nan | std dev: -nan =  -nan%)

[01]  *** Core  1 ***************************************************************

 ---- statistics:
[01]     avg : 112.3 abs dev : 2.5        std dev : 5.4        num     : 1000
[01]     min : 10.0  (element:    902)    max     : 133.0      (element:    404)
[01]   0-10% : 989 ( 98.9% | avg: 112.4 | abs dev:  2.2 | std dev:  2.9 =   2.6%)
[01]  10-25% : 9   (  0.9% | avg: 126.0 | abs dev:  1.8 | std dev:  2.7 =   2.1%)
[01]  25-50% : 0   (  0.0% | avg:  -nan | abs dev: -nan | std dev: -nan =  -nan%)
[01]  50-75% : 0   (  0.0% | avg:  -nan | abs dev: -nan | std dev: -nan =  -nan%)
[01] 75-100% : 2   (  0.2% | avg:  13.5 | abs dev:  3.5 | std dev:  3.5 =  25.9%)

#>> The meaning of the results

[00] Results Core 0 : store to owned mine (if owned state supported, else exclusive)
[00] Results Core 1 : load from modified (makes it owned, if owned state supported)

#>> The final val in the cache line that was used / the sum of all loads on this core
#>> These values can be used for ensuring the correctness of some test (e.g., FAI)

[00]  value of cl is 0    / sum is 0
[01]  value of cl is 0    / sum is 0
</pre>
