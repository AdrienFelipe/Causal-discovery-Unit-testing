# for making sample data
# for visualization
import medil.visualize as vis
import numpy as np
import pandas as pd
# for step 2
from medil.ecc_algorithms import find_clique_min_cover as find_cm
from medil.examples import triangle
from medil.functional_MCM import MeDILCausalModel  # also used in step 3
from medil.functional_MCM import gaussian_mixture_sampler
from medil.functional_MCM import uniform_sampler, GAN
from medil.independence_testing import distance_correlation
# for step 1
from medil.independence_testing import hypothesis_test
# for step 3
from pytorch_lightning import Trainer

from datasets.DatasetInterface import DatasetInterface
from tester.scripts.ScriptInterface import ScriptInterface


class MeDILExampleScript(ScriptInterface):
    name = 'MeDIL (example)'

    # https://causal.dev/files/medil_demo.pdf
    # https://medil.causal.dev/tutorial.html

    def predict(self, dataset: DatasetInterface):
        # make sample data
        num_latent, num_observed = triangle.MCM.shape

        decoder = MeDILCausalModel(biadj_mat=triangle.MCM)
        sampler = gaussian_mixture_sampler(num_latent)

        input_sample, output_sample = decoder.sample(sampler, num_samples=1000)
        np.save("measurement_data", output_sample)

        # step 1: estimate UDG
        p_vals, null_corr, dep_graph = hypothesis_test(output_sample.T, num_resamples=100)
        # dep_graph is adjacency matrix of the estimated UDG

        # step 2: learn graphical MCM
        learned_biadj_mat = find_cm(dep_graph)

        # step 3: learn functional MCM
        num_latent, num_observed = learned_biadj_mat.shape

        decoder = MeDILCausalModel(biadj_mat=learned_biadj_mat)
        sampler = uniform_sampler(num_latent)

        minMCM = GAN("measurement_data.npy", decoder, latent_sampler=sampler, batch_size=100)
        trainer = Trainer(max_epochs=100)
        trainer.fit(minMCM)

        # confirm given and learned causal structures match
        vis.show_dag(triangle.MCM)
        vis.show_dag(learned_biadj_mat)

        # compare plots of disttrance correlation values for given and learned MCMs
        generated_sample = decoder.sample(sampler, 1000)[1].detach().numpy()
        generated_dcor_mat = distance_correlation(generated_sample.T)

        vis.show_obs_dcor_mat(null_corr, print_val=True)
        vis.show_obs_dcor_mat(generated_dcor_mat, print_val=True)

        # get params for learned functional MCM; replace '0' with 'i' to get params for any M_i
        result = decoder.observed["0"].causal_function

        f = 4
