from infrablocks.invoke_factory.dynamic_task import DynamicTask


class TestTask:
    def test_example(self):
        task = DynamicTask()
        assert task is not None
