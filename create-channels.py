
'''
Create Slack channels for Pagerduty integration

Set Channel purpose
Add Pagerduty bot user to channel
'''
import json
import requests
import sys
import urllib
# Public channel
#   https://api.slack.com/methods/channels.create
#   POST https://slack.com/api/channels.create
# Private Channel
#   https://api.slack.com/methods/groups.create
#   POST https://slack.com/api/groups.create
# Set purpose
#   https://api.slack.com/methods/channels.setPurpose
#   POST https://slack.com/api/channels.setPurpose
# Add User to channel
#   https://api.slack.com/methods/channels.invite
#   POST https://slack.com/api/channels.invite
# Lookup user by email
# by name ?
#   users.list and search ? sound slike only way
#   https://api.slack.com/methods/users.list
#   GET https://slack.com/api/users.list
# lookup bot/app ?

# TODO:
#   create api call function, handle errors, return data

if "SLACK_TOKEN" in os.environ:
    slack_token = os.environ["SLACK_TOKEN"]
else:
    print("ERROR: Environment variable SLACK_TOKEN is required")
    sys.exit(1)

arg_token = "token=" + slack_token
url_base = "https://slack.com/api/"
slack_bot = "pagerduty_slack_bot"

environments = ["prod", "test"]
repositories = [
    #"123456789012",
    "app1",
    "app2",
]

# channel max name length ?
# mon-xxxx- = 9

def get_channels():
    url = url_base + "channels.list?" + arg_token
    result = requests.get(url)
    data = result.json()
    return data["channels"]

def get_users():
    url = url_base + "users.list?" + arg_token
    result = requests.get(url)
    data = result.json()
    return data["members"]

def get_channel_id_by_name(channels, name):
    id = ""
    for channel in channels:
        if channel["name"] == name:
            id = channel["id"]
    return id

def get_user_id_by_name(users, name):
    id = ""
    for user in users:
        if user["name"] == name:
            id = user["id"]
    return id

def add_channel_user(channel_id, user_id):
    #   https://api.slack.com/methods/channels.invite
    url = url_base + "channels.invite?" + arg_token + "&channel=" + channel_id + "&user=" + user_id
    result = requests.post(url)
    print("Add user results {}".format(result))

def set_channel_purpose(channel_id, purpose):
    print("\tAdd purpose...")
    #purpose = "Alerts/Notifications for " + repo + " in " + env
    p = urllib.quote_plus(purpose)
    url = url_base + "channels.setPurpose?" + arg_token + "&channel=" + channel_id + "&purpose=" + p + "&pretty=1"
    print("\turl: {}".format(url))
    result = requests.post(url)
    print("\tresult status: {}".format(result.status_code))

def create_channel(name):
    channel_id = ""
    print("Creating channel: {}".format(name))
    url = url_base + "channels.create?" + arg_token + "&name=" + name + "&validate=true&pretty=1"
    print("\turl: {}".format(url))
    result = requests.post(url)
    print("\tresult status: {}".format(result.status_code))
    print(result)
    data = result.json()
    print(data)
    if "ok" in data and data["ok"]:
        channel_id = result.json() ["channel"]["id"]
    return channel_id


users = get_users()
pagerduty_id = get_user_id_by_name(users, slack_bot)
channels = get_channels()
print("# Channels: {}".format(len(channels)))
print("# Users: {}".format(len(users)))
print("Pagerduty ID: {}".format(pagerduty_id))

###
### Create channels for environments
###
for env in environments:
    name = "mon-" + env
    channel_id = create_channel(name)
    if len(channel_id) == 0:
        channel_id = get_channel_id_by_name(channels, name)
    set_channel_purpose(channel_id, "Alerts/Notifications for " + env)
    add_channel_user(channel_id, pagerduty_id)

###
### Create channels for services ??
###

###
### Create channels for services per environment
###
for env in environments:
    #if env != "test":
    #    continue
    for repo in repositories:
        #if repo != "123456789012":
        #    continue
        name = "mon-" + env + "-" + repo
        channel_id = create_channel(name)
        if len(channel_id) == 0:
            channel_id = get_channel_id_by_name(channels, name)
        set_channel_purpose(channel_id, "Alerts/Notifications for " + repo + " in " + env)
        add_channel_user(channel_id, pagerduty_id)

sys.exit(0)
'''
        print("Creating channel: {}".format(name))
        url = url_base + "channels.create?" + arg_token + "&name=" + name + "&validate=true&pretty=1"
        print("\turl: {}".format(url))
        result = requests.post(url)
        print("\tresult status: {}".format(result.status_code))
        print(result)
        data = result.json()
        print(data)
        if "ok" in data and data["ok"]:
            print("\tAdd purpose...")
            channel_id = result.json() ["channel"]["id"]
            purpose = "Alerts/Notifications for " + repo + " in " + env
            p = urllib.quote_plus(purpose)
            url = url_base + "channels.setPurpose?" + arg_token + "&channel=" + channel_id + "&purpose=" + p + "&pretty=1"
            print("\turl: {}".format(url))
            result = requests.post(url)
            print("\tresult status: {}".format(result.status_code))
            # invite user @pagerduty_slack_bot
            # channel= channel id & user= user id
'''
