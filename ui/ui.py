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

@app.route('/', methods=['GET'])
def index():
    if not 'username' in session:
        flash('Please log in')
        return redirect(url_for('login'))

    from db import Db
    from forms.edit import EditForm

    db = Db()
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

@app.route('/add/', methods=['GET'])
def add():
    if not 'username' in session:
        flash('Please log in')
        return redirect(url_for('login'))

    from forms.edit import EditForm
    form = EditForm(request.form, csrf_context=request.remote_addr)
    return render_template('add.html', form=form)

@app.route('/save/', methods=['POST'])
def save():
    if not 'username' in session:
        flash('Please log in')
        return redirect(url_for('login'))

    from forms.edit import EditForm
    form = EditForm(request.form, csrf_context=request.remote_addr)

    if form.validate():
        from db import Db
        db = Db()

        if 'delete' in request.form and request.form['delete'] == 'y':
            db.delete_announce(request.form['name'])
            flash('Item succesfully deleted')
        else:
            raw_announces = request.form['texts'].strip()
            announces = {}
            lines = raw_announces.split("\n")

            for line in lines:
                items = line.split("|")
                if len(items) > 1:
                    announces[items[0]] = items[1]

            links = {}
            links['android'] = request.form['android']
            links['ios'] = request.form['ios']


            data = {}
            data['game'] = request.form['name']
            data['announces'] = announces
            data['links'] = links

            if db.update_announce(data) == None:
                flash("Data update error")
            else:
                flash("Data succesfully saved")

        return redirect(url_for('index'))

        #import pprint
        #return pprint.pformat(request.form)
    else:
        flash('Form error! Data wasn\'t saved!')
        return redirect(url_for('index'))


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
