#!/bin/bash

export FLASK_APP="run.py"
flask db migrate
flask db upgrade
