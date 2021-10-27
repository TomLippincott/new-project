# Basic pattern for a new research project

This repository is a basic template for how *I* structure a new research project.  It's essentially a build system, though the rules use a dummy script (just to demonstrate the ideas).

## Initializing and working with a new project

Run the following sequence of commands, with `${PROJECT_NAME}` replaced with whatever directory name you want to use for your project, and `${GIT_URL}` replaced with a new, empty Github repository URL:

```
git clone https://github.com/TomLippincott/new-project
mv new-project ${PROJECT_NAME}
cd ${PROJECT_NAME}
git remote remove origin
git remote add origin ${GIT_URL}
git push --set-upstream origin main
python3 -m venv local
source local/bin/activate
pip install -r requirements.txt
deactivate
```

The `${PROJECT_NAME}` directory is now an (empty) experiment, with version-control, environment, and dependency management.  To work on and run the experiment, you enter the environment by simply running:

```
cd ${PROJECT_NAME}
source local/bin/activate
```

Running Pip in this sandboxed environment will only have local effects, so e.g. dependencies from different projects won't clash.  After days/weeks/months of work, you can just close the terminal, or just leave the environment with:

```
deactivate
```

## How it works and common tasks

At a high level, the file `SConstruct` describes how to run your experiments, and the artifacts they produce: it's heavily commented, so read through it for details, and check out [the SCons documentation](https://scons.org/doc/production/HTML/scons-user/index.html).  For the moment, there are two important commands: a dry run of the build system:

```
scons -Q -n
```

The `-Q` switch just suppresses some non-informative output, while `-n` is the canonical dry-run flag for many UNIX tools.  This will print out all the commands that would be run, truncated to 100 characters.  If you add `OUTPUT_WIDTH=20000` after `-n`, you'll see the full commands.

Remove `-n` to *actually* run the build system:

```
scons -Q
```

The invocations should fly by very quickly (almost as fast as the dry run) because all the build rules are using the same dummy script that only touches the output files without doing anything meaningful: of course, you'll need to change this!  But try running it again and it should say:

```
scons: `.' is up to date.
```

If you look in the `work/` directory, you'll see all the files ("artifacts") it created.  Try deleting one of them, perhaps one of the "data.txt" files, and rerunning the build command.  It will again start invoking build rules, but only those necessary to reconstruct the portion of the dependency tree affected by the file you just deleted.

You shouldn't commit anything under `work/` to git: it's meant to be ephemeral, and the empirical results aren't an actual part of the experimental design.  But note how the build system defines the full dependency tree of operations for going from raw data to final results.  Well, actually, in this case the "experiment" starts with a dummy build rule that takes no inputs, but a real experiment would start with an unmodified data file under, say, `data/` (or pointed to via a variable in SConstruct), e.g. the PTB exactly as downloaded from the LDC.  The point is that it automatically documents the entire experiment, ensures replicability, gives you confidence that your comparisons are all even-handed, etc.

Moreover, there is a library called `steamroller` that can take an experiment defined in this fashion and automatically run it over our compute cluster, satisfying GPU requirements, and turning e.g. exhaustive grid-searches into a few minutes' wait.  We can get into that in the Fall, but the good news is you can design and write your experiments as shown in this repository, and very little modification will be needed to scale up massively.
