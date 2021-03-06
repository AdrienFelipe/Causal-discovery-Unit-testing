import inspect
import re
from typing import List

from generator.History import History
from generator.events.EventInterface import EventInterface
from generator.events.Function import Function
from generator.relation.Relation import Relation


class RelationFactory:
    __EVENT_METHODS = 'get_event|get_range|e'
    __TIME_METHODS = 'get_datetime|get_timestamp|t'
    __FUNC_METHOD = 'add_function'
    __ARG_POSITION = 'position'
    __ARG_DELAY = 'delay'
    __DEFAULT_ARG_EVENT = __ARG_POSITION
    __DEFAULT_ARG_TIME = __ARG_DELAY

    @staticmethod
    def build_relations(events: List[EventInterface], include_shadow=True):
        factory = RelationFactory()
        relations = []

        # Extract Function events.
        functions = [event for event in events if isinstance(event, Function)]
        for event in functions:
            relations += factory.__build_relation(event)

        # Exclude shadows events and link relations.
        if not include_shadow:
            relations = RelationFactory._remove_shadow_events(relations, events)

        return relations

    @staticmethod
    def _remove_shadow_events(relations: List[Relation], events: List[EventInterface]):
        """
        Rebuild relations after removing shadow events
        TODO for now this removes the time delay from relations
        """
        final_paths = []
        # List all sources and targets into separate lists.
        sources, targets = zip(*((relation.source, relation.target) for relation in relations))
        # Remove targets from sources to keep only root sources.
        paths = [[[root] for root in set(sources) - set(targets)]]
        # No root left means a circular relation. Use any source then.
        if len(paths[0]) == 0:
            paths[0].append([sources[0]])

        # Build paths.
        depth = 1
        while depth > 0:
            paths.append([])
            for path in paths[depth - 1]:
                is_final = True
                for relation in relations:
                    # Stop at circular loops.
                    if path[-1] == relation.source and path[-1] not in path[:-1]:
                        paths[depth].append([*path, relation.target])
                        is_final = False

                if is_final:
                    final_paths.append(path)

            depth = depth + 1 if len(paths[depth]) else -1

        # Remove shadow events.
        for path in final_paths:
            for item in path.copy():
                if events[item].shadow:
                    path.remove(item)

        # Rebuild relations.
        relations = []
        hashes = []
        for path in final_paths:
            for key in range(len(path) - 1):
                source = path[key]
                target = path[key + 1]
                relation_hash = f'{source}-{target}'
                if relation_hash in hashes:
                    continue
                hashes.append(relation_hash)
                relations.append(Relation(source, target))

        return relations

    def __build_relation(self, event: Function) -> list:
        """ Extract relations from events source code """
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
                    source=int(arg[self.__ARG_POSITION]),
                    target=int(event.position),
                    delay=int(arg[self.__ARG_DELAY])
                )
            )

        return args
