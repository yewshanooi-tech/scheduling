from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint, ConstraintCollectors)
from .domain import Assignment



@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        shift_conflict(constraint_factory),
        overlapping_shifts(constraint_factory)
    ]



def get_shift(a: Assignment) -> object:
    return a.shift

def get_shift_start(a: Assignment):
    if a.shift is not None and a.shift.start_time is not None:
        return a.shift.start_time.hour * 60 + a.shift.start_time.minute
    return None

def get_shift_end(a: Assignment):
    if a.shift is not None and a.shift.end_time is not None:
        return a.shift.end_time.hour * 60 + a.shift.end_time.minute
    return None

def get_florist(a: Assignment) -> object:
    return a.florist

def get_florist_name(a: Assignment) -> object:
    return a.florist.name



# HARD CONSTRAINTS

# A florist can work at most 1 shift at the same time.
def shift_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_shift),
                                  Joiners.equal(get_florist))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Shift conflict"))


# A florist cannot be assigned to overlapping shifts.
def overlapping_shifts(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(get_florist_name),
                                  Joiners.overlapping(get_shift_start, get_shift_end))
            .penalize(HardSoftScore.ONE_HARD, lambda a1, a2: 1)
            .as_constraint("Overlapping shift"))

