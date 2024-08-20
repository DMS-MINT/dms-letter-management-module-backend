#!/bin/bash
echo "--> Starting beats process"
celery -A core.tasks worker -l info --without-gossip --without-mingle --without-heartbeat