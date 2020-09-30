import pandas as pd
from causalinference import CausalModel
from causalinference.utils import random_data

from datasets.DatasetInterface import DatasetInterface
from tester.scripts.ScriptInterface import ScriptInterface


class CausalInferenceScript(ScriptInterface):
    name = 'Causal-inference'

    # https://github.com/laurencium/causalinference/blob/master/docs/tex/vignette.pdf

    def predict(self, dataset: DatasetInterface):
        data = dataset.get_data()

        size = len(data) // 2
        Y, X = data['E3'].to_numpy(), data[['E1', 'E2']].to_numpy()

        D = pd.np.concatenate((pd.np.zeros(size), pd.np.ones(len(data) - size)))
        pd.np.random.shuffle(D)
        causal = CausalModel(Y, D, X)

        one = causal.est_propensity()
        two = causal.est_propensity_s()
        three = causal.est_via_ols()
        four = causal.est_via_weighting()

        help(causal)

        f = 4
