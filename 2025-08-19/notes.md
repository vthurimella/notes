Deepdrivemd on smc7

Running the following commands in the readme doesn't seem to work properly

$ conda create -n deepdrivemd python=3.9 -y
$ conda activate deepdrivemd
$ make install 

Updating to the following works correctly

bash```
conda deactivate
conda env remove -n deepdrivemd
conda create -n deepdrivemd python=3.9 -y
conda activate deepdrivemd
conda install -c conda-forge gcc=12.1.0 openmm MDAnalysis numpy -y
pip install -e .
```
