# txtaug -- Text Augmentation
Yet another text augmentation python package.

## Table of Contents
* Usage
* Appendix
    * [Installation](#installation)
    * [Commands](#commands)
    * [Support](#support)
    * [Contributing](#contributing)


# Usage

```py
import txtaug
import numpy as np
```

## Typographical Errors (Tippfehler)

### Swap two consecutive characters (Vertauscher)
A user mix two consecutive characters up.

- Swap 1st and 2nd characters: `typo_swap_consecutive("Kinder", loc=0)`  (Result: `iKnder`)
- Swap 1st and 2nd characters, and enforce letter cases: `typo_swap_consecutive("Kinder", loc=0, keep_case=True)`  (Result: `Iknder`)
- Swap random `i`-th and `i+1`-th characters that are more likely at the end of the word: `np.random.seed(seed=123); typo_swap_consecutive("Kinder", loc='end')`



# Appendix

## Installation
The `txtaug` [git repo](http://github.com/ulf1/txtaug) is available as [PyPi package](https://pypi.org/project/txtaug)

```
pip install txtaug>=0.1.0
```


## Commands
Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

## Support
Please [open an issue](https://github.com/ulf1/txtaug/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/txtaug/compare/).
