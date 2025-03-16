from flask import Flask, request, render_template_string, render_template
import os
import bleach

app = Flask(__name__)

# First flag in SECRET_KEY
app.config['SECRET_KEY'] = "ATHACKCTF{0HH_T00_3ASY_FL4G}"

# Second flag written to a file
FLAG_FILE_PATH = os.path.join(os.getcwd(), "flag.txt")
SECOND_FLAG = "ATH{ADVANCED_SSTI_FLAG}"

# Write the second flag to a file at startup
if not os.path.exists(FLAG_FILE_PATH):
    with open(FLAG_FILE_PATH, "w") as f:
        f.write(SECOND_FLAG)

###############################################################################
# Jinja2 Environment Configuration
###############################################################################

# Modify Jinja2 environment to allow os and _io imports
def custom_environment(app):
    from jinja2 import Environment
    env = Environment(autoescape=True)
    env.globals['os'] = __import__('os')
    env.globals['_io'] = __import__('_io')
    return env

# Restrict os access to the current folder only
def restricted_os():
    class RestrictedOS:
        def __init__(self, base_path):
            self.base_path = base_path

        def safe_path(self, path):
            full_path = os.path.abspath(os.path.join(self.base_path, path))
            if not full_path.startswith(self.base_path):
                raise ValueError("Access outside the current folder is restricted.")
            return full_path

        def listdir(self, path="."):
            return os.listdir(self.safe_path(path))

        def open(self, path, mode="r"):
            return open(self.safe_path(path), mode)

        def __getattr__(self, name):
            # Restrict destructive methods
            if name in ["remove", "rmdir", "rename"]:
                raise AttributeError(f"Access to {name} is restricted.")
            return getattr(os, name)

    return RestrictedOS(os.getcwd())

# Update the Flask Jinja2 environment
def enable_custom_jinja_env(app):
    app.jinja_env.globals.update(
        os=restricted_os(),
        _io=__import__('_io')
    )

enable_custom_jinja_env(app)

###############################################################################
# Bleach-based Sanitization
###############################################################################

def sanitize_input(user_input):
    """
    Sanitize user input using bleach, which removes or escapes
    harmful HTML/JS. This helps mitigate XSS, but does NOT
    prevent Server-Side Template Injection (SSTI).
    """
    return bleach.clean(user_input)

###############################################################################
# Routes
###############################################################################

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Vulnerable route
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        user_input = request.form.get('input', '')
        try:
            # Clean user input with bleach to prevent XSS
            cleaned_input = sanitize_input(user_input)
            
            # But still render it with Jinja -> potential SSTI
            rendered_output = render_template_string(cleaned_input)
            return render_template('response.html', output=rendered_output)
        except Exception as e:
            return f"Error: {e}", 400
    return render_template('submit.html')

# Memory dump route
@app.route('/memory_dump')
def memory_dump():
    # Example sensitive data (challenge target)
    killcode = "Nope! You're not getting the killcode!"
    return render_template('memory_dump.html', killcode=killcode)

if __name__ == "__main__":
    app.run(debug=True)
