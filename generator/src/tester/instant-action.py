# noinspection PyUnresolvedReferences
import dowhy.api
import pandas as pd

# https://github.com/Microsoft/dowhy
# https://ntanmayee.github.io/articles/2018/11/16/tools-for-causality.html

# Load some sample data
filepath = 'datasets/instant-action.pkl'
data = pd.read_pickle(filepath)

x = 'E1'
y = 'E3'
causes = ['E1', 'E2']

# Create a causal model from the data and given graph.
model = data.causal.do(x=x, outcome=y, common_causes=causes, proceed_when_unidentifiable=True)

# Identify causal effect and return target estimands
identified_estimand = model.identify_effect()

# Estimate the target estimand using a statistical method.
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.propensity_score_matching")

# Refute the obtained estimate using multiple robustness checks.
refute_results = model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause")

f = 3
