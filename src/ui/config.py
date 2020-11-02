from __future__ import annotations

from datasets.unit.ChainedCausalityDataset import ChainedCausalityDataset
from datasets.unit.DirectCausalityDataset import DirectCausalityDataset
from datasets.unit.MultipleCausesCausalityDataset import MultipleCausesCausalityDataset
from datasets.unit.MultipleEffectsCausalityDataset import MultipleEffectsCausalityDataset
from datasets.unit.RelationalCausalityDataset import RelationalCausalityDataset
from discovery.scripts.PgmpyScript import PgmpyScript
from discovery.scripts.PyAgrumScript import PyAgrumScript

datasets2 = [
    DirectCausalityDataset.linear(100),
    DirectCausalityDataset.square_root(100),
    DirectCausalityDataset.power(100),
    DirectCausalityDataset.exponential(100),
    MultipleCausesCausalityDataset.linear(100),
    MultipleCausesCausalityDataset.power(100),
    MultipleEffectsCausalityDataset.linear(100),
    MultipleEffectsCausalityDataset.power(100),
    ChainedCausalityDataset.linear(100)
]

datasets = [
    MultipleCausesCausalityDataset.discrete(1000),
    DirectCausalityDataset.linear(1000),
]

success = [
    MultipleCausesCausalityDataset.discrete(1000),
    DirectCausalityDataset.linear(1000),
]

final = [
    RelationalCausalityDataset.discrete(100),
    ChainedCausalityDataset.linear(100),
    DirectCausalityDataset.linear(100),
    DirectCausalityDataset.square_root(100),
    DirectCausalityDataset.power(100),
    DirectCausalityDataset.exponential(100),
    MultipleCausesCausalityDataset.linear(100),
    MultipleCausesCausalityDataset.power(100),
    MultipleEffectsCausalityDataset.linear(100),
    MultipleEffectsCausalityDataset.power(100),
    ChainedCausalityDataset.linear(100),
]

scripts = [
    PgmpyScript.PC(),
    PgmpyScript.GES(),
    PyAgrumScript.GES(),
    PyAgrumScript.TS(),
]
