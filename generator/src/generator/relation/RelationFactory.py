import inspect
import re
from typing import List

from generator.History import History
from generator.events.Function import Function
from generator.relation.Relation import Relation


class RelationFactory:
    __EVENT_METHODS = 'get_event|get_range|e'
    __TIME_METHODS = 'get_datetime|get_timestamp'
    __FUNC_METHOD = 'add_function'
    __ARG_POSITION = 'position'
    __ARG_DELAY = 'delay'
    __DEFAULT_ARG_EVENT = __ARG_POSITION
    __DEFAULT_ARG_TIME = __ARG_DELAY

    @staticmethod
    def build_relations(events: List[Function]):
        factory = RelationFactory()
        relations = []
        for event in events:
            relations += factory.__build_relation(event)

        return relations

    def __build_relation(self, event: Function) -> list:
        function_string = inspect.getsource(event.function)

        if re.search(rf'.*\.{self.__FUNC_METHOD}\(', function_string):
            scope_parts = re.split(r'([()])', function_string)
            key = 0
            while key < len(scope_parts):
                func_content = ''
                if re.search(rf'\.{self.__FUNC_METHOD}$', scope_parts[key]):
                    depth = 0
                    for local_part in scope_parts[key + 1:]:
                        key += 1
                        if local_part == '(':
                            depth += 1
                        if depth > 1 or local_part not in ['(', ')']:
                            func_content += local_part
                        if local_part == ')':
                            depth -= 1
                        if depth == 0:
                            break
                    function_string = func_content
                    break
                key += 1

        # Extract variable label.
        argument_groups = re.search(r'(.*def[^\n:]+\((.*?)\)|lambda *?(\w+))(.*)', function_string, re.DOTALL)
        function_arguments = argument_groups.group(2)
        if function_arguments is None:
            function_arguments = argument_groups.group(3)
        if function_arguments is None:
            return []

        function_content = argument_groups.group(4)

        var_name = re.split(r' *: *', function_arguments)[0]

        args = []
        # Extract all History method calls.
        regex = re.compile(
            rf'{var_name}\.(({self.__EVENT_METHODS})|(?P<time_method>{self.__TIME_METHODS}))'
            rf'\((?P<arguments>.*?)\)'
        )

        for method_parts in regex.finditer(function_content):
            items = method_parts.groupdict()
            arguments_string = items['arguments']
            is_time_method = items['time_method'] is not None
            default_position = 0 if is_time_method else History.DEFAULT_POSITION
            default_argument = self.__DEFAULT_ARG_TIME if is_time_method else self.__DEFAULT_ARG_EVENT
            arg = {self.__ARG_POSITION: default_position, self.__ARG_DELAY: History.DEFAULT_DELAY}
            if arguments_string != '':
                arguments = re.split(" *, *", arguments_string)
                for argument in arguments:
                    arg_value = re.split(' *= *', argument)
                    if len(arg_value) == 1:
                        arg_value = [default_argument, arg_value[0]]
                    arg[arg_value[0]] = arg_value[1]

            args.append(
                Relation(
                    source=int(event.position),
                    target=int(arg[self.__ARG_POSITION]),
                    delay=int(arg[self.__ARG_DELAY])
                )
            )

        return args
