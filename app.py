from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask import send_from_directory
from backend.routes.resume_routes import resume_bp


load_dotenv()


app = Flask(__name__,static_folder='frontend')

CORS(app)


app.register_blueprint(
    resume_bp,
    url_prefix="/resume"
)


@app.route("/")
def home():

    return {
        "message":
        "Resume AI Screener API Running"
    }
@app.route("/dashboard")
def dashboard():

    return send_from_directory(
        "frontend",
        "dashboard.html"
    )
@app.route('/css/<path:filename>')
def css_files(filename):

    return send_from_directory(
        'frontend/css',
        filename
    )


@app.route('/js/<path:filename>')
def js_files(filename):

    return send_from_directory(
        'frontend/js',
        filename
    )

if __name__=="__main__":

    app.run(
    debug=True,
    use_reloader=False,
    port=5000
)

