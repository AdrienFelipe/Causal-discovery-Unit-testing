from discovery.EvaluateLearner import EvaluateLearner
from ui.config import scripts, datasets

exit(EvaluateLearner.run(scripts, datasets, output=EvaluateLearner.TABLE_OUTPUT, force_rebuild=True))
