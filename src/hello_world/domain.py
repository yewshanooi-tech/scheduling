from timefold.solver.domain import (planning_entity, planning_solution, PlanningId, PlanningVariable,
                                    PlanningEntityCollectionProperty,
                                    ProblemFactCollectionProperty, ValueRangeProvider,
                                    PlanningScore)
from timefold.solver.score import HardSoftScore
from dataclasses import dataclass, field
from datetime import time
from typing import Annotated


@dataclass
class Shift:
    day_of_week: str
    start_time: time
    end_time: time
    # min_staff_required: int

    def __str__(self):
        return f'{self.day_of_week} {self.start_time.strftime("%H:%M")}'


@dataclass
class Team:
    name: str
    # lead: str
    # acting_lead: str
    # members: str

    def __str__(self):
        return f'{self.name}'


@planning_entity
@dataclass
class Assignment:
    id: Annotated[str, PlanningId]
    florist: str
    skill_level: str
    tenure_months: int
    shift: Annotated[Shift | None, PlanningVariable] = field(default=None)
    team: Annotated[Team | None, PlanningVariable] = field(default=None)


@planning_solution
@dataclass
class Timetable:
    id: str
    shifts: Annotated[list[Shift],
                         ProblemFactCollectionProperty,
                         ValueRangeProvider]
    teams: Annotated[list[Team],
                     ProblemFactCollectionProperty,
                     ValueRangeProvider]
    assignments: Annotated[list[Assignment],
                       PlanningEntityCollectionProperty]
    score: Annotated[HardSoftScore, PlanningScore] = field(default=None)  # type: ignore[assignment]