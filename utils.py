from datetime import datetime


def update_to_user(update):
    return {
        "userId": update.message.chat['id'],
        "userName": update.message.chat['username'],
        "firstName": update.message.chat['first_name'],
        "firstDate": str(datetime.now()),
        "balance": 0.0,
        "refBalance": 0.0,
        "referralLink": 'some_referral_link'
    }


def check_data(data):
    if isinstance(data, str):
        return "'{}'".format(data)
    else:
        return data


def update_to_settings(update):
    return {
        "userId": update.message.chat['id'],
        "some_row": '...'
    }
