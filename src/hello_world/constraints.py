from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint, ConstraintCollectors)
# from datetime import time

from .domain import Assignment



@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        florist_conflict(constraint_factory),
        team_conflict(constraint_factory)
    ]


def get_shift(a: Assignment) -> object:
    return a.shift


def get_florist(a: Assignment) -> object:
    return a.florist



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


