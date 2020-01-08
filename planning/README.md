# Planning generation

Generate a planning, from:
  * [`TEAM`](worker.py); A team of workers, each of them having:
    - Availabilities: hours they can work or not, for each day of the week;
    - A number of hours to work.
  * [`WORK_WEEK`](calendar.py); The amount of people required for the business to operate, for each day of the week.


## General idea

Each hour for which a worker is available is a variable, that can be evaluated to `0` (the worker will not work), or `1` (the worker will work).
Then, we can express the following:
  * A worker needs to work `n` hours: the sum of the variables corresponding to a given worker must equal to `n`;
  * Business needs `k` people on a certain timeslot (day and hour): the sum of the variables corresponding to this slot, across all the workers, must equal to `k`.

At the end, an set of values for these variables tells who works when.
