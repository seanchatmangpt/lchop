import yaml
from flask import Flask, render_template

app = Flask(__name__)

# template root
ystr = """administration_module:
  description: "A specific type of object"
  look_and_feel:
    - description: "Object with methods for dealing with the look and feel"
    - set_theme
    - customize_layout
  security:
    - description: "Object with methods for dealing with security in a Federated security framework"
    - authenticate_user
    - authorize_access
  information:
    - description: "Object with methods for drawing information from and having audit trails for all modules within this suite"
    - query_data
    - log_activity
  decision_making:
    - description: "Object with methods for interfacing back to the decision-making facility"
    - send_request
    - receive_response

# Classes
module:
  - description: "Class for any module within this application suite"
  - information
  - decision_making

# Interfaces
common_interface:
  - description: "Interface for connecting methods that link to other methods"
  - query_data
  - log_activity
  - send_request
  - receive_response
  """


@app.route("/")
def index():
    yaml_data = yaml.safe_load(ystr)
    return render_template("index.html", yaml_data=yaml_data)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
