def save_user(role, name):
    print(f"Saving {role}: {name}")


def send_welcome_email(email):
    print(f"Sending email to {email}")


def create_user(role, name, email):

    save_user(role, name)
    send_welcome_email(email)