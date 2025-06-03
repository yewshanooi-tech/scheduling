from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint, ConstraintCollectors)
# from datetime import time
from typing import Optional

from .domain import Assignment, Team



@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        shift_conflict(constraint_factory),
        team_capacity(constraint_factory),
        overlapping_shifts(constraint_factory),
        same_shift_team(constraint_factory),

        # Soft constraints
        rest_days(constraint_factory)
    ]



# GETTERS

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

def get_team(a: Assignment) -> object:
    return a.team



# HARD CONSTRAINTS

# A florist can work at most 1 shift at the same time.
def shift_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_shift),
                                  Joiners.equal(get_florist))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Shift conflict"))


# A team can accommodate at most 4 florists at the same time.
def team_capacity(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each(Assignment)
            .group_by(lambda a: (a.team, a.shift), ConstraintCollectors.count())
            .filter(lambda _, count: count > 4)
            .penalize(HardSoftScore.ONE_HARD, lambda _, count: count - 4)
            .as_constraint("Team capacity"))


# A florist cannot be assigned to overlapping shifts.
def overlapping_shifts(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_florist_name),
                                  Joiners.overlapping(get_shift_start, get_shift_end))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Overlapping shift"))


# 2 different florists from the same team cannot work the same shift.
def same_shift_team(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_team),
                                  Joiners.equal(get_shift))
            .filter(lambda a1, a2: a1.florist != a2.florist)
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Same shift same team"))



# SOFT CONSTRAINTS

# Florist rest day should be respected.
def rest_days(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each(Assignment)
            .filter(lambda a: a.florist.rest_days is not None and a.shift is not None and a.shift.day_of_week.upper() in [d.upper() for d in a.florist.rest_days])
            .penalize(HardSoftScore.ONE_SOFT, lambda a: 1)
            .as_constraint("Florist rest day"))


