from django.core.mail import send_mail



class emailHandler:
    _email_account='delphi.tbd@gmail.com'
    _new_acc_subject='New Delphi Account'
    _forget_pass_subject='Delphi password change request'
    _new_acc_email_file='tree/new_account_email.txt'
    _forg_pass_email_file='tree/forgotten_email.txt'
   
    '''
    emailNewUser: a function called by handleSignUp in views. Is meant to email 
                  a new user that their account was succesfully made.
    input: to_email: The email address of the new user
    '''
    def emailNewUser(self, to_email):
        with open(self._new_acc_email_file,'r') as email_file_tmp:
            email_body_tmp=email_file_tmp.read()
        send_mail(self._new_acc_subject,email_body_tmp,self._email_account,[to_email],fail_silently=False)
    
    '''
    emailForgPass: a function called by handleForgotPassword to send a user a
                   unique web address which allows them to change their password.
    input: to_email: the email address of a user
    '''
    def emailForgPass(self, to_email):
        with open(self._forg_pass_email_file,'r') as email_file_tmp:
            email_body_tmp=email_file_tmp.read()
        #must insert the random webpage for a newpassword here
        send_mail(self._forget_pass_sbuject,email_body_tmp,self._email_account,[to_email],fail_silently=False)