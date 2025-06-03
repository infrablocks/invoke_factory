from typing import Iterable
from unittest.mock import Mock

from invoke.collection import Collection
from invoke.context import Context

from infrablocks.invoke_factory.task_factory import (
    Arguments,
    Parameter,
    create_task,
)


class TestTaskFactory:
    def test_invocation_of_locally_defined_function(self):
        def task_body(_context: Context, _arguments: Arguments) -> None:
            pass

        context = Context()
        task = create_task(task_body)

        task(context)

        # doesn't blow up

    def test_invokes_body_when_task_is_executed(self):
        mock_task = Mock()
        mock_task.__name__ = "mock_task"
        context = Context()
        task = create_task(mock_task)

        task(context)

        mock_task.assert_called_once()

    def test_invokes_body_with_context_when_task_is_executed(self):
        mock_task = Mock()
        mock_task.__name__ = "mock_task"
        context = Context()
        task = create_task(mock_task)

        task(context)

        args, _ = mock_task.call_args
        assert args[0] is context

    def test_invokes_body_with_arguments_when_task_is_executed(self):
        parameters: Iterable[Parameter] = [{"name": "foo"}]
        mock_task = Mock()
        mock_task.__name__ = "mock_task"
        task = create_task(mock_task, parameters)

        task(Context(), foo=100)

        args, _ = mock_task.call_args
        assert args[1]["foo"] == 100

    def test_includes_parameter_help_in_task(self):
        parameters: Iterable[Parameter] = [
            {"name": "foo", "help": "Foo help"},
            {"name": "bar", "help": "Bar help"},
        ]
        mock_task = Mock()
        mock_task.__name__ = "mock_task"
        task = create_task(mock_task, parameters)

        assert task.help == {
            "foo": "Foo help",
            "bar": "Bar help",
        }

    def test_created_task_can_be_added_to_collection(self):
        parameters: Iterable[Parameter] = [{"name": "foo"}]
        mock_task = Mock()
        mock_task.__name__ = "mock_task"
        collection = Collection()

        task = create_task(mock_task, parameters)
        collection.add_task(task)

        assert len(collection.tasks) == 1
