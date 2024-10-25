import logging
from flask import Flask, request, render_template
from flask_cors import CORS
from fetch_data import get_item_drop_data
from drop_rate_calc import calculate_average_grinds_needed
from fractions import Fraction

app = Flask(__name__)
CORS(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DEBUG'] = True

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    item_name = ""
    points_per_grind = ""
    amount_wanted = ""
    grinds_per_hour = ""
    error_message = ""

    if request.method == "POST":
        logging.debug("Received POST request")
        # Get the user input from the form
        item_name = request.form.get("item_name")
        points_per_grind = request.form.get("points_per_grind")
        amount_wanted = request.form.get("amount_wanted")
        grinds_per_hour = request.form.get("grinds_per_hour")

        logging.debug(f"Item name: {item_name}, Points per grind: {points_per_grind}, Amount wanted: {amount_wanted}, Grinds per hour: {grinds_per_hour}")

        try:
            # Convert inputs to appropriate types
            points_per_grind = int(points_per_grind)
            amount_wanted = int(amount_wanted)
            grinds_per_hour = int(grinds_per_hour)

            # Fetch drop data for the specific item
            drop_sources = get_item_drop_data(item_name)

            if not drop_sources:
                    error_message = f"The item '{item_name}' does not exist or does not have a drop rate table."
            else:

                # Loop through each monster that drops the item to calculate points/hour
                for monster, drop_chance in drop_sources:
                    try:
                        drop_chance_fraction = Fraction(drop_chance)
                        average_grinds_needed = calculate_average_grinds_needed(drop_chance_fraction, amount_wanted)
                        points_per_hour = (grinds_per_hour / average_grinds_needed) * points_per_grind

                        # Add each drop source to the result list
                        result.append({
                            "monster": monster,
                            "drop_chance": drop_chance,
                            "average_grinds_needed": average_grinds_needed,
                            "points_per_hour": points_per_hour
                        })

                    except ValueError:
                        # Handle cases where drop_chance is not a valid fraction (e.g., "Always")
                        result.append({
                            "monster": monster,
                            "drop_chance": drop_chance,
                            "error": "Invalid drop chance"
                        })
        except (ValueError, TypeError):
            # If any input conversion fails, add an error message
            error_message = "Invalid input. Please enter valid numbers."

    # Pass the input data and result to the template
    return render_template("index.html", 
                           result=result,
                           item_name=item_name,
                           points_per_grind=points_per_grind,
                           amount_wanted=amount_wanted,
                           grinds_per_hour=grinds_per_hour,
                           error_message=error_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
