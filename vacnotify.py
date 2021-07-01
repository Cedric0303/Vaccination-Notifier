import json
import time
import getpass
import requests
import messages

print("Configuring script...")

# set this to True if you would like the script to repeatedly check the results
# page, or False if you only want it to run once
CHECK_REPEATEDLY = True

# if you set the script to check repeatedly above, you can configure the delay
# between vaccination status checks in minutes here
DELAY_BETWEEN_CHECKS = 180 # minutes

# leave these lines unchanged to be prompted for your username and password
# every time you run the script, or just hard code your credentials here if
# you"re lazy (but then be careful not to let anyone else see this file)
print("Username can be either your phone number or email address.")
MYSEJAHTERA_USERNAME = input("Username: ")
MYSEJAHTERA_PASSWORD = getpass.getpass()
# MYSEJAHTERA_USERNAME = "<INSERT USERNAME HERE>"
# MYSEJAHTERA_PASSWORD = "<INSERT PASSWORD HERE>"

# your results will be stored in this file in between checks
RESULTS_FILENAME = "results.txt"

# # #
# NOTIFICATION CONFIGURATION
#

# we"ll use a multi-notifier to allow for any number of
# notification methods (added below)
from notify.by_multiple import MultiNotifier
NOTIFIER = MultiNotifier()

# choose one or more notification methods to use when a change is detected.

# in most cases you can configure the notification method with the required
# secrets by including them in the corresponding script, or by leaving the
# scripts alone and typing them in at start-up time (see README for per-method
# instructions, and remember to keep your secrets safe!)
print("Configuring chosen notification method(s)...")

# option 0: email notification, via SMTP
from notify.by_email import SMTPGmailNotifier
# the script will send email from and to your email address by default.
# if you need to use an app-specific password to get around 2FA on
# your email account, or other authentication issues, you can set it
# here as the value of password.
GMAIL_ADDRESS = input("Email address: ")
GMAIL_PASSWORD = getpass.getpass()
# GMAIL_ADDRESS  = "<INSERT GMAIL ADDRESS HERE>"
# GMAIL_PASSWORD = "<INSERT PASSWORD HERE>" # or app-specific password
NOTIFIER.add_notifier(SMTPGmailNotifier(
    address=GMAIL_ADDRESS,
    password=GMAIL_PASSWORD)) 

# option 1: wechat notification via ServerChan
# uncomment below and configure to enable
# from notify.by_wechat import ServerChanNotifier
# SERVERCHAN_API_KEY = # put API key here, as a string (see README)
# NOTIFIER.add_notifier(ServerChanNotifier(
#    apikey=SERVERCHAN_API_KEY))

# option 2: telegram notification via a telegram bot
# uncomment below and configure to enable
# from notify.by_telegram import TelegramBotNotifier
# TELEGRAM_ACCESS_TOKEN = # put access token string here (see README)
# TELEGRAM_DESTINATION  = # put destination chat name here (see README)
# NOTIFIER.add_notifier(TelegramBotNotifier(
#    token=TELEGRAM_ACCESS_TOKEN,
#    chat=TELEGRAM_DESTINATION))

# option 3: push notification via pushbullet
# uncomment below and configure to enable
# from notify.by_push import PushbulletNotifier
# PUSHBULLET_ACCESS_TOKEN = # put access token here (string) (see README)
# NOTIFIER.add_notifier(PushbulletNotifier(
#    token=PUSHBULLET_ACCESS_TOKEN))

# option 4: ifttt notification via triggering a webhook
# uncomment below and configure to enable
# from notify.by_ifttt import IFTTTWebhookNotifier
# IFTTT_WEBHOOK_KEY = # put webhook key string here (see README)
# NOTIFIER.add_notifier(IFTTTWebhookNotifier(
#    key=IFTTT_WEBHOOK_KEY))

# option 5: desktop notifications using notify2 python library
# uncomment below to enable
# from notify.by_desktop import DesktopNotifier
# NOTIFIER.add_notifier(DesktopNotifier())

# option 6: notifications via appending to a local file
# uncomment below and configure to enable
# from notify.by_logfile import LogFileNotifier
# LOGFILE_FILEPATH = # put filepath string here (see README)
# NOTIFIER.add_notifier(LogFileNotifier(
#    filepath=LOGFILE_FILEPATH))

