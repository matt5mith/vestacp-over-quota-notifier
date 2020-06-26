# VestaCP Over Quota Notifier
This script is designed to work with VestaCP and send out email alerts when mail accounts are appoaching or exceeding their quota.

## Requirements
Python v3.6.5+
VestaCP

## Installation
- Pull repository or manually download the application files and place them in a suitably named directory
- Copy config.json.example to config.json

## Configuration
Amend the various settings in config.json

## Usage
python3 run.py

## Cron Job
The following line needs adding to v-list-sys-users, v-list-mail-domains, v-list-mail-accounts, v-list-mail-account when running via a Cron Job.  All of these files reside in /usr/local/vesta/bin.  This is due to Cron not having access to the VESTA Enviromental Variable.  The line needs adding prior to "source $VESTA/func/main.sh":

VESTA='/usr/local/vesta'
