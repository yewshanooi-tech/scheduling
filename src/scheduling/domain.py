from timefold.solver.domain import (planning_entity, planning_solution, PlanningId, PlanningVariable,
                                    PlanningEntityCollectionProperty,
                                    ProblemFactCollectionProperty, ValueRangeProvider,
                                    PlanningScore)
from timefold.solver.score import HardSoftScore
from dataclasses import dataclass, field
from datetime import time
from typing import Annotated


@dataclass
class Florist:
    name: str
    level: str
    rest_day: str = ""

    def __str__(self):
        return f'{self.name} {self.level} {self.rest_day}'


@dataclass
class Team:
    name: str

    def __str__(self):
        return f'{self.name}'


@dataclass
class Shift:
    day_of_week: str
    start_time: time
    end_time: time

    def __str__(self):
        return f'{self.day_of_week} {self.start_time.strftime("%H:%M")} {self.end_time.strftime("%H:%M")}'


@planning_entity
@dataclass
class Assignment:
    id: Annotated[str, PlanningId]
    florist: Florist    # Referenced from Florist class
    team: Annotated[Team | None, PlanningVariable] = field(default=None)
    shift: Annotated[Shift | None, PlanningVariable] = field(default=None)

    def __str__(self):
        return f'{self.florist.name} {self.team.name if self.team else "None"} {self.shift.day_of_week if self.shift else "None"}'


@planning_solution
@dataclass
class Timetable:
    id: str
    florists: Annotated[list[Florist],
                        ProblemFactCollectionProperty,
                        ValueRangeProvider]
    teams: Annotated[list[Team],
                    ProblemFactCollectionProperty,
                    ValueRangeProvider]
    shifts: Annotated[list[Shift],
                         ProblemFactCollectionProperty,
                         ValueRangeProvider]
    assignments: Annotated[list[Assignment],
                       PlanningEntityCollectionProperty]
    score: Annotated[HardSoftScore, PlanningScore] = field(default=None)    # type: ignore[assignment]