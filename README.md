# Django-Autogenerator

Generates a Django project with some sample HTML, CSS, and JavaScript placed inside the project directory.
This script can be modified to perform more advanced tasks.

### Requirements
- `django` (2.0.0 or later)
- `Python 3.6` (or later)
- `pip`
- `git`


### Installation
Start by cloning the repo.
```
git clone https://github.com/oleoneto/Django-Autogenerator.git
```

Give the script `generator.sh` permission to run.
```
cd Django-Autogenerator
chmod 755 generator.sh
```

### Usage

Specify the name of the project, followed by the name of each application you'd like to create inside your project. 
```
./generator.sh PROJECTNAME AppName1 AppName2
```

### Pull requests
Feel free to submit your contributions.

**Django Autogenerator** is [MIT Licensed](LICENSE).
