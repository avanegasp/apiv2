import os

from breathecode.admissions.models import CohortUser
from breathecode.authenticate.models import Profile
from ..command import command
from ..utils import to_string

"""
Possible parameters for this command:
- users: Array of user slack_ids mentioned inside the slack command text content
- user_id: Slack user ID of the message author
- team_id: Slack team_id where the message was posted
- channel_id: Slack channel_id where the message was posted
- text: Content of the slack channel

"""
@command(only='staff')
def execute(users, **context):

    if len(users) == 0:
        raise Exception("No usernames found on the command")

    response = {
        "blocks": []
    }
    response["blocks"].append(render_student(user_id=users[0]))

    return response

def render_student(user_id):

    cohort_users = CohortUser.objects.filter(user__slackuser__slack_id=user_id, role='STUDENT')
    user = cohort_users.first()
    if user is None:
        raise Exception(f"Student {user_id} not found on any cohort")

    user = user.user
    cohorts = [c.cohort for c in cohort_users]

    avatar_url = os.getenv("API_URL","") + "/static/img/avatar.png"
    github_username = "Undefined"
    phone = "Undefined"
    try:
        github_username = user.profile.github_username
        avatar_url = user.profile.avatar_url
        phone = user.profile.phone
    except Profile.DoesNotExist:
        pass

    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Student Name:* {user.first_name} {user.last_name}\n*Github*: {github_username}\n*Phone*: {phone}\n*Cohorts:*: {','.join([c.name for c in cohorts])}\n*Education Status:* {','.join([to_string(c.educational_status) for c in cohort_users])}\n*Finantial Status:* {','.join([to_string(c.finantial_status) for c in cohort_users])}"
        },
        "accessory": {
            "type": "image",
            "image_url": to_string(avatar_url),
            "alt_text": f"{user.first_name} {user.last_name}"
        }
    }