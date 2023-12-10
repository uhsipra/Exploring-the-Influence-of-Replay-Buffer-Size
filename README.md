# CMPUT655 Final Project
Final project for CMPUT 655

## GitHub Content
The file structure of the artifact is as follow:
* **DQN_NSTEP_CartPole.ipynb:** DQN NSTEP Jupyter Notebook for CartPole, outputs a csv in your google drive
* **DQN_NSTEP_LunarLander.ipynb:** DQN NSTEP Jupyter Notebook for LunarLander, outputs a csv in your google drive
* **graphs.py:** takes csv data and creates a data visualisations of results (rewards vs time-steps) 
* **graphs_individual.py:** takes csv data and creates a data visualisations of results (rewards vs time-steps) but has individual lines for each run

## Step-by-Step Reproduction of Results

1. Open Google Colab (https://colab.research.google.com/) and upload `DQN_NSTEP_LunarLander.ipynb` to run in your local Google Drive
2. Run `DQN_NSTEP_LunarLander.ipynb` on Google Colab, this will require google sign in to store the resulting data in your local Google Drive
3. Download the results (.csv) found in your google drive
4. Change the file name at the top of `graphs_individual.py` to the corresponding .csv file and make sure to run the program with the .csv file in the same folder
