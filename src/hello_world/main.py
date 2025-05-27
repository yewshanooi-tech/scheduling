from timefold.solver.config import (SolverConfig, ScoreDirectorFactoryConfig,
                                    TerminationConfig, Duration)
from timefold.solver import SolverFactory
from enum import Enum
from datetime import time
import logging
import argparse
import csv
from datetime import datetime

from .domain import *
from .constraints import define_constraints


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('app')


def main():
    parser = argparse.ArgumentParser(description='Solve a school timetable.')
    parser.add_argument('--demo_data', dest='demo_data', action='store',
                        choices=['SMALL', 'LARGE'],
                        default='SMALL',
                        help='Demo dataset to use')
    # Input file parameter - START
    parser.add_argument('--input_file', dest='input_file', action='store',
                        default=None,
                        help='Path to external CSV file for timetable data')
    # Input file parameter - END
    args = parser.parse_args()

    solver_factory = SolverFactory.create(
        SolverConfig(
            solution_class=Timetable,
            entity_class_list=[Lesson],
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
        demo_data = getattr(DemoData, args.demo_data)
        problem = generate_demo_data(demo_data)

    # Solve the problem
    solver = solver_factory.build_solver()
    solution = solver.solve(problem)

    # Visualize the solution
    print_timetable(solution)


def generate_demo_data(demo_data: 'DemoData') -> Timetable:
    days = (('MONDAY', 'TUESDAY') if demo_data == DemoData.SMALL
            else ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'))
    timeslots = [
        Timeslot(day, start, start.replace(hour=start.hour + 1))
        for day in days
        for start in (time(8, 30), time(9, 30), time(10, 30), time(13, 30), time(14, 30))
    ]

    room_ids = (('A', 'B', 'C') if demo_data == DemoData.SMALL
                else ('A', 'B', 'C', 'D', 'E', 'F'))
    rooms = [Room(f'Room {name}') for name in room_ids]

    lessons = []

    def id_generator():
        current = 0
        while True:
            yield str(current)
            current += 1

    ids = id_generator()
    lessons.append(Lesson(next(ids), "Math", "A. Turing", "9th grade"))
    lessons.append(Lesson(next(ids), "Math", "A. Turing", "9th grade"))
    lessons.append(Lesson(next(ids), "Physics", "M. Curie", "9th grade"))
    lessons.append(Lesson(next(ids), "Chemistry", "M. Curie", "9th grade"))
    lessons.append(Lesson(next(ids), "Biology", "C. Darwin", "9th grade"))
    lessons.append(Lesson(next(ids), "History", "I. Jones", "9th grade"))
    lessons.append(Lesson(next(ids), "English", "I. Jones", "9th grade"))
    lessons.append(Lesson(next(ids), "English", "I. Jones", "9th grade"))
    lessons.append(Lesson(next(ids), "Spanish", "P. Cruz", "9th grade"))
    lessons.append(Lesson(next(ids), "Spanish", "P. Cruz", "9th grade"))
    if demo_data == DemoData.LARGE:
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "9th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "9th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "9th grade"))
        lessons.append(Lesson(next(ids), "ICT", "A. Turing", "9th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "9th grade"))
        lessons.append(Lesson(next(ids), "Geography", "C. Darwin", "9th grade"))
        lessons.append(Lesson(next(ids), "Geology", "C. Darwin", "9th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "9th grade"))
        lessons.append(Lesson(next(ids), "English", "I. Jones", "9th grade"))
        lessons.append(Lesson(next(ids), "Drama", "I. Jones", "9th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "9th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "9th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "9th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "9th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "9th grade"))

    lessons.append(Lesson(next(ids), "Math", "A. Turing", "10th grade"))
    lessons.append(Lesson(next(ids), "Math", "A. Turing", "10th grade"))
    lessons.append(Lesson(next(ids), "Math", "A. Turing", "10th grade"))
    lessons.append(Lesson(next(ids), "Physics", "M. Curie", "10th grade"))
    lessons.append(Lesson(next(ids), "Chemistry", "M. Curie", "10th grade"))
    lessons.append(Lesson(next(ids), "French", "M. Curie", "10th grade"))
    lessons.append(Lesson(next(ids), "Geography", "C. Darwin", "10th grade"))
    lessons.append(Lesson(next(ids), "History", "I. Jones", "10th grade"))
    lessons.append(Lesson(next(ids), "English", "P. Cruz", "10th grade"))
    lessons.append(Lesson(next(ids), "Spanish", "P. Cruz", "10th grade"))
    if demo_data == DemoData.LARGE:
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "10th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "10th grade"))
        lessons.append(Lesson(next(ids), "ICT", "A. Turing", "10th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "10th grade"))
        lessons.append(Lesson(next(ids), "Biology", "C. Darwin", "10th grade"))
        lessons.append(Lesson(next(ids), "Geology", "C. Darwin", "10th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "10th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "10th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "10th grade"))
        lessons.append(Lesson(next(ids), "Drama", "I. Jones", "10th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "10th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "10th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "10th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "10th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "10th grade"))
    
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "ICT", "A. Turing", "11th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "11th grade"))
        lessons.append(Lesson(next(ids), "Chemistry", "M. Curie", "11th grade"))
        lessons.append(Lesson(next(ids), "French", "M. Curie", "11th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "11th grade"))
        lessons.append(Lesson(next(ids), "Geography", "C. Darwin", "11th grade"))
        lessons.append(Lesson(next(ids), "Biology", "C. Darwin", "11th grade"))
        lessons.append(Lesson(next(ids), "Geology", "C. Darwin", "11th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "11th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "11th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "11th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "11th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "11th grade"))
        lessons.append(Lesson(next(ids), "Spanish", "P. Cruz", "11th grade"))
        lessons.append(Lesson(next(ids), "Drama", "P. Cruz", "11th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "11th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "11th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "11th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "11th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "11th grade"))
    
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "Math", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "ICT", "A. Turing", "12th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "12th grade"))
        lessons.append(Lesson(next(ids), "Chemistry", "M. Curie", "12th grade"))
        lessons.append(Lesson(next(ids), "French", "M. Curie", "12th grade"))
        lessons.append(Lesson(next(ids), "Physics", "M. Curie", "12th grade"))
        lessons.append(Lesson(next(ids), "Geography", "C. Darwin", "12th grade"))
        lessons.append(Lesson(next(ids), "Biology", "C. Darwin", "12th grade"))
        lessons.append(Lesson(next(ids), "Geology", "C. Darwin", "12th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "12th grade"))
        lessons.append(Lesson(next(ids), "History", "I. Jones", "12th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "12th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "12th grade"))
        lessons.append(Lesson(next(ids), "English", "P. Cruz", "12th grade"))
        lessons.append(Lesson(next(ids), "Spanish", "P. Cruz", "12th grade"))
        lessons.append(Lesson(next(ids), "Drama", "P. Cruz", "12th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "12th grade"))
        lessons.append(Lesson(next(ids), "Art", "S. Dali", "12th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "12th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "12th grade"))
        lessons.append(Lesson(next(ids), "Physical education", "C. Lewis", "12th grade"))

    return Timetable(demo_data.name, timeslots, rooms, lessons)



# Load timetable from CSV - START

def load_timetable_from_csv(csv_path: str) -> Timetable:
    # Example CSV columns: subject,teacher,student_group,day_of_week,start_time,end_time,room
    lessons = []
    timeslot_set = set()
    room_set = set()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subject = row['subject']
            teacher = row['teacher']
            student_group = row['student_group']
            day_of_week = row['day_of_week']
            start_time = datetime.strptime(row['start_time'], '%H:%M').time()
            end_time = datetime.strptime(row['end_time'], '%H:%M').time()
            room_name = row['room']
            timeslot_set.add((day_of_week, start_time, end_time))
            room_set.add(room_name)
            lessons.append((subject, teacher, student_group, day_of_week, start_time, end_time, room_name))


    # Define the correct weekday order - START
    
    weekday_order = {'MONDAY': 0, 'TUESDAY': 1, 'WEDNESDAY': 2, 'THURSDAY': 3, 'FRIDAY': 4, 'SATURDAY': 5, 'SUNDAY': 6}
    def timeslot_sort_key(x):
        day, start, end = x
        return (weekday_order.get(day.upper(), 99), start, end)
    timeslots = [Timeslot(day, start, end) for (day, start, end) in sorted(timeslot_set, key=timeslot_sort_key)]
    
    # Define the correct weekday order - START

    rooms = [Room(f'Room {name}') for name in sorted(room_set)]
    timeslot_map = {(t.day_of_week, t.start_time, t.end_time): t for t in timeslots}
    room_map = {r.name.replace('Room ', ''): r for r in rooms}
    def id_generator():
        current = 0
        while True:
            yield str(current)
            current += 1
    ids = id_generator()
    lesson_objs = []
    for subject, teacher, student_group, day, start, end, room_name in lessons:
        lesson_objs.append(Lesson(next(ids), subject, teacher, student_group,
                                 timeslot=timeslot_map[(day, start, end)],
                                 room=room_map[room_name]))
    return Timetable('EXTERNAL', timeslots, rooms, lesson_objs)

# Load timetable from CSV - END



def print_timetable(time_table: Timetable) -> None:
    LOGGER.info("")

    column_width = 18
    rooms = time_table.rooms
    timeslots = time_table.timeslots
    lessons = time_table.lessons
    lesson_map = {
        (lesson.room.name, lesson.timeslot.day_of_week, lesson.timeslot.start_time): lesson
        for lesson in lessons
        if lesson.room is not None and lesson.timeslot is not None
    }
    row_format = ("|{:<" + str(column_width) + "}") * (len(rooms) + 1) + "|"
    sep_format = "+" + ((("-" * column_width) + "+") * (len(rooms) + 1))

    LOGGER.info(sep_format)
    LOGGER.info(row_format.format('', *[room.name for room in rooms]))
    LOGGER.info(sep_format)

    for timeslot in timeslots:
        def get_row_lessons():
            for room in rooms:
                yield lesson_map.get((room.name, timeslot.day_of_week, timeslot.start_time),
                                     Lesson('', '', '', ''))

        row_lessons = [*get_row_lessons()]
        LOGGER.info(row_format.format(str(timeslot), *[lesson.subject for lesson in row_lessons]))
        LOGGER.info(row_format.format('', *[lesson.teacher for lesson in row_lessons]))
        LOGGER.info(row_format.format('', *[lesson.student_group for lesson in row_lessons]))
        LOGGER.info(sep_format)

    unassigned_lessons = [lesson for lesson in lessons if lesson.room is None or lesson.timeslot is None]
    if len(unassigned_lessons) > 0:
        LOGGER.info("")
        LOGGER.info("Unassigned lessons")
        for lesson in unassigned_lessons:
            LOGGER.info(f'    {lesson.subject} - {lesson.teacher} - {lesson.student_group}')


class DemoData(Enum):
    SMALL = 'SMALL'
    LARGE = 'LARGE'


if __name__ == '__main__':
    main()