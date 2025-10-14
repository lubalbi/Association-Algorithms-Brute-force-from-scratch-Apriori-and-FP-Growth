Instructions to Run the Association Rule Mining Program

1. Prerequisites:
- Python 3.9+ must be installed.
- The following files and folders are included in the submission:

	/Running_all_the_algorithms.ipynb (Jupyter Notebook)
	/Project_report.pdf (Tutorial report)
	/BruteForce.py (Standalone script)
	/Apriori.py (Standalone script)
	/FPGrowth.py (Standalone script)
	/readme.txt (This file)
	/Data/ (Folder with all CSV datasets)
	/Screenshots/ (Folder with all PNG screenshots)

2. Installing Required Libraries:
- Open a command prompt or terminal and run the following command to install all necessary libraries:
	pip install pandas numpy apyori mlxtend

3. Steps to Run the Code:
a. Running the Full Project in Jupyter Notebook
- Open a command prompt, navigate to the project directory, and start Jupyter:
	jupyter notebook
- Open the file 'Running_all_the_algorithms.ipynb' and run the cells.

b. Running Standalone Scripts from the Command Line
- Open a command prompt and navigate to the project directory.
- To run the Brute-Force algorithm only:
	python BruteForce.py
- To run the Apriori algorithm only:
	python Apriori.py
- To run the FP-Growth algorithm only:
	python FPGrowth.py

Note: The standalone scripts are interactive and will prompt you to select a dataset and enter support and confidence values.

c. View the Output
The results of the analysis, including association rules and execution times, will be printed directly to the notebook output or the command prompt window.

Student: Lucas Marques Balbi