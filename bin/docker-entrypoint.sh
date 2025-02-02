#!/bin/sh -e

hostname=$(hostname -f)

case "$1" in
    django)
        echo "Run: $CONTAINER_ENVIRONMENT"
        echo "Application: django"
        log_dir="/var/log/django"
        mkdir -p "${log_dir}"
        access_logfile="${log_dir}/django-access.log"
        error_logfile="${log_dir}/django-error.log"
        echo "Skipping collectstatic&migrations"
        python manage.py runserver 0.0.0.0:8000
        ;;
    dramatiq)
        echo "Application: Dramatiq"
        log_dir="/var/log/dramatiq"
        mkdir -p "${log_dir}"
        exec python manage.py rundramatiq \
            --queues default \
            --processes 3 \
            --threads 3 \
            --use-gevent \
            -v 2 \
            --log-file=${log_dir}/dramatiq.log
        ;;
    *)
        exec "$@"
        ;;
esac