pip:
		./env/bin/pip $(filter-out $@,$(MAKECMDGOALS))

conda:
		conda $(filter-out $@,$(MAKECMDGOALS)) --prefix env/
