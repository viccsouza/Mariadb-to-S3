#!/bin/bash

sleep 20 && mysqldump --column-statistics=0 -hdb -uroot -pcesar FACULDADE > /dumps/dump.sql
