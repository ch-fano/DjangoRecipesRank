from SearchEngine.index import Index
from SearchEngine.model import IRModel
from functools import reduce


class Benchmark:

    def __init__(self, query):
        self.query = query
        self.index = Index()

    def get_results(self, n_result, model, verbose=False):
        my_model = IRModel(self.index, model)
        result = my_model.search(query=self.query["query"], res_limit=n_result, sentiments=self.query["sentiments"],
                                    verbose=verbose)

        results = [int(id) for id in result.keys()]
        if verbose:
            print(f'Results: {results}\nRelevant documents: {self.query["relevant_documents"]}')
            print(f'Relevant retrived: {set(results).intersection(set(self.query["relevant_documents"]))}')
        return results
    
    @staticmethod
    def recall(R, A):
        return round(len(set(R).intersection(set(A))) / len(R), 2) if len(R) > 0 else 0

    @staticmethod
    def precision(R, A):
        return round(len(set(R).intersection(set(A))) / len(A), 2) if len(A) > 0 else 0


    def get_precision_values(self, results_doc, verbose=False):
        precision_values = []

        for c in range(1, len(results_doc) + 1):
            precision_values.append(self.precision(self.query["relevant_documents"], results_doc[:c]))

        if verbose:
            print(f'Precision values: {precision_values}')

        return precision_values

    def get_recall_values(self, results_doc, verbose=False):
        recall_values = []
        for c in range(1, len(results_doc) + 1):
            recall_values.append(self.recall(self.query["relevant_documents"], results_doc[:c]))

        if verbose:
            print(f'Recall values: {recall_values}')

        return recall_values

    @staticmethod
    def get_srl_values(precision, recall, verbose=False):
        levels = [i / 10 for i in range(11)]
        srl_values = []

        if verbose:
            print(f'Natural Recall-Precision Values {zip(precision, recall)}')

        for level in levels:
            precisions = [p for p, r in zip(precision, recall) if r >= level]

            if precisions:
                srl_values.append(max(precisions))
            else:
                srl_values.append(0.0)

        srl_values = list(zip(levels, srl_values))

        if verbose:
            print(f'Standard Recall-Precision Values {srl_values}')
        return srl_values

    def get_ni_ap_avg_precision(self, precision, recall, verbose=False):
        ni_ap_avg_p = [precision[i] for i in range(len(recall)) if i == 0 or recall[i] != recall[i - 1]]

        if verbose:
            print(ni_ap_avg_p)

        return round(sum(ni_ap_avg_p) / len(self.query["relevant_documents"]), 2) if len(
            self.query["relevant_documents"]) != 0 else 0

    @staticmethod
    def get_i_ap_avg_precision(srl_values, verbose=False):
        sum_prec = reduce(lambda x, y: x + y, [srl_values[i][1] for i in range(len(srl_values))], 0)
        i_ap_avg_prec = round(sum_prec / len(srl_values), 2)

        if verbose:
            print(f"Interpolated Average precision: {i_ap_avg_prec}")

        return i_ap_avg_prec

    def get_r_precision(self, result, verbose=False):
        relevant_doc_retrived_first_r_position = set(result[:len(self.query["relevant_documents"])]).intersection(
            set(self.query["relevant_documents"]))
        r_prec = round(len(relevant_doc_retrived_first_r_position) / len(self.query["relevant_documents"]), 2) if len(
            self.query["relevant_documents"]) != 0 else 0

        if verbose:
            print(f"R-Precision: {r_prec}")

        return r_prec

    def get_f_measure(self, result, verbose=False):
        r = self.recall(self.query["relevant_documents"], result)
        p = self.precision(self.query["relevant_documents"], result)

        f_measure = round((2 * r * p) / (p + r), 2)

        if verbose:
            print(f"F-Measure: {f_measure}")

        return f_measure

    def get_e_measure(self, result, b, verbose=False):
        r = self.recall(self.query["relevant_documents"], result)
        p = self.precision(self.query["relevant_documents"], result)

        e_measure = round(1 - ((1 + b ** 2) / ((b ** 2) / r + 1 / p)), 2)

        if verbose:
            print(f"E-Measure: {e_measure}")

        return e_measure

    def __str__(self) -> str:
        return f'UIN: {self.query["UIN"]}\nQuery: {self.query["query"]}\nSentiments: {self.query["sentiments"]}\nRelevant documents: {self.query["relevant_documents"]} '