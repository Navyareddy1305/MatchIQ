from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from werkzeug.utils import secure_filename

from pypdf import PdfReader
from docx import Document

import os
import uuid
import json

from matcher import calculate_match


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "matchiq-secret-key-change-this"


UPLOAD_FOLDER = "uploads"
APPLICATION_FOLDER = "applications"


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    APPLICATION_FOLDER,
    exist_ok=True
)


APPLICATIONS_FILE = os.path.join(
    APPLICATION_FOLDER,
    "applications.json"
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def allowed_file(filename):
    """
    Check whether uploaded file is PDF or DOCX.
    """

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf(filepath):
    """
    Extract text from PDF resume.
    """

    reader = PdfReader(filepath)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text.append(
                page_text
            )

    return "\n".join(text)


# =========================================================
# DOCX TEXT EXTRACTION
# =========================================================

def extract_docx(filepath):
    """
    Extract text from DOCX resume.
    """

    document = Document(filepath)

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text.append(
                paragraph.text.strip()
            )

    return "\n".join(text)


# =========================================================
# RESUME EXTRACTION
# =========================================================

def extract_resume(filepath):
    """
    Automatically extract resume text
    depending on file type.
    """

    extension = filepath.rsplit(
        ".",
        1
    )[1].lower()

    if extension == "pdf":

        return extract_pdf(filepath)

    elif extension == "docx":

        return extract_docx(filepath)

    return ""


# =========================================================
# APPLICATION STORAGE
# =========================================================

def load_applications():
    """
    Load saved applications from JSON file.
    """

    if not os.path.exists(
        APPLICATIONS_FILE
    ):

        return []


    try:

        with open(
            APPLICATIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception:

        return []


# =========================================================
# SAVE APPLICATION
# =========================================================

def save_application(application):
    """
    Save a new application.
    """

    applications = load_applications()

    applications.append(
        application
    )

    with open(
        APPLICATIONS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            applications,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        if not email or not password:

            return render_template(
                "login.html",
                error="Please enter email and password."
            )


        # Create session

        session["logged_in"] = True

        session["email"] = email

        session["name"] = (
            email
            .split("@")[0]
            .title()
        )


        return redirect(
            url_for("profile")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# SIGNUP
# =========================================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        if not name or not email or not password:

            return render_template(
                "signup.html",
                error="Please fill all fields."
            )


        # Create session

        session["logged_in"] = True

        session["name"] = name

        session["email"] = email


        return redirect(
            url_for("profile")
        )


    return render_template(
        "signup.html"
    )


# =========================================================
# PROFILE / CANDIDATE DASHBOARD
# =========================================================

@app.route("/profile")
def profile():

    return render_template(
        "profile.html"
    )


# =========================================================
# EMPLOYEE PROFILE ALIAS
# =========================================================

@app.route("/employee/profile")
def employee_profile():

    return render_template(
        "profile.html"
    )


# =========================================================
# JOBS
# =========================================================

@app.route("/jobs")
def jobs():

    return render_template(
        "jobs.html"
    )


# =========================================================
# APPLY FOR JOB
# =========================================================

@app.route(
    "/apply",
    methods=["GET", "POST"]
)
def apply():

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        job_title = request.args.get(
            "title",
            ""
        ).strip()

        company = request.args.get(
            "company",
            ""
        ).strip()

        location = request.args.get(
            "location",
            ""
        ).strip()

        job_type = request.args.get(
            "type",
            ""
        ).strip()

        salary = request.args.get(
            "salary",
            ""
        ).strip()

        description = request.args.get(
            "description",
            ""
        ).strip()

        skills = request.args.get(
            "skills",
            ""
        ).strip()


        return render_template(
            "apply.html",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary,
            description=description,
            skills=skills
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    job_title = request.form.get(
        "job_title",
        ""
    ).strip()

    company = request.form.get(
        "company",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    job_type = request.form.get(
        "job_type",
        ""
    ).strip()

    salary = request.form.get(
        "salary",
        ""
    ).strip()

    cover_letter = request.form.get(
        "cover_letter",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:

        return render_template(
            "apply.html",
            error="Please enter your name.",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary
        )


    if not email:

        return render_template(
            "apply.html",
            error="Please enter your email.",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary
        )


    if not phone:

        return render_template(
            "apply.html",
            error="Please enter your phone number.",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary
        )


    if not job_title:

        return render_template(
            "apply.html",
            error="Job information is missing.",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary
        )


    # -----------------------------------------------------
    # CREATE APPLICATION
    # -----------------------------------------------------

    application = {

        "application_id":
            uuid.uuid4().hex,

        "name":
            name,

        "email":
            email,

        "phone":
            phone,

        "job_title":
            job_title,

        "company":
            company,

        "location":
            location,

        "job_type":
            job_type,

        "salary":
            salary,

        "cover_letter":
            cover_letter,

        "status":
            "Submitted"
    }


    # -----------------------------------------------------
    # SAVE APPLICATION
    # -----------------------------------------------------

    try:

        save_application(
            application
        )


    except Exception as error:

        return render_template(
            "apply.html",
            error=f"Could not submit application: {error}",
            job_title=job_title,
            company=company,
            location=location,
            job_type=job_type,
            salary=salary
        )


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return render_template(
        "application-success.html",
        application=application
    )


# =========================================================
# EMPLOYER DASHBOARD
# =========================================================

@app.route("/employer-dashboard")
def employer_dashboard():

    return render_template(
        "employer-dashboard.html"
    )


# =========================================================
# EMPLOYER APPLICATIONS
# =========================================================

@app.route("/employer-applications")
def employer_applications():

    applications = load_applications()

    return render_template(
        "employer-applications.html",
        applications=applications
    )


# =========================================================
# AI MATCHER PAGE
# =========================================================

@app.route("/matcher")
def matcher_page():

    return render_template(
        "matcher.html"
    )


# =========================================================
# MATCH ALIAS
# =========================================================

@app.route("/match")
def match_page():

    return render_template(
        "matcher.html"
    )


# =========================================================
# AI RESUME MATCH API
# =========================================================

@app.route(
    "/api/match",
    methods=["POST"]
)
def api_match():

    # -----------------------------------------------------
    # GET RESUME
    # -----------------------------------------------------

    resume_file = request.files.get(
        "resume_file"
    )


    # -----------------------------------------------------
    # GET JOB DESCRIPTION
    # -----------------------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATE RESUME
    # -----------------------------------------------------

    if not resume_file:

        return jsonify({

            "status": "error",

            "error":
                "Please upload your resume."

        }), 400


    if resume_file.filename == "":

        return jsonify({

            "status": "error",

            "error":
                "Please select a resume."

        }), 400


    if not allowed_file(
        resume_file.filename
    ):

        return jsonify({

            "status": "error",

            "error":
                "Only PDF and DOCX files are supported."

        }), 400


    # -----------------------------------------------------
    # VALIDATE JOB DESCRIPTION
    # -----------------------------------------------------

    if not job_description:

        return jsonify({

            "status": "error",

            "error":
                "Please enter a job description."

        }), 400


    # -----------------------------------------------------
    # CREATE UNIQUE FILE NAME
    # -----------------------------------------------------

    original_filename = secure_filename(
        resume_file.filename
    )


    extension = os.path.splitext(
        original_filename
    )[1]


    unique_filename = (
        uuid.uuid4().hex
        + extension
    )


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )


    # -----------------------------------------------------
    # SAVE RESUME
    # -----------------------------------------------------

    try:

        resume_file.save(
            filepath
        )


    except Exception as error:

        return jsonify({

            "status": "error",

            "error":
                f"Could not save resume: {error}"

        }), 500


    # -----------------------------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------------------------

    try:

        resume_text = extract_resume(
            filepath
        )


    except Exception as error:

        return jsonify({

            "status": "error",

            "error":
                f"Could not read resume: {error}"

        }), 500


    # -----------------------------------------------------
    # CHECK EXTRACTED TEXT
    # -----------------------------------------------------

    if not resume_text.strip():

        return jsonify({

            "status": "error",

            "error":
                "Could not extract text from the resume."

        }), 400


    # -----------------------------------------------------
    # RUN AI MATCHING
    # -----------------------------------------------------

    try:

        result = calculate_match(
            resume_text,
            job_description
        )


    except Exception as error:

        return jsonify({

            "status": "error",

            "error":
                f"AI matching failed: {error}"

        }), 500


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return jsonify({

        "status": "success",

        "filename":
            original_filename,

        **result

    })


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():

    return render_template(
        "settings.html",
        user_name=session.get(
            "name",
            "User"
        )
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "application": "MatchIQ",

        "message":
            "MatchIQ server is running successfully."

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )