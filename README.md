# Vaccination Notifier

This script periodically checks the mysejahtera api for
any changes to your vacination status, and sends you a notification
when a change is detected.

Originally made by Matt, with contributions from CaviarChen,
blueset, josephsurin, alanung, and abhinavcreed13 as a [UoM WAM Spammer](https://github.com/matomatical/UoM-WAM-Spam).

Modified by Cedric0303 to work on MySejahtera API for vaccination notifications.

Details involving accessing MySejahtera API came from [nakvaksin](https://github.com/nubpro/nakvaksin).


## Installation

Clone this repository to get started Vaccination Notifying!

The basic Vaccination Notifier script requires [Python 3.6](https://www.python.org/)
(or higher).

Once you have Python installed, you'll also need the following two
third-party Python packages for API handling:

* [Requests](https://2.python-requests.org/en/master/)


You can easily install these with [pip](https://pypi.python.org/pypi/pip)
using the command `pip3 install requests`, or however else
you prefer to install Python packages.


## Configuration

While the script has sensible default settings, it's also easily configurable.
You can modify the constants atop `vacnotify.py` to easily change the behaviour.
Some important configuration options are:

* `CHECK_REPEATEDLY`: By default, the script will repeatedly check your vaccination status until you kill it.
If you want the script to check your vaccination status only once, set this to `False`.

* `DELAY_BETWEEN_CHECKS`: You can configure how often the script logs in to check for results.
Default is set to 180 minutes.


There are some other configuration options, all documented in the script itself.

### Notifcation methods

The script can notify you using a range of notification methods. Each requires
its own configuration, as explained below:

* #### Email (default)

   The default notifcation method. The script will log in to your 
   email account and send you a self-email notifying you about vaccination status changes.

   This option requires no additional configuration, but if you see an error
   (or similar):
   `smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')`
   then Google must be blocking the script's attempt to log into your SMTP
   server. This is because Google thinks the way the script logs into your
   account does not meet their security standards.
   One work-around is to go to: [your Google security settings](https://myaccount.google.com/u/2/lesssecureapps?pageId=none)
   and turn on the option to "allow less secure apps".
   You might like to remember to turn it off when you get your results.

   The following notification method is a more secure workaround, with a few
   more configuration steps.

* #### WeChat message

   The script will use the [ServerChan](https://sc.ftqq.com) API to send you a
   [WeChat](https://wechat.com) message.

   You'll need to acquire a WeChat account and a ServerChan API key.
   Set up your account and then configure the script with your API key
   (you can hard-code it into `vacnotify.py`, or add code to read it from a file 
   or environment variable or standard input, for example).
   Remember to keep your secrets safe!

* #### Telegram message

   The script will contact a Telegram Bot so that it may send you a Telegram
   message.

   You will need a [Telegram](https://telegram.org) account and a Telegram bot
   (which can be created using [@BotFather](https://t.me/botfather)).
   You'll then need a bot access token, which will be in the format:
   ```
   123456789:AaBbCcDdEeFfGgHhIiJjKkLlMm
   ```
   Set up your Telegram account and note the numerical user, group, or channel ID
   you wish to be contacted through (your 'destination').
   Configure the script with your access token and destination (you can hard-code
   them into `vacnotify.py`, or add code to read them from a file or environment
   variable or standard input, for example).
   Remember to keep your secrets safe!

* #### Push notifications (Pushbullet)

   The script will use the [Pushbullet](https://www.pushbullet.com) API to send
   you a push notification (to whichever devices you have their apps installed).

   You'll need to acquire a Pushbullet account and API Access Token for this.
   Set up your account and link your desired devices, then configure the script
   with your access token (you can hard-code it into `vacnotify.py`, or add code to
   read it from a file or environment variable or standard input, for example).
   Remember to keep your secrets safe!

* #### IFTTT webhook

   The script will trigger an [IFTTT](https://ifttt.com) webhook, which you can
   set up to contact you in any means supported by the IFTTT service.

   You'll need an IFTTT account and a webhook key. You can retrieve a key
   [here](https://ifttt.com/maker_webhooks), and should be in the format:
   ```
   Aa0Bb1Cc2Dd3Ee4Ff5Gg6H
   ```
   Configure the script with your webhook key (you can hard-code it into
   `vacnotify.py`, or add code to read it from a file or environment variable or
   standard input, for example).
   The script will send notification messages with the event `vac-notify`, with
   `value1` set to the subject of the notification and `value2` set to the
   body text. Set up an IFTTT applet to respond to this event, and enter the
   webhook key into the script at runtime, or hard-code it into
   `notify/by_ifttt.py`.
   Remember to keep your secrets safe!

* #### Desktop notification

   The script will trigger a desktop notification displaying the update.

   Desktop notifications require an additional third-party Python module,
   [notify2](notify2.readthedocs.org). First, install this package (e.g.
   `pip install notify2`).

   Depending on your platform, you may need to install support for desktop
   notifications. For example, for Arch linux, you'll need [libnotify and a
   notification server](https://wiki.archlinux.org/index.php/Desktop_notifications).

   No script configuration is required, other than to turn on the notifier.

* #### Logfile message

   The script will log the notification message to a local file.

   The only configuration required is to configure the name of the desired file
   into the script (you can hard-code it into `vacnotify.py`, or add code to read
   it from a file or environment variable or standard input, for example).

* #### Slack webhook
   
   The script will trigger a slack webhook which you can configure for your
   personal message channel. 
   
   In order to enable slack webhook integration, you need to follow the
   steps below:
   
   - Create or choose the slack workspace you wish to connect.
   - Open the [Slack App Directory](https://slack.com/apps), and search for
     the *Incoming WebHooks* integration.
   - Choose the channel or conversation you want to send messaged to and click
     *Add Incoming WebHooks Integration*.
     In the next view, you can customise the integration as you wish
     (don't forget to Save if you do make any changes).
     For example, you can customise the name, icon and labels.
   - You'll eventually see the Webhook URL. Copy this URL.
   - Uncomment `option 8` in `vacnotify.py` and add your copied webhook URL as
     the `SLACK_APP_WEBHOOK` variable.
   
#### Multiple notification methods

The script can combine multiple notification methods in its attempt to reach
you regarding a detected vaccination status change.

All you'll need to configure each of your desired notification methods
individually using the above instructions, and ensure they all get added to the
multi-notifier during the configuration section of the script.

That is, to use multiple notification methods, *just uncomment and configure multiple
notification methods!*


## Usage

Once you have installed the requirements and configured the script, simply run
it with `python3 vacnotify.py`.

The script will ask you for your MySejahtera username and password. It uses these
to log into the MySejahtera API on your behalf every however-many minutes you
configured, looking for updated vaccination results. It stores the previous results in a
JSON-formatted text file between checks, for comparison.

The first time the script finds your results, or whenever it sees your vaccination resultdata change, 
the script will also send you a notification using your configured
notification method(s).

> Note: Don't forget to stop the script after the receiving your vaccination result!


### Common issues

The script is not very robust.  If anything goes wrong, it will probably crash
with an overly dramatic error message.  Please see these possible errors:

##### The script crashes with an error: `InvalidLoginException`.

You might have typed your username or password wrong.
Please check that you got them right, and try again.

##### The script crashes with an error: `InvalidVaccinationException`.

You might have not registered for the vaccine.
Please check that you have sucessfully registered for the vaccine.

### Other issues
Some notification methods may not work properly yet as they haven't been modified to work with Vaccination Notifier. - Cedric0303