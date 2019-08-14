#!/bin/bash
function create_sock_file {
  touch /var/run/supervisor.sock
  chmod 777 /var/run/supervisor.sock
  service supervisor start || true
}

function run_application {
  supervisorctl reread
  supervisorctl update
  supervisorctl restart push_service
  supervisorctl status
}

function run_celery {
  supervisorctl start celery
}

function main {
  create_sock_file
  run_application
  run_celery
}

main $@
