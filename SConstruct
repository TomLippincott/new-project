import os
import os.path
import logging
import random
import subprocess
import shlex
import gzip
import re
import functools
import time
import imp
import sys
import json

# workaround needed to fix bug with SCons and the pickle module
del sys.modules['pickle']
sys.modules['pickle'] = imp.load_module('pickle', *imp.find_module('pickle'))
import pickle

# Variables control various aspects of the experiment.  Note that you have to declare
# any variables you want to use here, with reasonable default values, but when you want
# to change/override the default values, do so in the "custom.py" file (see it for an
# example, changing the number of folds).
vars = Variables("custom.py")
vars.AddVariables(
    ("OUTPUT_WIDTH", "", 100),
    ("MODEL_TYPES", "", ["mlp", "cnn", "rnn"]),
    ("PARAMETER_VALUES", "", [0.1, 0.5, 0.9]),
    ("DATASETS", "", ["A", "B", "C"]),
    ("FOLDS", "", 10),
)

# Methods on the environment object are used all over the place, but it mostly serves to
# manage the variables (see above) and builders (see below).
env = Environment(variables=vars, ENV=os.environ, TARFLAGS="-c -z", TARSUFFIX=".tgz",
                  tools=["default"],
)

# Defining a bunch of builders (none of these do anything except "touch" their targets,
# as you can see in the dummy.py script).  Consider in particular the "TrainModel" builder,
# which interpolates two variables beyond the standard SOURCES/TARGETS: PARAMETER_VALUE
# and MODEL_TYPE.  When we invoke the TrainModel builder (see below), we'll need to pass
# in values for these (note that e.g. the existence of a MODEL_TYPES variable above doesn't
# automatically populate MODEL_TYPE, we'll do this with for-loops).
env.Append(
    BUILDERS={
        "CreateData" : Builder(
            action="python scripts/dummy.py createdata --outputs ${TARGETS[0]}"
        ),
        "ShuffleData" : Builder(
            action="python scripts/dummy.py shuffledata --dataset ${SOURCES[0]} --outputs ${TARGETS}"
        ),
        "TrainModel" : Builder(
            action="python scripts/dummy.py trainmodel --parameter_value ${PARAMETER_VALUE} --model_type ${MODEL_TYPE} --train ${SOURCES[0]} --dev ${SOURCES[0]} --outputs ${TARGETS[0]}"
        ),
        "ApplyModel" : Builder(
            action="python scripts/dummy.py applymodel --model ${SOURCES[0]} --test ${SOURCES[1]} --outputs ${TARGETS[0]}"
        ),
        "GenerateReport" : Builder(
            action="python scripts/dummy.py generatereport --experimental_results ${SOURCES} --outputs ${TARGETS[0]}"
        ),
    }
)

# You can ignore the next three items, they simply make the output a bit more readable and
# the dependency-tracking a bit faster:

# function for width-aware printing of commands
def print_cmd_line(s, target, source, env):
    if len(s) > int(env["OUTPUT_WIDTH"]):
        print(s[:int(float(env["OUTPUT_WIDTH"]) / 2) - 2] + "..." + s[-int(float(env["OUTPUT_WIDTH"]) / 2) + 1:])
    else:
        print(s)

# and the command-printing function
env['PRINT_CMD_LINE_FUNC'] = print_cmd_line

# and how we decide if a dependency is out of date
env.Decider("timestamp-newer")


# OK, at this point we have defined all the builders and variables, so it's
# time to specify the actual experiments by iterating over some of the variables:

# Run all combinations of datasets, folds, model types, and parameter values, collecting
# the build artifacts from applying the models to test data in a list.
#
# The basic pattern for using a build rule is:
#
#   "Rule(list_of_targets, list_of_sources, VARIABLE1=value, VARIABLE2=value...)"
#
# Variables that are defined at the top of this file will get used automatically (e.g.
# "${OUTPUT_WIDTH}" would get replaced with "100"), but note how arbitrary other variables
# can also be specified locally, and how this functionality is used to populate the build
# commands *and* determine output filenames.  It's a very flexible system, and there are
# surely lots of other ways to accomplish this!
results = []
for dataset_name in env["DATASETS"]:
    data = env.CreateData("work/${DATASET_NAME}/data.txt", [], DATASET_NAME=dataset_name)
    for fold in range(1, env["FOLDS"] + 1):
        train, dev, test = env.ShuffleData(
            [
                "work/${DATASET_NAME}/${FOLD}/train.txt",
                "work/${DATASET_NAME}/${FOLD}/dev.txt",
                "work/${DATASET_NAME}/${FOLD}/test.txt",
            ],
            data,
            FOLD=fold,
            DATASET_NAME=dataset_name,
        )
        for model_type in env["MODEL_TYPES"]:
            for parameter_value in env["PARAMETER_VALUES"]:
                model = env.TrainModel(
                    "work/${DATASET_NAME}/${FOLD}/${MODEL_TYPE}/${PARAMETER_VALUE}/model.bin",
                    [train, dev],
                    FOLD=fold,
                    DATASET_NAME=dataset_name,
                    MODEL_TYPE=model_type,
                    PARAMETER_VALUE=parameter_value,
                )
                results.append(
                    env.ApplyModel(
                        "work/${DATASET_NAME}/${FOLD}/${MODEL_TYPE}/${PARAMETER_VALUE}/applied.txt",
                        [model, test],
                        FOLD=fold,
                        DATASET_NAME=dataset_name,
                        MODEL_TYPE=model_type,
                        PARAMETER_VALUE=parameter_value,                        
                    )
                )

# Use the list of applied model outputs to generate an evaluation report (table, plot,
# f-score, confusion matrix, whatever makes sense).
report = env.GenerateReport(
    "work/report.txt",
    results
)
