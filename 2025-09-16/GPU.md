# Met with Nicholas about GPU metrics

nsys can be used to visualize when there is a big change between two different applications on the GPU. nsys stores all GPU information in a sqlite database that is visualized.

$ nsys stats --report=cuda_gpu_trace output .