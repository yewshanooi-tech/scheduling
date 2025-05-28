from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint)
from datetime import time

from .domain import Assignment


@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        florist_conflict(constraint_factory)
    ]


def florist_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    # A florist can work at most one shift at the same time.
    return (constraint_factory
            .for_each_unique_pair(Assignment,
                                  Joiners.equal(lambda a: a.shift),
                                  Joiners.equal(lambda a: a.florist))
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Florist conflict"))

