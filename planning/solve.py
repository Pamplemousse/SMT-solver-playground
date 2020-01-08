"""
Generate a work schedule for *ONE* week.
"""

import time
from functools import reduce

from z3 import And, Int, IntVal, Or, sat, Solver


from calendar import WORK_WEEK
from display import print_planning_per_day_per_worker
from worker import TEAM


def get_variable_name(worker_name, day, hour):
    return Int("%s %s %s" % (worker_name, day.value, hour))


# Memoize this function via a side-effect.
_variables_for_workers = {}
def variables_for_worker(worker):
    def _availabilities_variables_per_day(worker, day):
        hours_available = list(filter(
            lambda x: x[1] == 1,
            enumerate(worker.availabilities[day]),
        ))

        return list(map(
            lambda x: get_variable_name(worker._name, day, x[0]),
            hours_available,
        ))

    if worker not in _variables_for_workers.keys():
        availabilities = reduce(
            lambda acc, x: acc + _availabilities_variables_per_day(worker, x[0]),
            worker.availabilities.items(),
            []
        )

        _variables_for_workers[worker] = availabilities

    return _variables_for_workers[worker]


def work_their_hours(workers):
    def work_its_hours(worker):
        sum_of_hours = sum(variables_for_worker(worker))
        number_of_hours_to_work = IntVal(worker.hours_per_week)

        return sum_of_hours == number_of_hours_to_work

    return And(list(map(
        lambda w: work_its_hours(w),
        workers
    )))


def hours_on_schedule_are_either_worked_or_not(hours):
    return And(list(map(
        lambda h: Or([ h == 0, h == 1 ]),
        hours
    )))


def enough_people_are_working(week, team, schedule):
    def enough_people_are_working_daily(day, team, schedule):
        def enough_people_are_working_hourly(hour, weekday, schedule):
            workforce = sum(filter(
                # Variable appears in schedule only if worker is available.
                lambda var: var in schedule,
                list(map(
                    lambda worker: get_variable_name(worker._name, weekday, hour),
                    team
                ))
            ))

            return day.schedule_requirements[hour] == workforce

        return reduce(
            lambda acc, d: acc + [ enough_people_are_working_hourly(d[0], day.day, schedule) ],
            enumerate(day.schedule_requirements),
            []
        )

    return And(reduce(
        lambda acc, w: acc + enough_people_are_working_daily(w, team, schedule),
        week,
        []
    ))


# SCHEDULE is the set of variables representing all the workers available slots;
# Values for these variables fully describe a work schedule.
SCHEDULE = reduce(
    lambda acc, w: acc + variables_for_worker(w),
    TEAM,
    []
)

formula = And([
    hours_on_schedule_are_either_worked_or_not(SCHEDULE),
    work_their_hours(TEAM),
    enough_people_are_working(WORK_WEEK, TEAM, SCHEDULE),
])


print('Formula is ready!')

solver = Solver()
second = 1000
minute = 60 * second
solver.set('timeout', 5 * minute)
solver.add(formula)

start = time.clock()
is_formula_sat = solver.check()
end = time.clock()

print('Formula is %s, in %f seconds' % (is_formula_sat, end - start))

if is_formula_sat == sat:
    model = solver.model()
    print_planning_per_day_per_worker(model, WORK_WEEK, TEAM, get_variable_name)
else:
    print("No solution found")

import ipdb; ipdb.set_trace()
pass
