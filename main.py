import os, random
from  flask import Flask, render_template, request as rq, g, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

Host = "0.0.0.0"
background_bf_rd = ["ba.jpg", "752346.png", "753591.png", "920997.png", "BdBy1Ky.png"]

@app.route('/', methods=['GET', 'POST'])
def login():
    background_rd = random.choice(background_bf_rd)
    if rq.method =='POST':
        headers = rq.headers.get('Host')
        file = open("log_headers.log", "a")
        file.write(str(headers+"\n"))
        session.pop('user', None)
        if rq.form['username'] == str(os.getenv("USER")) and rq.form['password'] == str(os.getenv("PASSWORD")):
            session['user'] = rq.form['username']
            return redirect(url_for('cli'))
        else:
            wrong = "wrong username or password"
            return render_template('login.html', data=wrong, bg=background_rd)

    return render_template('login.html', bg=background_rd)

@app.route('/cli', methods=['GET', 'POST'])
def cli():
    if g.user:
            if len(rq.form)==0 or not rq.method == "POST":
                background = "black.jfif"
                end_sesion = url_for('login')
                resp = render_template("cli.html", bg=background, Host=Host, end_sesion=end_sesion)
            else:
                cli = rq.form["cli"]
                stream = os.popen(cli)
                output = f"\nroot@neko:~# {cli}\n"+stream.read()
    
                if rq.form["cli"] == "":
                    background = "black.jfif"
                    end_sesion = url_for('login')
                    resp = render_template("cli.html", output=output, bg=background, Host=Host, end_sesion=end_sesion)
                elif output == f"\nroot@neko:~# {cli}\n":
                    background = "black.jfif"
                    alert = "wrong command"
                    end_sesion = url_for('login')
                    resp = render_template("cli.html", output=output.replace(cli, ""), bg=background, data_alert=alert, Host=Host, end_sesion=end_sesion)
                else:
                    end_sesion = url_for('login')
                    background_rd = random.choice(background_bf_rd)
                    resp = render_template("cli.html", output=output, bg=background_rd, Host=Host, end_sesion=end_sesion)
    
            return resp
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']
        print(g.user)

@app.route('/end')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.debug = True
    app.run(host=Host, port=80)
