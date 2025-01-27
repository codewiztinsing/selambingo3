#!/bin/bash
/root/selambingo3/venv/bin/gunicorn botbackend.wsgi:application --bind 0.0.0.0:8000
