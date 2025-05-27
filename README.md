# Scheduling

A simple scheduling system for Florists.


## Installation

1. Create a Python virtual environment

```bash
  python -m venv .venv
```

2. Activate the virtual environment

```bash
  .venv\Scripts\Activate.ps1
```

3. Install required packages

```bash
  pip install -e .
```

4. Run the app using `--input_file` flag with a .csv file

```bash
  run-app --input_file my_timetable.csv
```


## Export

Generate a list of currently installed packages

```bash
  pip freeze > requirements.txt
```

Install required packages based on exported file

```bash
  pip install -r requirements.txt
```


## Others

```bash
  uvicorn app.main:app --reload
```