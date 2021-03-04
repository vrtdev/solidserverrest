* in a virtual env with a clone of the repo, install requirements
* install twine: ```pip install twine```
* change setup.py with appropriate version tag
* prepare package: ```python setup.py sdist bdist_wheel```
* push to pypi: ```twine upload dist/*```
