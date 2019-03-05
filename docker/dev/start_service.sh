#!/usr/bin/env bash

function create_sock_file {
  touch /var/run/supervisor.sock
  chmod 777 /var/run/supervisor.sock
  service supervisor start
}

function run_application {
  supervisorctl start micro_service
}

function main {
  create_sock_file
  run_application
}

main $@
