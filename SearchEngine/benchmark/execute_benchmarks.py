import os
import json
from whoosh.scoring import BM25F
from SearchEngine.word2vec.doc2vec_model import Doc2VecModel
from SearchEngine.sentiment.sentiment_model import SentimentModelWA, SentimentModelARWA
import seaborn as sns
import pandas as pd

# file containing benchmark queries
file_path = os.path.join('./SearchEngine/benchmark', 'queries.json')

# loades the queries
with open(file_path) as f:
    queries = json.load(f)

# Models that need to be tested.
models = [
    (BM25F(), "BM25F"),
    (Doc2VecModel(), "Doc2Vec"),
    (SentimentModelWA(), "Sentiment Weighted Average"),
    (SentimentModelARWA(), "Sentiment Weighted Average Reviews")
]

indexes, uin = [i for i in range(len(queries))], [k["UIN"] for k in queries]
print('ID \t UIN')
print('\n'.join([f"{x[0]} \t {x[1]}" for x in list(zip(indexes, uin))]))

try:
    examined_q = 5
    print("User Information Need: " + queries[examined_q]["UIN"])
except IndexError as e:
    print("index not valid")

from SearchEngine.benchmark.benchmark_functions import Benchmark

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)  # Suppress the warning

b = Benchmark(queries[examined_q])

# define axes' names
axes = ["recall", "precision"]

# create a dataframe for Seaborn
df = pd.DataFrame()
for model, model_name in models:
    result = b.get_results(20, model)
    # get precision at standard recall values over list of result
    SRLValues = b.get_srl_values(
        b.get_precision_values(result),
        b.get_recall_values(result)
    )

    # tmp dataframe concatenated to the main one
    dfB = pd.DataFrame(SRLValues, columns=axes)
    dfB["Version"] = f'{model_name}'

    df = pd.concat([df, dfB])

sns.set_theme()

# plot the line graph
pltP = sns.lineplot(data=df, x='recall', y='precision', marker='o', markersize=4, hue="Version",
                    palette="colorblind")
pltP.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

# set fixed axes, the semicolon suppress the output
pltP.set_xlim([-0.1, 1.1]);
pltP.set_ylim([-0.1, 1.1]);

print(b)

IAPatSRL = {}

for q in queries:
    tmpB = Benchmark(q)
    for model, model_name in models:
        result = tmpB.get_results(20, model)
        SRLValues = tmpB.get_srl_values(
            tmpB.get_precision_values(result),
            tmpB.get_recall_values(result)
        )
        IAPatSRL.setdefault(model_name, []).append(
            SRLValues
        )

from functools import reduce
import matplotlib as plt

meansDict = {}

for k, v in IAPatSRL.items():
    # Trasporre la lista di liste per ottenere gli elementi corrispondenti
    transposed = list(zip(*v))

    # Calcolare la media dei secondi elementi delle tuple utilizzando reduce
    means = []
    for tuples in transposed:
        mean = reduce(lambda acc, t: acc + t[1], tuples, 0) / len(tuples)
        means.append((tuples[0][0], round(mean, 2)))

    meansDict[k] = means

# Convert the dictionary to a DataFrame
df_list = []

for key, value in meansDict.items():
    for x, y in value:
        df_list.append({'Version': key, 'Recall': x, 'Precision': y})

df = pd.DataFrame(df_list)

# Plotting with Seaborn
pltIAPatSRL = sns.lineplot(data=df, x='Recall', y='Precision', hue='Version', marker='o', markersize=4,
                           palette="colorblind")
pltIAPatSRL.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left');

pltIAPatSRL.set_xlim([-0.1, 1.1]);
pltIAPatSRL.set_ylim([-0.1, 1.1]);

from matplotlib.ticker import MultipleLocator
import textwrap

versions = []
AvPr_values = []

for model, model_name in models:
    result = b.get_results(20, model)
    SRLValues = b.get_srl_values(
        b.get_precision_values(result),
        b.get_recall_values(result)
    )

    AvPr_values.append(b.get_i_ap_avg_precision(SRLValues))
    versions.append(textwrap.fill(model_name, width=10,
                                  break_long_words=True))

# plot the average precisions
# apply the default theme
sns.set_theme()

# create a dataframe for Seaborn
df = pd.DataFrame({"Search-engine version": versions, "IAP at SRL": AvPr_values})

# plot the bar graph
pltAvPr = sns.barplot(data=df, x="Search-engine version", y='IAP at SRL', palette="colorblind")

# set fixed axes, the semicolon suppress the output
pltAvPr.set_ylim([0.0, max(AvPr_values) + 0.20]);  # set y-axis
pltAvPr.yaxis.set_major_locator(MultipleLocator(0.05))

