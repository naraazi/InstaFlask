from app.extensions import db
from app.user import user
from app.user.models import User
from app.user.forms import SignupForm, LoginForm, ResetForm, PasswordResetForm
from app.helper.mail import send_email
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required


@user.route('/signup', methods=['get', 'post'])
def signup():
    if current_user.is_authenticated:
        return 'You need to logout to access this page!'
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('signup.html', form=form)


@user.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return 'You need to logout to access this page!'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user.route('/confirm')
@login_required
def confirm():
    if current_user.is_confirmed:
        return 'You are already confirmed'
    token = current_user.get_serializer_token()
    # -- EMAIL SENDER HERE!!
    send_email(subject='E-mail Confirmation', to=current_user.email,
               text_body='If your are getting this, it means you are unable to see HTML page. Please contact Admin.',
               template='confirm', token=token)
    return '<h1>An confirmation mail has been sent to your e-mail. Check your Inbox.</h1>'


@user.route('/confirm/<token>')
@login_required
def confirmation(token):
    if current_user.is_confirmed:
        return 'You are already confirmed'
    user = User.verify_serializer_token(token, salt='Mail Confirmation')
    if user:
        user.is_confirmed = True
        db.session.commit()
        return 'User Confirmed'
    return "<h1>There has been some issue. Please try again</h1>"


@user.route('/reset', methods=['get', 'post'])
def reset():
    if current_user.is_authenticated:
        return 'You need to logout to access this page!'
    form = ResetForm()
    if form.validate_on_submit():
        # -- HERE U CHANGE 'USER' WITH 'EMAIL' ON PASSWORD RESETTING
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user:
            token = user.get_serializer_token(salt='Password Reset')
            # -- EMAIL SENDER HERE!!
            send_email(subject='Password Reset', to=user.email,
                       text_body='If your are getting this, it means you are unable to see HTML page. Please contact Admin.',
                       template='reset', token=token)
            return '<h1>Mail has been send. Check your Inbox.</h1>'
    return render_template('reset.html', form=form)


@user.route('reset/<token>', methods=['get', 'post'])
def reset_request(token):
    if current_user.is_authenticated:
        return 'You need to logout to access this page!'
    form = PasswordResetForm()
    user = User.verify_serializer_token(token, salt='Password Reset')
    if user:
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            return redirect(url_for('user.login'))
        return render_template('password_reset.html', form=form)
    else:
        return redirect(url_for('user.reset'))
    return "Password Reset Request"
