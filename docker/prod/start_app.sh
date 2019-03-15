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

function main {
  create_sock_file
  run_application
}

main $@
