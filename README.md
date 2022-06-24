Steps to install (conda, preferred):
- brew install cmake coreutils
- conda env create -f environment.yml
- conda activate codex_pddl
- git clone https://github.com/ronuchit/pddlgym_planners into this repo.
- cd pddlgym_planners/FD; ./build.py release

Steps to install (pip):
- pip install openai
- pip install pddlgym
- submodule / clone: https://github.com/ronuchit/pddlgym_planners
- brew install cmake coreutils
