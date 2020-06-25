import os
import json
import subprocess
import os.path
import smtplib

def json_from_shell_command(cmd):
    response = subprocess.check_output(cmd + ' json', shell=True)
    return json.loads(response)

def get_users():
    return json_from_shell_command('v-list-sys-users')

def get_domains(user):
    return json_from_shell_command('v-list-mail-domains ' + user)

def get_mail_accounts(user, domain):
    return json_from_shell_command('v-list-mail-accounts ' + user + ' ' + domain)

def get_mail_account_info(user, domain, account):
    account_info = json_from_shell_command('v-list-mail-account ' + user + ' ' + domain + ' ' +  mail_account)[mail_account]
    if account_info['QUOTA'] == "unlimited":
        account_info['QUOTA'] = CONFIG['unlimited_quota']
    account_info['U_DISK'] = int(account_info['U_DISK'])
    account_info['QUOTA'] = int(account_info['QUOTA'])
    account_info['ADDRESS'] = account + '@' + domain
    return account_info

def send_email_report(report):
    message = f'Subject: Quota Issues on jupiter.mshost.co.uk\nTo: {CONFIG["recipient"]}\nFrom: {CONFIG["sender"]}\n\n{report}'

    server = smtplib.SMTP(CONFIG['smtp_host'], CONFIG['smtp_port'])
    if CONFIG['local_hostname'] != '':
        server.local_hostname = CONFIG['local_hostname']
    if CONFIG['smtp_username'] != '':
        server.login(CONFIG['smtp_username'], CONFIG['smtp_password'])
    server.sendmail(CONFIG['sender'], CONFIG['recipient'], message)
    server.quit()

f = open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "r")
CONFIG = json.loads(f.read())

report = ''

for user in get_users():
    for domain in get_domains(user):
        for mail_account in get_mail_accounts(user, domain):
            mail_account_info = get_mail_account_info(user, domain, mail_account)

            quota_percentage = round(float(mail_account_info['U_DISK']) / float(mail_account_info['QUOTA']) * 100, 1)
            usage_string = ' (Quota: ' + str(mail_account_info['QUOTA']) + 'MB | Usage: ' + str(mail_account_info['U_DISK']) + 'MB | ' + str(quota_percentage) + '%)'

            if mail_account_info['U_DISK'] >= mail_account_info['QUOTA']:
                report = report + mail_account_info['ADDRESS'] + ' is over quota' + usage_string + CONFIG['new_line']
            elif quota_percentage > CONFIG['quota_warning_percentage']:
                report = report + mail_account_info['ADDRESS'] + ' is over ' + str(CONFIG['quota_warning_percentage']) + '% warning level' + usage_string + CONFIG['new_line']

if report != '':
    print(report)
    send_email_report(report)
    