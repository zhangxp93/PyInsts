from pyinsts.concurrent.concurren import ConcurrentTask


def _double(value: int) -> int:
    return value * 2


def _add(a: int, b: int) -> int:
    return a + b


def test_concurrent_task_runs_in_parallel():
    with ConcurrentTask(max_workers=2) as task:
        task.run_async("double", _double, 21)
        task.run_async("add", _add, 1, 2)

        double_result, add_result = task.get_all_results("double", "add")

    assert double_result == 42
    assert add_result == 3


def test_concurrent_task_missing_name_raises():
    with ConcurrentTask(max_workers=1) as task:
        try:
            task.get_result("missing")
            raised = False
        except KeyError:
            raised = True

    assert raised
