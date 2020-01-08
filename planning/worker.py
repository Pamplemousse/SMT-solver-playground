from calendar import WeekDay


class Worker:
    def __init__(self, name, hours_per_week, availablities):
        """
        :param string name:
        :param int hours_per_week:
        :param dict[WeekDay,array[int]] availablities:
        """
        self._name = name
        self._hours_per_week = hours_per_week
        self._availabilities = availablities

    @property
    def availabilities(self):
        return self._availabilities

    @property
    def hours_per_week(self):
        return self._hours_per_week

    @property
    def name(self):
        return self._name



FULL_WEEK = { WeekDay.MONDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            , WeekDay.TUESDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            , WeekDay.WEDNESDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            , WeekDay.THURSDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            , WeekDay.FRIDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] }

FULL_WEEKEND = { WeekDay.SATURDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
               , WeekDay.SUNDAY: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
               }

TEAM = list(map(
    lambda x: Worker(*x),
    [ ('Michel Michel', 40, FULL_WEEK)
    , ('Amber Kyuk', 40, FULL_WEEK)
    , ('Stu Dent', 10, FULL_WEEKEND)
    ]
))
