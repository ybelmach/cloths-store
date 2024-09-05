import pyotp

from django.core.mail import send_mail
from django.shortcuts import render
from datetime import datetime, timedelta

import my_info


def two_fa_sending(request, user, path):
    email = user.email
    totp = pyotp.TOTP(pyotp.random_base32(), interval=600)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=10)
    request.session['otp_valid_time'] = str(valid_date)
    send_mail(
        subject='Your code verification from online shop.',
        message=f"""Hello Dear Customer
Please enter this verification code in site now to confirm your email address and complete the 2FA process:
Your verification PIN:
{otp}
This code expires 10 minutes from when it was sent. If the code is not entered, your account may be cracked.
Thanks,
The Shop Team""",
        from_email=my_info.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    print(f"[INFO] message to email was sent to {email}")
    return render(request, path)
