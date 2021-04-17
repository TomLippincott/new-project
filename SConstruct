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

# actual variable and environment objects
vars = Variables("custom.py")
vars.AddVariables(
    ("OUTPUT_WIDTH", "", 120),
    ("MODEL_TYPES", "", ["mlp", "cnn", "rnn"]),
    ("DATASETS", "", ["A", "B", "C"]),
    ("FOLDS", "", 5),
)

env = Environment(variables=vars, ENV=os.environ, TARFLAGS="-c -z", TARSUFFIX=".tgz",
                  tools=["default"],
)

env.Append(
    BUILDERS={
        "CreateData" : Builder(
            action="python scripts/dummy.py --outputs ${TARGETS[0]}"
        ),
        "ShuffleData" : Builder(
            action="python scripts/dummy.py --dataset ${SOURCES[0]} --outputs ${TARGETS}"
        ),
        "TrainModel" : Builder(
            action="python scripts/dummy.py model_type${MODEL_TYPE} --train ${SOURCES[0]} --dev ${SOURCES[0]} --outputs ${TARGETS[0]}"
        ),
        "ApplyModel" : Builder(
            action="python scripts/dummy.py --model ${SOURCES[0]} --test ${SOURCES[0]} --outputs ${TARGETS[0]}"
        ),
        "GenerateReport" : Builder(
            action="python scripts/dummy.py --experimental_results ${SOURCES} --outputs ${TARGETS[0]}"
        ),
    }
)

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

#
for dataset in env["DATASETS"]:
    env.CreateData("work/${DATASET}.txt", [], DATASET=dataset)

# run all combinations
results = []
for fold in range(1, env["FOLDS"] + 1):
    for train_data in env["DATASETS"]:
        train, dev = env.ShuffleData(
            [
                "work/${FOLD}/${TRAIN_DATA}/train.txt",
                "work/${FOLD}/${TRAIN_DATA}/dev.txt"
            ],
            "work/${TRAIN_DATA}.txt",
            FOLD=fold,
            TRAIN_DATA=train_data,
        )
        for model_type in env["MODEL_TYPES"]:
            model = env.TrainModel(
                "work/${FOLD}/${TRAIN_DATA}/${MODEL_TYPE}.bin",
                [train, dev],
                FOLD=fold,
                TRAIN_DATA=train_data,
                MODEL_TYPE=model_type,
            )
            for test_data in env["DATASETS"]:
                results.append(
                    env.ApplyModel(
                        "work/${FOLD}/${TRAIN_DATA}/${MODEL_TYPE}/${TEST_DATA}.out",
                        [model, "work/${TEST_DATA}.txt"],
                        FOLD=fold,
                        TRAIN_DATA=train_data,
                        MODEL_TYPE=model_type,
                        TEST_DATA=test_data,
                    )
                )

report = env.GenerateReport(
    "work/report.txt",
    results
)
