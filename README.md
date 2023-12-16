# CMPUT655 Final Project
Final project for CMPUT 655

## GitHub Content
The file structure of the artifact is as follow:
* **07_n_step_learning_*.ipynb:** Notebook to test individual configurations and plot the loss and cumulative reward during learning in real time
* **DQN_NSTEP_CartPole.ipynb:** DQN NSTEP Jupyter Notebook for CartPole, outputs a csv in your google drive
* **DQN_NSTEP_FrozenLake.ipynb:** DQN NSTEP Jupyter Notebook for FrozenLake, outputs a csv in your google drive
* **DQN_NSTEP_LunarLander.ipynb:** DQN NSTEP Jupyter Notebook for LunarLander, outputs a csv in your google drive
* **graphs.py:** Takes csv data and creates a data visualisations of results (rewards vs time-steps) 
* **graphs_individual.py:** Takes csv data and creates a data visualisations of results (rewards vs time-steps) but has individual lines for each run
* **compute last 100 table.py:** Computes statistics for data and outputs them in latex format
* **Data Folder** Contains the data from all runs of the frozen lake and lunar lander runs

## Step-by-Step Reproduction of Results

1. Open Google Colab (https://colab.research.google.com/) and upload `DQN_NSTEP_\*.ipynb` to run in your local Google Drive
2. Run `DQN_NSTEP_\*.ipynb` on Google Colab, this will require google sign in to store the resulting data in your local Google Drive
3. Download the results (.csv) found in your google drive
4. Change the file path at the top of `graphs.py` and `compute last 100 table.py` to the corresponding folder containing csvs, and the outputs will be an image or a latex table respectivly.
5. Setting the group_x or the group_y parameter in `graphs.py` to `True` will change the type of graph generated, and roll up along the given axis; if both are false, it will output a grid of plots.
