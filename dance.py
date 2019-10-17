from flask import Flask, redirect, url_for
import os
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github


app = Flask(__name__)


app.config['SECRET_KEY'] = 'akjhsdvfkjahsdvfkjhsadv'

github_blueprint = make_github_blueprint(client_id=os.environ.get("GITHUB_OAUTH_CLIENT_ID"), client_secret=os.environ.get("GITHUB_OAUTH_CLIENT_SECRET"))

app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')

app.register_blueprint(github_blueprint, url_prefix='/login')

@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    print("authorized")
    resp = github.get("/user")
    assert resp.ok
    print(resp.json()["login"])
    return "You are @{login} on GitHub".format(login=resp.json()["login"])
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)