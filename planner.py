from pddlgym_planners.fd import FD
from pddlgym_planners.planner import PlanningFailure, PlanningTimeout
from tempfile import NamedTemporaryFile

#  planner = FD(alias_flag='', final_flags='--search "astar(goalcount())"')
planner = FD(alias_flag='--alias "lama-first"')


def plan(domain_fname, problem_fname):
    global planner
    try:
        plan = planner.plan_from_pddl(domain_fname, problem_fname, timeout=2)
    except PlanningFailure as pf:
        return False, pf
    except PlanningTimeout as pt:
        print("timed out")
        return False, pt
    return True, plan


def attempt_domain(domain_str, problem_str):
    with NamedTemporaryFile(mode="w") as domain_file, NamedTemporaryFile(
        mode="w"
    ) as problem_file:
        domain_file.write(domain_str)
        problem_file.write(problem_str)
        domain_file.flush()
        problem_file.flush()
        success, out = plan(domain_file.name, problem_file.name)
        return (success, out)
