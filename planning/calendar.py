from enum import Enum


class WeekDay(Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


class WorkDay:
    def __init__(self, week_day, schedule_requirements):
        """
        :param WeekDay day:
        :param array[int] schedule:
            Encode the requirements for a day of work.
            Each entry of the array represent a 1h slice of the day, from 8am to 6pm,
            and contains an integer value indicating the number of worker required on that slice.
        """
        self._day = week_day
        self._schedule_requirements = schedule_requirements

    @property
    def day(self):
        return self._day

    @property
    def schedule_requirements(self):
        return self._schedule_requirements


WORK_WEEK = list(map(
    lambda x: WorkDay(*x),
    [ (WeekDay.MONDAY, [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0])
    , (WeekDay.TUESDAY, [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0])
    , (WeekDay.WEDNESDAY, [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0])
    , (WeekDay.THURSDAY, [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0])
    , (WeekDay.FRIDAY, [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0])
    , (WeekDay.SATURDAY, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])
    , (WeekDay.SUNDAY, [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    ]
))
