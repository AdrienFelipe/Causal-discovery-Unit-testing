class EvaluateLearner:

    @staticmethod
    def compare_relations(real_relations, learned_relations):
        missing = []
        added = learned_relations.copy()
        inverted = []

        for real in real_relations:
            found = False
            for learned in added:
                if real.source == learned.source and real.target == learned.target:
                    added.remove(learned)
                    found = True
                    break
                elif real.source == learned.target and real.target == learned.source:
                    added.remove(learned)
                    inverted.append(learned)
                    found = True
                    break
            if not found:
                missing.append(real)

        return missing, added, inverted
