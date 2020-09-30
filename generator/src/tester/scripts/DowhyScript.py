import pandas as pd
from dowhy import CausalModel

from datasets.DatasetInterface import DatasetInterface
from tester.scripts.ScriptInterface import ScriptInterface


class DowhyScript(ScriptInterface):
    name = 'dowhy'

    def predict(self, dataset: DatasetInterface):
        data = dataset.get_data()

        # Temporally add treatment.
        data['treatment'] = True
        treatment = 'treatment'

        outcome = dataset.get_outcome()
        common_causes = dataset.get_causes()

        model = CausalModel(data, treatment, outcome, common_causes=common_causes, proceed_when_unidentifiable=True)

        # Identify the causal effect
        relation = model.identify_effect()

        # Estimate the causal effect
        estimate = model.estimate_effect(relation, method_name="backdoor.linear_regression", test_significance=True)

        # Refute the obtained estimate
        result = model.refute_estimate(relation, estimate, method_name="random_common_cause")

        return result.estimated_effect, result.new_effect

    def predict_tutorial(self, data: pd.DataFrame):
        # https://towardsdatascience.com/implementing-causal-inference-a-key-step-towards-agi-de2cde8ea599
        data = pd.read_csv(
            'https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv',
            header=None)
        col = ['treatment', 'y_factual', 'y_cfactual', 'mu0', 'mu1', ]

        for i in range(1, 26):
            col.append('x' + str(i))

        data.columns = col
        data = data.astype({'treatment': 'bool'}, copy=False)
        result = data.head()

        # Create a causal model from the data and given common causes.
        xs = ""
        for i in range(1, 26):
            xs += ("x" + str(i) + "+")
        model = CausalModel(
            data=data,
            treatment='treatment',
            outcome='y_factual',
            common_causes=xs.split('+')
        )

        # Identify the causal effect
        identified_estimand = model.identify_effect()
        print(identified_estimand)

        # Estimate the causal effect and compare it with Average Treatment Effect
        estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression",
                                         test_significance=True)
        print(estimate)
        print("Causal Estimate is " + str(estimate.value))

        refute_results = model.refute_estimate(identified_estimand, estimate,
                                               method_name="random_common_cause")
        print(refute_results)

        dd = 3

    def predict_example(self, data: pd.DataFrame):
        # https://github.com/Microsoft/dowhy
        # https://ntanmayee.github.io/articles/2018/11/16/tools-for-causality.html

        x = 'E1'
        y = 'E3'
        causes = ['E1', 'E2']

        model = CausalModel(data=data, treatment=causes, outcome=y, proceed_when_unidentifiable=True)

        # Identify causal effect and return target estimands
        identified_estimand = model.identify_effect()

        # Estimate the target estimand using a statistical method.
        estimate = model.estimate_effect(identified_estimand,
                                         method_name="backdoor.propensity_score_matching")

        # Refute the obtained estimate using multiple robustness checks.
        refute_results = model.refute_estimate(identified_estimand, estimate,
                                               method_name="random_common_cause")
