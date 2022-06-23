"""
main.py | Runs an interactive script to translate NL into PDDL.

SET_DOMAIN <domain_path>
SET_PROBLEM <problem_path>
CODEX_CONDITION <nl_string>
CODEX_QUERY <nl_string>
"""
import os

from time import sleep
from codex import *
from planner import *

SET_DEFAULTS = "SET_DEFAULTS"
SET_DOMAIN = "SET_DOMAIN"
SET_PROBLEM = "SET_PROBLEM"
CODEX_CONDITION = "CODEX_CONDITION"
CODEX_QUERY = "CODEX_QUERY"
DOMAINS_PREFIX = os.path.join(os.getcwd(), "domains")
GENERATED_PREFIX = os.path.join(os.getcwd(), "generated")


def get_input():
    raw_input = input("codex_pddl> ")
    command_type = raw_input.split()[0]
    command = " ".join(raw_input.split()[1:])
    return command_type, command


def load_pddl_from_file(pddl_file):
    # Sets PDDL domain or problem directly.
    with open(os.path.join(DOMAINS_PREFIX, pddl_file), "r") as f:
        pddl = f.read()
    return pddl


def create_prompt(predicates, objects, command_type, command):
    prompt = (
        "; Translate the following statements into PDDL.\n"
        + "; Statements that begin with SET_CONDITION should be turned into a single predicate.\n"
        + "; Statements that begin with SET_GOAL should be turned into a conjunction of predicates.\n"
        + "; Statements that begin with TRANSLATE_TO_NL should be turned back into natural language.\n"
        + "\n; These are the available predicates on this domain.\n"
    )
    prompt += predicates + "\n"
    prompt += "; These are the available objects in the domain.\n"
    prompt += objects + "\n"
    prompt += f"; {command_type} {command}\n"

    if command_type == CODEX_CONDITION:
        continuation = "(:init "
    elif command_type == CODEX_QUERY:
        continuation = "(:goal "
    else:
        continuation = "A natural language way to say this plan is that first, you "
    prompt += continuation
    return prompt


def set_domain(pddl_file):
    print(f"Setting domain from file: {pddl_file}")
    raw_pddl = load_pddl_from_file(pddl_file)
    split_pddl = raw_pddl.split(";")
    predicates = split_pddl[1]
    return raw_pddl, predicates


def set_problem(pddl_file):
    print(f"Setting problem from file: {pddl_file}")
    raw_pddl = load_pddl_from_file(pddl_file)
    split_pddl = raw_pddl.split(";")
    objects, initial_conditions, goal = split_pddl[1], split_pddl[2], split_pddl[3]
    return objects, initial_conditions, goal


def codex_condition(
    command_type, command, domain, predicates, objects, initial_conditions, goal
):
    # Conditioning statement through Codex.
    prompt = create_prompt(predicates, objects, command_type, command)
    completion = get_completion(prompt, temperature=0.0, stop="\n")
    assert completion[-1] == ")"
    condition = completion[:-1]
    print(f"CONDITION: {condition}")
    return condition


def build_problem(objects, initial_conditions, goal):
    problem = "(define (problem codexproblem) (:domain Codex)\n"
    problem += objects + "\n"
    problem += initial_conditions + "\n"
    problem += goal + "\n"
    problem += ")"
    return problem


def codex_query_and_plan(
    command_type,
    command,
    domain,
    predicates,
    objects,
    initial_conditions,
    initial_conditions_list,
    goal,
):
    prompt = create_prompt(predicates, objects, command_type, command)
    completion = get_completion(prompt, temperature=0.0, stop="\n")
    assert completion[-1] == ")"
    goal = "(:goal " + completion
    print(f"GOAL: {goal}")
    if len(initial_conditions_list) > 0:
        initial_conditions = "(:init\n" + "\n".join(initial_conditions_list) + ")"
    print(initial_conditions)
    # Write out the domain.
    print("Writing domain...")
    with open(os.path.join(GENERATED_PREFIX, "codex_domain.pddl"), "w") as f:
        domain = "(define (domain Codex)\n" + "\n".join(domain.split("\n")[1:])
        f.write(domain)
    # Write out problem.
    print("Writing problem...")
    with open(os.path.join(GENERATED_PREFIX, "codex_problem.pddl"), "w") as f:
        problem = build_problem(objects, initial_conditions, goal)
        problem = "".join([s for s in problem.strip().splitlines(True) if s.strip()])
        f.write(problem)
    print("Planning...")
    success, out = plan(
        os.path.join(GENERATED_PREFIX, "codex_domain.pddl"),
        os.path.join(GENERATED_PREFIX, "codex_problem.pddl"),
    )
    print(success, out)

    prompt = create_prompt(predicates, objects, command_type, out)
    completion = get_completion(prompt, temperature=0.0, stop="\n")
    print(completion)


def main():
    domain, predicates, objects, initial_conditions, goal = None, None, None, None, None
    initial_conditions_list = []
    while True:
        command_type, command = get_input()
        if command_type == SET_DEFAULTS:
            domain, predicates = set_domain("depots.pddl")
            objects, initial_conditions, goal = set_problem("depot_problems/p1.pddl")
            initial_conditions_list = []
        elif command_type == SET_DOMAIN:
            domain, predicates = set_domain(command)
            print(domain)
        elif command_type == SET_PROBLEM:
            objects, initial_conditions, goal = set_problem(command)
            initial_conditions_list = []
        elif command_type == CODEX_CONDITION:
            initial_condition = codex_condition(
                command_type,
                command,
                domain,
                predicates,
                objects,
                initial_conditions,
                goal,
            )
            initial_conditions_list.append(initial_condition)
        elif command_type == CODEX_QUERY:
            codex_query_and_plan(
                command_type,
                command,
                domain,
                predicates,
                objects,
                initial_conditions,
                initial_conditions_list,
                goal,
            )
        else:
            print(f"Unknown command type: {command_type}")


if __name__ == "__main__":
    main()

