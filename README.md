# Over Quota Notifier
This script is designed to work with VestaCP and send out email alerts when mail accounts are appoaching or exceeding their quota.


### Notes
The following line needs adding to v-list-sys-users, v-list-mail-domains, v-list-mail-accounts, v-list-mail-account when running via a Cron Job.  All of these files reside in /usr/local/vesta/bin.  This is due to Cron not having access to the VESTA Enviromental Variable.  The line needs adding prior to "source $VESTA/func/main.sh":

VESTA='/usr/local/vesta'