print(b)

versions = []
RP_values = []

for model, model_name in models:
    result = b.get_results(20, model)

    RP_values.append(b.get_r_precision(result))

    versions.append(textwrap.fill(model_name, width=10,
                                  break_long_words=True))

# plot the average precisi+ons
# apply the default theme
sns.set_theme()

# create a dataframe for Seaborn
df = pd.DataFrame({"Search-engine version": versions, 'Precision@R': RP_values})

# plot the bar graph
pltRP = sns.barplot(data=df, x="Search-engine version", y='Precision@R', palette="colorblind")

# set fixed axes, the semicolon suppress the output
pltRP.set_ylim([0.0, max(AvPr_values) + 0.20]);  # set y-axis
pltRP.yaxis.set_major_locator(MultipleLocator(0.05))

print(b)

'''
Available models: 
- "BM25F"
- "Doc2Vec"
- "Sentiment Weighted Average"
- "Sentiment Weighted Average Reviews"
'''

model1 = "BM25F"
model2 = "Doc2Vec"

for model, model_name in models:
    if model1 == model_name:
        model1 = (model, model_name)
    if model2 == model_name:
        model2 = (model, model_name)

RP_comparison = []
for q in queries:
    tmpB = Benchmark(q)
    model1Res = tmpB.get_results(20, model1[0])
    model2Res = tmpB.get_results(20, model2[0])

    RP_comparison.append(
        tmpB.get_r_precision(model1Res) - tmpB.get_r_precision(model2Res)
    )

df = pd.DataFrame({
    'Queries': range(0, len(RP_comparison)),
    'R-Precision A/B': RP_comparison
})

pltRP_comp = sns.barplot(x='Queries', y='R-Precision A/B', data=df, color='skyblue')
pltRP_comp.set_title(f'R-Precision Comparison between {model1[1]} (A) and {model2[1]} (B)');

NIAP_dict = {}

for q in queries:

    tmpB = Benchmark(q)

    for model, model_name in models:
        result = tmpB.get_results(20, model)
        NIAP_dict.setdefault(model_name, []).append(tmpB.get_ni_ap_avg_precision(
            tmpB.get_precision_values(result),
            tmpB.get_recall_values(result),
        ))

MAP_list = []
versions = []

for model_name, p_list in NIAP_dict.items():
    MAP_list.append(round(sum(p_list) / len(p_list), 2) if len(p_list) != 0 else 0)

    versions.append(textwrap.fill(model_name, width=10,
                                  break_long_words=True))

# apply the default theme
sns.set_theme()

# create a dataframe for Seaborn
df = pd.DataFrame({"Search-engine version": versions, 'MAP': MAP_list})

# plot the bar graph
pltRP = sns.barplot(data=df, x="Search-engine version", y='MAP', palette="colorblind")

# set fixed axes, the semicolon suppress the output
pltRP.set_ylim([0.0, max(AvPr_values) + 0.20]);  # set y-axis
pltRP.yaxis.set_major_locator(MultipleLocator(0.05))

b_recall = 0.5  # Default value for emphasizing recall
b_precision = 1.5  # Default value for emphasizing precision

df = pd.DataFrame(columns=["Search-engine version"])
for model, model_name in models:
    result = b.get_results(20, model)

    data = {
        'F-Measure': [b.get_f_measure(result)],
        'E-Measure Recall': [b.get_e_measure(result, b_recall)],
        'E-Measure Precision': [b.get_e_measure(result, b_precision)]
    }

    tmpDf = pd.DataFrame(data)
    tmpDf["Search-engine version"] = textwrap.fill(model_name, width=10,
                                                   break_long_words=True)

    df = pd.concat([df, tmpDf])

# apply the default theme
sns.set_theme()

df_long = df.melt(id_vars='Search-engine version', var_name='Metric', value_name='Measure\'s Value')

# Crea il barplot
pltMeasures = sns.barplot(x='Search-engine version', y='Measure\'s Value', hue='Metric', data=df_long,
                          palette='icefire')
pltMeasures.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

# set fixed axes, the semicolon suppress the output
pltMeasures.set_ylim([0.0, df.iloc[:, -3:].max().max() + 0.1]);  # set y-axis

infolabel = f'E-Measure b value:\n- b for emphasizing recall: {b_recall} \n- b for emphasizing precision: {b_precision}'
pltMeasures.text(x=pltMeasures.get_xlim()[1] + 0.3, y=(pltMeasures.get_ylim()[0] + pltMeasures.get_ylim()[1]) / 2,
                 s=infolabel, fontsize=12, color='black', ha='left', va='center', rotation=0);

print(b)
