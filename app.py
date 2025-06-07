from flask import Flask, request, redirect, render_template
import itsdangerous
import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-fallback-key")
serializer = itsdangerous.URLSafeSerializer(SECRET_KEY)

# Allow only these domains to prevent abuse
ALLOWED_DOMAINS = ["travelaroundplaces.com"]

def make_redirect_token(url):
    return serializer.dumps(url)

def is_domain_allowed(url):
    try:
        domain = urlparse(url).netloc
        return any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS)
    except Exception:
        return False

@app.route('/redirect')
def redirect_route():
    token = request.args.get('t')
    if not token:
        return "<h2>❌ No redirect token provided.</h2>"
    try:
        url = serializer.loads(token)
        if not is_domain_allowed(url):
            return "<h2>⚠️ Redirect domain not allowed.</h2>"
        return redirect(url)
    except Exception as e:
        return f"<h2>❌ Invalid or expired token: {str(e)}</h2>"

@app.route('/')
def index():
    url = "https://travelaroundplaces.com/restaurants-in-boca-raton-fl/"
    token = make_redirect_token(url)
    
    # ⚠️ Use your actual Render domain here once deployed
    redirect_link = f"https://redirector-site.onrender.com/redirect?t={token}"
    
    return render_template('index.html', redirect_link=redirect_link)

if __name__ == '__main__':
    app.run(debug=True)
