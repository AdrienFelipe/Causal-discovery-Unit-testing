import inspect
import re
from typing import List

from History import History
from Relation import Relation
from events.Effect import Effect


class RelationFactory:
    __METHOD_NAME = 'get_effect'
    __ARG_POSITION = 'position'
    __ARG_DELAY = 'delay'

    @staticmethod
    def build_relations(events: List[Effect]):
        factory = RelationFactory()
        relations = []
        for event in events:
            relations += factory.__build_relation(event)

        return relations

    def __build_relation(self, event: Effect) -> list:
        function_string = inspect.getsource(event.effect)

        # Extract variable name.
        function_arguments = re.search(r'^[^\n]+\((.*?)\)', function_string).group(1)
        var_name = re.split(r' *: *', function_arguments)[0]

        args = []
        # Extract all History method calls.
        method_calls = re.findall(rf'{var_name}\.{self.__METHOD_NAME}\((.*?)\)', function_string)
        for arguments_string in method_calls:
            arg = {self.__ARG_POSITION: History.DEFAULT_POSITION, self.__ARG_DELAY: History.DEFAULT_DELAY}
            if arguments_string is not '':
                arguments = re.split(" *, *", arguments_string)
                for argument in arguments:
                    arg_value = re.split(' *= *', argument)
                    if len(arg_value) == 1:
                        arg_value = [self.__ARG_POSITION, arg_value[0]]
                    arg[arg_value[0]] = arg_value[1]

            args.append(
                Relation(
                    int(event.position + History.DEFAULT_POSITION),
                    int(arg[self.__ARG_POSITION]),
                    int(arg[self.__ARG_DELAY])
                )
            )

        return args
