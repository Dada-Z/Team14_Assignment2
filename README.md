# Assignment2 Team 14
Team member: Dada Zhang, Nick Montemarano

This repo is used for Data Mining - Assignment 2: *Apriori* algorithm.

The file contains 4 components:

1. Data: vote.arff and test.arff

2. Python file: determine frequent sets and generate association rules
- **Apriori_algorithm_vote_data.ipynb:** practice on Aprior algorithm using "vote.arff" dataset
- **apriori_algorithm_team14_test.py:** assignment submission
  + run python file, including python script, data, input minimum for support and confidence
  + !python apriori_algorithm_team14_test.py test.arff --min_support 0.3 --min_confidence 0.6

3. Plots: the runtime of algorithm and the number of rules as a function of "minimum support"
- runtime_algorithm.png
- runtime_number_rules.png

4. Output: 
- Two text files for frequent sets and association rules.
  + frequent_itemsets.txt
  + association_rules.txt
- Weka output (**Weka_test_output_0.3_0.6.txt**):
  + The inputs are lowerBoundMinSupport=0.3 and minMetric=0.6
  + The output of association rule from Weka was saved in text file

5. Report: pdf file contains contribution form (cover page).
- Zhang_Montemarano.pdf
