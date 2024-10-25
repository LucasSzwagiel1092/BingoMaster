from fetch_data import get_item_drop_data
from drop_rate_calc import calculate_average_grinds_needed
from fractions import Fraction

def main():
    # User inputs
    points_per_grind = 100  # Replace with actual points per grind
    specific_item_name = "Chromium ingot"  # Replace with the item you want to filter
    amount_wanted = 1  # How many items you want
    grinds_per_hour = 20  # How many grinds you can do in an hour

    # Fetch drop data for the specific item
    drop_sources = get_item_drop_data(specific_item_name)

    # Loop through each monster that drops the item to calculate points/hour
    for monster, drop_chance in drop_sources:
        try:
            drop_chance_fraction = Fraction(drop_chance)
            average_grinds_needed = calculate_average_grinds_needed(drop_chance_fraction, amount_wanted)
            points_per_hour = (grinds_per_hour / average_grinds_needed) * points_per_grind

            # Print out results for each monster drop source
            print(f"Grinding for {amount_wanted} of {specific_item_name} from {monster} at a {drop_chance} drop chance...")
            print(f"Average number of grinds needed: {average_grinds_needed:.2f}")
            print(f"Points per hour: {points_per_hour:.2f}\n")

        except ValueError:
            # Handle cases where drop_chance is not a valid fraction (e.g., "Always")
            print(f"Skipping {monster} due to invalid drop chance: {drop_chance}\n")

if __name__ == "__main__":
    main()
