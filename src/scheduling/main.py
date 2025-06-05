from timefold.solver.config import (SolverConfig, ScoreDirectorFactoryConfig,
                                    TerminationConfig, Duration)
from timefold.solver import SolverFactory
from enum import Enum
# from datetime import time
import logging
import argparse
import csv
from datetime import datetime

from .domain import *
from .constraints import define_constraints


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('app')


def main():
    parser = argparse.ArgumentParser(description='Solve a florist scheduling problem.')
    parser.add_argument('--input', dest='input_file', action='store',
                        default=None,
                        help='Path to external CSV file for timetable data')
    args = parser.parse_args()

    solver_factory = SolverFactory.create(
        SolverConfig(
            solution_class=Timetable,
            entity_class_list=[Assignment],
            score_director_factory_config=ScoreDirectorFactoryConfig(
                constraint_provider_function=define_constraints
            ),
            termination_config=TerminationConfig(
                # The solver runs only for 5 seconds on this small dataset.
                # It's recommended to run for at least 5 minutes (300) otherwise.
                spent_limit=Duration(seconds=5)
            )
        ))

    # Load the problem
    if args.input_file:
        problem = load_timetable_from_csv(args.input_file)
    else:
        raise ValueError("No file provided. Please use the --input flag to import a file.")

    # Solve the problem
    solver = solver_factory.build_solver()
    print("\n────────────────────\n")
    solution = solver.solve(problem)

    # Visualize the solution
    print("\n────────────────────\n")
    print_timetable(solution)
    print("\n────────────────────\n")





def load_timetable_from_csv(csv_path: str) -> Timetable:
    # CSV columns: florist_name,start_time,end_time
    assignments = []
    shift_set = set()
    florist_map = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            florist_name = row['florist_name']
            if florist_name not in florist_map:
                florist_map[florist_name] = Florist(florist_name)
            start_time = datetime.strptime(row['start_time'], '%H:%M').time()
            end_time = datetime.strptime(row['end_time'], '%H:%M').time()
            assignments.append((florist_name, start_time, end_time))
            shift_set.add((start_time, end_time))

    def shift_sort_key(x):
        start, end = x
        return (start, end)

    shifts = [Shift(start, end) for (start, end) in sorted(shift_set, key=shift_sort_key)]
    shift_map = {(s.start_time, s.end_time): s for s in shifts}
    def id_generator():
        current = 0
        while True:
            yield str(current)
            current += 1
    ids = id_generator()
    assignment_objs = []
    for florist_name, start, end in assignments:
        assignment_objs.append(Assignment(
            next(ids),
            florist_map[florist_name],
            shift=shift_map[(start, end)]
        ))
    return Timetable('EXTERNAL', list(florist_map.values()), shifts, assignment_objs)





def print_timetable(timetable: Timetable) -> None:
    column_width = 18
    shifts = timetable.shifts
    assignments = timetable.assignments
    assignment_map = {
        (assignment.shift.start_time if assignment.shift else '',): assignment
        for assignment in assignments
        if assignment.shift is not None
    }
    row_format = ("|{:<" + str(column_width) + "}") * 2 + "|"
    sep_format = "+" + (("-" * column_width + "+") * 2)

    LOGGER.info(sep_format)
    LOGGER.info(row_format.format('', 'Florist'))
    LOGGER.info(sep_format)

    for shift in shifts:
        florist_name = ''
        for assignment in assignments:
            if assignment.shift and assignment.shift.start_time == shift.start_time and assignment.shift.end_time == shift.end_time:
                florist_name = assignment.florist.name
                break
        LOGGER.info(row_format.format(f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')}", florist_name))
        LOGGER.info(sep_format)

    unassigned = [a for a in assignments if a.shift is None]
    if len(unassigned) > 0:
        LOGGER.info("")
        LOGGER.info("Unassigned assignments")
        for a in unassigned:
            LOGGER.info(f'    {a.florist.name}')





if __name__ == '__main__':
    main()