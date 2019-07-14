#!/bin/bash

cd /opt/CZN/run

gunicorn -w 3 -b 127.0.0.1:7000 api:app
