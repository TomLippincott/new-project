# Basic pattern for a new research project

This repository is essentially a template for how *I* structure a new project.  It's a build system, but the rules use a dummy script (just to demonstrate the idea).

## Initializing and working with a new project

The following sequence:

```
git clone https://github.com/TomLippincott/new-project
mv new-project ${PROJECT_NAME}
cd ${PROJECT_NAME}
git remote remove origin
git remote add origin ${GIT_URL}
git push --set-upstream origin main
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

The `${PROJECT_NAME}` directory is now an (empty) experiment, with version-control, environment, and dependency management.  To work on and run the experiment, you simply run:

```
cd ${PROJECT_NAME}
source venv/bin/activate
```

After days/weeks/months of work, you can just close the terminal, or just leave the environment with:

```
deactivate
```

## Common tasks

Dry run of the build system:

```
scons -Qn
```

Actually run the build system:

```
scons -Q
```
