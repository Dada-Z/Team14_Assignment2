# library
import pandas as pd
import ipywidgets as widgets
from io import StringIO
from scipy.io import arff
from IPython.display import display
from collections import defaultdict
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse

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


# Load data file - we consider .arff files.
# only consider .arff file.
def load_arff(file_path):
    data, meta = arff.loadarff(file_path)
    df = pd.DataFrame(data)

    if 'Class' in df.columns:
        df = df.drop(columns = ['Class'])

    # Convert byte-encoded values to string
    df = df.applymap(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)

    # Convert to list of transactions
    transactions = df.apply(lambda row: {col for col in df.columns if row[col] == 'y'}, axis=1).tolist()
    
    return transactions

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run Apriori Algorithm on an ARFF dataset")
    parser.add_argument("file", type=str, help="Path to the dataset file (.arff)")
    parser.add_argument("--min_support", type=float, default=0.3, help="Minimum support threshold")
    parser.add_argument("--min_confidence", type=float, default=0.6, help="Minimum confidence threshold")

    args = parser.parse_args()

    # data
    transactions = load_arff(args.file)

    # Apriori Algorithm and Association Rules
    frequent_itemsets = apriori_algorithm(transactions, args.min_support)
    rules = association_rules(frequent_itemsets, transactions, args.min_confidence)

    # Save output as text files.
    # spending time on fixing error here. 
    # if keep using the following - error and error.
    # frequent_itemsets_df.to_csv("frequent_itemsets.txt", sep='\t', index=False)
    top_rules = sorted(rules, key=lambda x: x[3], reverse=True)[:10]

    print("Top 10 Association Rules Based on Confidence:")
    for antecedent, consequent, support, confidence in top_rules:
        print(f"{set(antecedent)} -> {set(consequent)} (Support: {support:.3f}, Confidence: {confidence:.3f})")
        
    with open("frequent_itemsets.txt", "w") as f:
        f.write("=== Frequent Itemsets ===\n")
        for itemset, support in frequent_itemsets.items():
            f.write(f"{set(itemset)} - Support: {support:.3f}\n")

    with open("association_rules.txt", "w") as f:
        f.write("=== Association Rules ===\n")
        for antecedent, consequent, support, confidence in rules:
            f.write(f"{set(antecedent)} → {set(consequent)} (Support: {support:.3f}, Confidence: {confidence:.3f})\n")

    ###########################################
    # plot
    min_support_fun = np.linspace(0.1, 0.5, 10)
    runtimes = []
    num_rule = []

    for min_support in min_support_fun:
        start_time = time.time()
        # Find frequent sets
        frequent_itemsets_test = apriori_algorithm(transactions, min_support)
        # Find association rules
        rules_test = association_rules(frequent_itemsets_test, transactions, args.min_confidence)

        # End
        end_time = time.time()

        # Save output
        runtimes.append(end_time - start_time)
        num_rule.append(len(rules_test))

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

if __name__ == "__main__":
    main()

# Observe the upload widget for changes
# uploader.observe(upload_function, names='value')
