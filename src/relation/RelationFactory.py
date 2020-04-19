import inspect
import re
from typing import List

from History import History
from events.Effect import Effect
from relation.Relation import Relation


class RelationFactory:
    __METHOD_NAME = 'get_event'
    __TIME_METHODS = 'get_datetime|get_timestamp'
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
        argument_groups = re.search(r'^[^\n:]+\((.*?)\)|lambda *?(\w+)', function_string)
        function_arguments = argument_groups.group(1)
        if function_arguments is None:
            function_arguments = argument_groups.group(2)
        if function_arguments is None:
            return []

        var_name = re.split(r' *: *', function_arguments)[0]

        args = []
        # Extract all History method calls.
        regex = re.compile(
            rf'{var_name}\.({self.__METHOD_NAME}|(?P<time_method>{self.__TIME_METHODS}))'
            rf'\((?P<arguments>.*?)\)'
        )

        for method_parts in regex.finditer(function_string):
            items = method_parts.groupdict()
            arguments_string = items['arguments']
            is_time_method = items['time_method'] is not None
            default_position = 0 if is_time_method else History.DEFAULT_POSITION
            arg = {self.__ARG_POSITION: default_position, self.__ARG_DELAY: History.DEFAULT_DELAY}
            if arguments_string is not '':
                arguments = re.split(" *, *", arguments_string)
                for argument in arguments:
                    arg_value = re.split(' *= *', argument)
                    if len(arg_value) == 1:
                        arg_value = [self.__ARG_POSITION, arg_value[0]]
                    arg[arg_value[0]] = arg_value[1]

            args.append(
                Relation(
                    source=int(event.position + History.DEFAULT_POSITION),
                    target=int(arg[self.__ARG_POSITION]),
                    delay=int(arg[self.__ARG_DELAY])
                )
            )

        return args
