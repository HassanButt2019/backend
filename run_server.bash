#!/bin/bash
# call from within Docker to setup database and run server.
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTPATH/ && python3 
cd $SCRIPTPATH/ && python3 -m uvicorn 
