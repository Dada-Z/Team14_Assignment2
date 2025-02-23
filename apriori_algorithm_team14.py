# load data
import pandas as pd
from scipy.io import arff

file_path = "/content/test.arff"
data, meta = arff.loadarff(file_path)

# Convert data to dataframe
df = pd.DataFrame(data)
# again
df = df.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
# compute transcation
transactions = df.apply(lambda row: [col for col in df.columns if row[col] == 'y'], axis=1).tolist()
# check
# print(df.shape)
# df.head(3)

# library
from collections import defaultdict
import pandas as pd
import numpy as np
from itertools import combinations
from IPython.display import display

# There are multiple way to do this
# but we consider transaction and minimum support at the beginning.
# similar to the first try (w/o defining a function), find frequent sets.

def apriori_algorithm(transactions, min_support):
    item_counts = defaultdict(int)
    num_transactions = len(transactions)

    # count occurrences
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1

    # define frequent sets
    frequent_itemsets = {
        itemset: count / num_transactions
        for itemset, count in item_counts.items()
        if (count / num_transactions) >= min_support}

    k = 2
    current_itemsets = list(frequent_itemsets.keys())

    while current_itemsets:
        candidate_counts = defaultdict(int)

        # find candidate
        candidates = [i.union(j) for i in current_itemsets for j in current_itemsets if len(i.union(j)) == k]
        candidates = list(set(candidates))

        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] += 1

        filtered_candidates = {
            itemset: count / num_transactions
            for itemset, count in candidate_counts.items()
            if (count / num_transactions) >= min_support}

        current_itemsets = list(filtered_candidates.keys())

        # update and save frequent sets
        frequent_itemsets.update(filtered_candidates)

        k += 1

    return frequent_itemsets


def association_rules(frequent_itemsets, transactions, min_confidence):
    # similar as above
    num_transactions = len(transactions)
    rules = []

    for itemset in frequent_itemsets.keys():
        if len(itemset) > 1:
            for consequent_size in range(1, len(itemset)):
                for consequent in combinations(itemset, consequent_size):
                    antecedent = itemset.difference(consequent)

                    if antecedent and consequent:
                        antecedent_support = frequent_itemsets.get(frozenset(antecedent), 0)
                        rule_support = frequent_itemsets[itemset]
                        confidence = rule_support / antecedent_support if antecedent_support > 0 else 0

                        if confidence >= min_confidence:
                            rules.append((set(antecedent), set(consequent), rule_support, confidence))

    return rules

#############################
# Using 0.3 as a threshold of minimum support
# we will continue using it in Weka.
threshold_min_support = 0.3
frequent_itemsets = apriori_algorithm(transactions, threshold_min_support)
# print results, need to do convertion
frequent_itemsets_df = pd.DataFrame([(set(itemset), support) for itemset, support in frequent_itemsets.items()], columns=["Itemset", "Support"])
print(f"Total frequent sets: {len(frequent_itemsets)}")
display(frequent_itemsets_df)

# Using a threshold of 0.6 (60%) for confidence
threshold_min_confidence = 0.6
association_rules_output = association_rules(frequent_itemsets, transactions, threshold_min_confidence)
association_rules_df = pd.DataFrame(association_rules_output, columns=["Antecedent", "Consequent", "Support", "Confidence"])
# print
print(f"Total association rules: {len(association_rules_output)}")
display(association_rules_df)

# save frequent itemsets as text file
frequent_itemsets_df.to_csv("frequent_itemsets.txt", sep='\t', index=False)
# save association rules as text file
association_rules_df.to_csv("association_rules.txt", sep='\t', index=False)

"""# Part II. Plot"""

import time
import matplotlib.pyplot as plt

# Using practice code, define min_support
min_support_fun = np.linspace(0.1, 0.5, 10)
runtimes = []
num_rule = []

# loop for plot
for min_support in min_support_fun:
    start_time = time.time()
    # find frequent sets
    frequent_itemsets_test = apriori_algorithm(transactions, min_support) # corresponding to function
    # find association rules
    rules_test = association_rules(frequent_itemsets_test, transactions, threshold_min_confidence)

    # End
    end_time = time.time()

    # Save output
    runtimes.append(end_time - start_time)
    num_rule.append(len(rules_test))

###########################################
# plot
# Use min_support_fun instead of min_support for plotting
plt.figure(figsize=(5, 5))
plt.plot(min_support_fun, runtimes, marker='o', linestyle='-', color="r", label="Apriori Runtime (seconds)")
plt.xlabel("Minimum Support")
plt.ylabel("Runtime of Apriori (seconds)")
plt.title("Runtime of Apriori vs. Minimum Support")
plt.legend()
plt.grid()
# save plot
plt.savefig("runtime_algorithm.png")
plt.show()

# continue - plot Apriori algorithm and number of rules
plt.figure(figsize=(5, 5))
# Use min_support_fun instead of min_support for plotting
plt.plot(min_support_fun, num_rule, marker='s', linestyle='-', color="b", label="Number of Rules")
plt.xlabel("Minimum Support")
plt.ylabel("Number of Rules")
plt.title("Number of Rules vs. Minimum Support")
plt.legend()
plt.grid()
# save plot
plt.savefig("runtime_number_rules.png")
plt.show()