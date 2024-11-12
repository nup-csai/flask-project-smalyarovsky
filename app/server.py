from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# TODO implement as a class
supply_examples = [
    {
        "name": "milk",
        "divisible": True,
        "amount": 1000,
        "units": "mL",
        "calories": 420,
        "proteins": 10.0,
        "fats": 34.0,
        "carbohydrates": 50.0,
        "price": 1.55
    },
    {
        "name": "snickers",
        "divisible": False,
        "calories": 488,
        "proteins": 7.0,
        "fats": 24.0,
        "carbohydrates": 73.0,
        "price": 1.1
    }
]


@app.route("/list")
def list():
    message = {
        "status": 200,
        "message": "OK",
        "list": supply_examples
    }
    return jsonify(message)


@app.route("/add", methods=["POST"])
def add():
    supply = dict()
    try:
        supply["name"] = request.args.get("name")
        divisible = request.args.get("divisible")
        assert(divisible == "true" or divisible == "false")
        supply["divisible"] = (divisible == "true")
        if supply["divisible"]:
            supply["amount"] = int(request.args.get("amount"))
            supply["units"] = int(request.args.get("units"))
        supply["calories"] = int(request.args.get("units"))
        supply["proteins"] = float(request.args.get("units"))
        supply["fats"] = float(request.args.get("units"))
        supply["carbohydrates"] = float(request.args.get("units"))
        supply["price"] = float(request.args.get("units"))
    except Exception as e:
        message = {
            "status": 400,
            "message": "Invalid arguments"
        }
        return jsonify(message)
    message = {
        "status": 200,
        "message": "OK"
    }
    supply_examples.append(supply)
    return jsonify(message)

