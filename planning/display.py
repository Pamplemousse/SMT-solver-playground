def print_planning_per_day_per_worker(model, work_week, team, variable_builder):
    """
    :param z3.z3.ModelRef model:
    :param list[WorkDay] work_week:
    :param list[Worker] team:
    :param function variable_builder:
        The function to compute the variable corresponding to a worker's hour of work in a day.
        Takes a worker_name (string), a day (WeekDay), and an hour (int) as parameter.
    """
    for worker in team:
        print('-----')
        print('%s:' % worker.name)

        for workday in work_week:
            def _works_or_not(worker, day, hour):
                variable = variable_builder(worker.name, day, hour)
                value = model[variable]
                return 0 if value is None else value

            shift = list(map(
                lambda hour: _works_or_not(worker, workday.day, hour),
                range(len(workday.schedule_requirements))
            ))

            print('\t%s: %s' % (workday.day.value, shift))
