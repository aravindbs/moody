#!/bin/bash

cd web
gunicorn app:app -k gevent
