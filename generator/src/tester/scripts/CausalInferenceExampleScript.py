import pandas as pd
from causalinference import CausalModel
from causalinference.utils import random_data

from tester.scripts.ScriptInterface import ScriptInterface


class CausalInferenceExampleScript(ScriptInterface):
    name = 'Causal-inference (example)'

    # https://github.com/laurencium/causalinference/blob/master/docs/tex/vignette.pdf

    def predict(self, data: pd.DataFrame):
        Y, D, X = random_data()
        causal = CausalModel(Y, D, X)

        one = causal.est_propensity()
        two = causal.est_propensity_s()
        three = causal.est_via_ols()
        four = causal.est_via_weighting()

        help(causal)

        f = 4
