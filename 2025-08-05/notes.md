Summary of Today's Findings
Today, we successfully conducted two key experiments: a baseline run with a single worker and a scaled-up run with 32 workers. The results were illuminating and have given us a clear direction.

Scaling Experiment Reveals a Critical Bottleneck
The most important finding is that scaling from 1 worker to 32 workers only decreased the total runtime from 3m 32s to 3m 13s—a speedup of only ~1.1x for a 32x increase in resources. This is a classic sign that the computations themselves are not the limiting factor.

Contrary to our initial thought, the Gantt chart from the 32-worker run provides clear evidence that the workflow is Thinker-bound, not simulation-bound.

Screenshot here

As seen in the chart above, the 32 worker lanes (the y-axis) are mostly empty (white space) for the duration of the run. We can see vertical bands of tasks, but they are separated by long horizontal gaps where the workers are idle. These gaps correspond to the times when the central 

Thinker process is performing retrain and score operations, during which no new simulations are dispatched. The workers are being starved of tasks.

Standard Profiling Tools Are Insufficient
We confirmed that standard, single-process profilers are not well-suited for this multi-process application. As you noted, the Snakeviz output was not particularly helpful.

Gantt Chart

The plot  shows that the vast majority of the time in the main process is spent in 

thinker.join(). This is because cProfile only attached to the initial examol run process; it could not see inside the separate Thinker or the 32 Doer processes that Parsl spawned. This finding directly motivates the need for our proposed Profiloop toolchain (Contribution #2), which can aggregate data from across these distributed components.
