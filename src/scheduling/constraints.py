from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint, ConstraintCollectors)
# from datetime import time
from typing import Optional

from .domain import Assignment



@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        florist_conflict(constraint_factory),
        team_conflict(constraint_factory),
        no_overlapping_shifts(constraint_factory)
    ]



def get_shift(a: Assignment) -> object:
    return a.shift

def get_shift_start(a: Assignment) -> Optional[int]:
    if a.shift is not None and a.shift.start_time is not None:
        return a.shift.start_time.hour * 60 + a.shift.start_time.minute
    return None

def get_shift_end(a: Assignment) -> Optional[int]:
    if a.shift is not None and a.shift.end_time is not None:
        return a.shift.end_time.hour * 60 + a.shift.end_time.minute
    return None


def get_florist(a: Assignment) -> object:
    return a.florist

def get_florist_name(a: Assignment) -> object:
    return a.florist.name



# A florist can work at most 1 shift at the same time.
def florist_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_shift),
                                  Joiners.equal(get_florist))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Florist conflict"))


# A team can accommodate at most 4 florists at the same time.
def team_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each(Assignment)
            .group_by(lambda a: (a.team, a.shift), ConstraintCollectors.count())
            .filter(lambda _, count: count > 4)
            .penalize(HardSoftScore.ONE_HARD, lambda _, count: count - 4)
            .as_constraint("Team capacity conflict"))


# A florist cannot be assigned to overlapping shifts.
def no_overlapping_shifts(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_florist_name),
                                  Joiners.overlapping(get_shift_start, get_shift_end))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Overlapping shift"))


