# CSSV-Restriction-Analysis
Identification of a set of restriction enzymes which could be used to distinguish the different strains of Cacao Swollen Shoot Virus:

Must be provided with a file in the format of the example document which is included using argv. This file is a text file with each line containing the GenBank 
accession code and the name of a restriction enzyme which cuts it, separated by a tab. For this reason I use .py since it formats well.

restriction_sites.py is an example of input data format.

count.py contains the classes to generate the enzyme and species objects.

main.py contains the main code which tests random sets of enzymes, and reports back the best set of enzymes. The criteria for this is the number of genome clusters, i.e. if these enzymes were used on all the species, how many different profiles are there.

main_range.py varies the number of enzymes used in each set, (can be adapted for any range). For each number of enzymes, the program generates 100000 random enzyme sets and determines the number of clusters for each. The program reports the highest number of clusters produced for each number, as well as the data for each random set for analysis. Columns are the number of enzymes.

main_enzymes.py is used to calculate the average number of clusters generated when each enzyme is part of the randomly generated set. This can be used to quantify the quality of each of the enzymes nicely.
