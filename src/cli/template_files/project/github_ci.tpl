name: Django CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      max-parallel: 4
      matrix:
        python-version: [3.7, 3.8, 3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python {% raw %}${{ matrix.python-version }}{% endraw %}
      uses: actions/setup-python@v2
      with:
        python-version: {% raw %}${{ matrix.python-version }}{% endraw %}
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Tests
      run: |
        python manage.py test
