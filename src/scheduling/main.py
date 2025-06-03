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
    # CSV columns: florist_name,level,team,day_of_week,start_time,end_time,rest_day
    assignments = []
    shift_set = set()
    team_set = set()
    florist_map = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            florist_name = row['florist_name']
            level = row['level']
            team_name = row['team']
            rest_day = row.get('rest_day', '') or ''
            if florist_name not in florist_map:
                florist_map[florist_name] = Florist(florist_name, level, rest_day)
            day_of_week = row['day_of_week']
            start_time = datetime.strptime(row['start_time'], '%H:%M').time()
            end_time = datetime.strptime(row['end_time'], '%H:%M').time()
            assignments.append((florist_name, day_of_week, start_time, end_time, team_name))
            shift_set.add((day_of_week, start_time, end_time))
            team_set.add(team_name)


    # Define the correct weekday order
    day_order = {'MONDAY': 0, 'TUESDAY': 1, 'WEDNESDAY': 2, 'THURSDAY': 3, 'FRIDAY': 4, 'SATURDAY': 5, 'SUNDAY': 6}
    def shift_sort_key(x):
        day, start, end = x
        return (day_order.get(day.upper(), 99), start, end)

    shifts = [Shift(day, start, end) for (day, start, end) in sorted(shift_set, key=shift_sort_key)]
    teams = [Team(name) for name in sorted(team_set)]

    shift_map = {(s.day_of_week, s.start_time, s.end_time): s for s in shifts}
    team_map = {t.name: t for t in teams}
    def id_generator():
        current = 0
        while True:
            yield str(current)
            current += 1
    ids = id_generator()
    assignment_objs = []
    for florist_name, day, start, end, team_name in assignments:
        assignment_objs.append(Assignment(
            next(ids),
            florist_map[florist_name],
            shift=shift_map[(day, start, end)],
            team=team_map[team_name]
        ))
    return Timetable('EXTERNAL', list(florist_map.values()), teams, shifts, assignment_objs)





def print_timetable(timetable: Timetable) -> None:
    column_width = 18
    teams = timetable.teams
    shifts = timetable.shifts
    assignments = timetable.assignments
    assignment_map = {
        (assignment.team.name if assignment.team else '',
         assignment.shift.day_of_week if assignment.shift else '',
         assignment.shift.start_time if assignment.shift else ''): assignment
        for assignment in assignments
        if assignment.team is not None and assignment.shift is not None
    }
    row_format = ("|{:<" + str(column_width) + "}") * (len(teams) + 1) + "|"
    sep_format = "+" + (("-" * column_width + "+") * (len(teams) + 1))

    LOGGER.info(sep_format)
    LOGGER.info(row_format.format('', *[f'Team {team.name}' for team in teams]))
    LOGGER.info(sep_format)

    for shift in shifts:
        def get_row_assignments():
            for team in teams:
                yield Assignment(
                    id='',
                    florist=Florist('', '', ''),
                    team=team,
                    shift=shift
                ) if (team.name, shift.day_of_week, shift.start_time) not in assignment_map else assignment_map[(team.name, shift.day_of_week, shift.start_time)]

        row_assignments = [*get_row_assignments()]

        def get_florist_display(a, team):
            return a.florist.name

        LOGGER.info(row_format.format(shift.day_of_week, *[get_florist_display(a, a.team) if a.team else a.florist.name for a in row_assignments]))
        LOGGER.info(row_format.format(f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')}", *[a.florist.level for a in row_assignments]))
        LOGGER.info(sep_format)

    unassigned = [a for a in assignments if a.team is None or a.shift is None]
    if len(unassigned) > 0:
        LOGGER.info("")
        LOGGER.info("Unassigned assignments")
        for a in unassigned:
            LOGGER.info(f'    {a.florist.name} - {a.florist.level}')





if __name__ == '__main__':
    main()