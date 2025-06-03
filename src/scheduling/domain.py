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

    def __str__(self):
        return f'{self.name}'


@dataclass
class Shift:
    start_time: time
    end_time: time

    def __str__(self):
        return f'{self.start_time.strftime("%H:%M")} {self.end_time.strftime("%H:%M")}'


@planning_entity
@dataclass
class Assignment:
    id: Annotated[str, PlanningId]
    florist: Florist
    shift: Annotated[Shift | None, PlanningVariable] = field(default=None)

    def __str__(self):
        return f'{self.florist.name} {self.shift.start_time.strftime("%H:%M") if self.shift else "None"}'


@planning_solution
@dataclass
class Timetable:
    id: str
    florists: Annotated[list[Florist],
                        ProblemFactCollectionProperty,
                        ValueRangeProvider]
    shifts: Annotated[list[Shift],
                         ProblemFactCollectionProperty,
                         ValueRangeProvider]
    assignments: Annotated[list[Assignment],
                       PlanningEntityCollectionProperty]
    score: Annotated[HardSoftScore, PlanningScore] = field(default=None)    # type: ignore[assignment]