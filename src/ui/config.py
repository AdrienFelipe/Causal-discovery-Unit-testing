from __future__ import annotations

from datasets.causality.ChainedCausalityDataset import ChainedCausalityDataset
from datasets.causality.DirectCausalityDataset import DirectCausalityDataset
from datasets.causality.MultipleCausesCausalityDataset import MultipleCausesCausalityDataset
from discovery.scripts.PgmpyScript import PgmpyScript
from discovery.scripts.PyAgrumScript import PyAgrumScript

datasets = [
    MultipleCausesCausalityDataset.discrete(1000),
    DirectCausalityDataset.linear(1000),
    ChainedCausalityDataset.linear(100),
]

scripts = [
    PgmpyScript.PC(),
    PgmpyScript.GES(),
    PyAgrumScript.GES(),
    PyAgrumScript.TS(),
]