# option 7: push notification via slack incoming webhooks
# uncomment below and configure to enable
# from notify.by_slack import SlackAppNotifier
# SLACK_APP_WEBHOOK = # put webhook key string here (see README)
# NOTIFIER.add_notifier(SlackAppNotifier(
#    hook_url=SLACK_APP_WEBHOOK))

# let"s get to it!

def main():
    NOTIFIER.notify(*messages.hello_message(delay=DELAY_BETWEEN_CHECKS))
    
    # conduct the first check! don't catch any exceptions here, if the check
    # fails this first time, it"s likely to be a configuration problem (e.g.
    # wrong username/password) so we should crash the script to let the user
    # know.
    poll_and_notify()

    while CHECK_REPEATEDLY:
        print("Sleeping", DELAY_BETWEEN_CHECKS, "minutes before next check.")
        time.sleep(DELAY_BETWEEN_CHECKS * 60) # seconds
        print("Waking up!")
        try:
            poll_and_notify()
        except Exception as e:
            # if we get an exception now, it may have been some temporary
            # problem accessing the website, let"s just ignore it and try
            # again next time.
            print("Exception encountered:")
            print(f'{e.__class__.__name__}: {e}')
            print('Hopefully it won"t happen again. Continuing.')


def poll_and_notify():
    """
    Check for updated results, and send a notification if a change is detected.
    """
    # query the API for the latest result
    new_results = get_status(MYSEJAHTERA_USERNAME, MYSEJAHTERA_PASSWORD)
    # load the previous results from file
    try:
        with open(RESULTS_FILENAME) as resultsfile:
            old_results = json.load(resultsfile)
    except:
        # the first run, there probably won"t be such a file
        # imagine a default
        old_results = {
            'Health Facility:': '',
            'Vaccination Location:': '',
            'Date:': '',
            'Time:': ''}

    if new_results == "DONE":
        print("Congratulations, you have received all your vaccinations.")
        return
    
    # compare the results:
    elif new_results and old_results != new_results:
        # send notification
        print("Found updated results for your vaccination.")
        NOTIFIER.notify(*messages.update_message(new_results))
        # update the results file for next time
        with open(RESULTS_FILENAME, "w") as resultsfile:
            json.dump(new_results, resultsfile, indent=2)

    else:
        # no change to results to vaccination status. ignore it!
        print("No changes to your vaccination status.")
        for key, value in old_results.items():
            print(key, value)


class InvalidLoginException(Exception):
    """Represent a login form validation error"""

class InvalidVaccinationException(Exception):
    """Represent a vaccination registration error"""


def get_status(username, password):
    
    with requests.Session() as session:
    
        print("Logging in to the MySejahtera page")
        login_form = dict()
        login_form["username"] = username
        login_form["password"] = password
        
        response = session.post("https://mysejahtera.malaysia.gov.my/epms/login", data=login_form)
        if response.status_code > 299:
            raise InvalidLoginException("Your login attempt was not successful."
                    " Please check your details and try again.")
        response = session.get("https://mysejahtera.malaysia.gov.my/epms/v1/mobileApp/vaccination/processFlow", 
            headers={"x-auth-token": dict(response.headers)["X-AUTH-TOKEN"]})
        
        stages = response.json()
        
        first_done = False

        for stage in stages:
            stage_fields = dict(stage)
            stage_name = stage_fields["headerText"]["en_US"]
            stage_state = stage_fields["state"]

            if not first_done:
                if stage_name == "Registered" and stage_state == "PENDING":
                    raise InvalidVaccinationException("You have not registered for the vaccine.")
                if stage_name == "1st Dose appointment":
                    if stage_state == "ACTIVE":
                        data_dict = {each['text']['en_US']: each['value'] for each in stage_fields['data']}
                        return data_dict
                    elif stage_state == "COMPLETED":
                        first_done = True
            
            if first_done:
                if stage_name == "2nd Dose appointment":
                    if stage_state == "ACTIVE":
                        data_dict = {each['text']['en_US']: each['value'] for each in stage_fields['data']}
                        return data_dict
                    elif stage_state == "COMPLETED":
                        return "DONE"
        return False


if __name__ == "__main__":
    main()
