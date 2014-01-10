__author__ = 'Roman Arkharov'

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash

app = Flask(__name__)

app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def index():
    if not 'username' in session:
        flash('Please log in')
        return redirect(url_for('login'))

    if request.method == 'POST':
        import pprint
        return pprint.pformat(request.form)
    else:
        from db import Db
        from flask import current_app
        from forms.edit import EditForm

        db = Db(current_app.config['MONGODB_DATABASE'], current_app.config['MONGODB_HOST'], current_app.config['MONGODB_PORT'])
        announces = db.load_announces()
        a = {}

        counter = 0
        edit_forms = []

        for key in announces:
            item = announces[key]
            if 'links' in item and 'announces' in item:
                links = item['links']
                if 'ios' in links and 'android' in links:
                    a[key] = item

                    form = EditForm(request.form, csrf_context=request.remote_addr)
                    form.name.data = key
                    form.android.data = links['android']
                    form.ios.data = links['ios']

                    texts = ''
                    for key in item['announces']:
                        texts = texts + key + "|" +  item['announces'][key] + "\n"

                    form.texts.data = texts

                    edit_forms.append(form)

                    counter = counter + 1

        return render_template('index.html', announces=a, counter=counter, edit_forms=edit_forms)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash("You've already logged in")
        return redirect(url_for('index'))

    from forms.user.login import LoginForm

    form = LoginForm(request.form, csrf_context=request.remote_addr)

    if request.method == 'POST':
        if form.validate():
            session['is_logged'] = True
            session['username'] = request.form['login']
            session['password'] = request.form['password']
            return redirect(url_for('index'))
        elif form.csrf_token.errors:
            # If we're here we suspect the user of cross-site request forgery
            flash('CSRF error.')
            return render_template('login.html', form=form)
        else:
            # If form data contains errors
            flash('Login error', 'alert')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    return 'Logout'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
