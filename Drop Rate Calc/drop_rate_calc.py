from fractions import Fraction

def calculate_average_grinds_needed(drop_chance_fraction, amount_wanted):
    # Convert drop chance fraction to decimal
    drop_chance_decimal = float(drop_chance_fraction)

    # Average number of grinds needed to get the desired amount of items
    average_grinds_needed = amount_wanted / drop_chance_decimal

    return average_grinds_needed

def calculate_points_per_hour(points_per_grind, average_grinds_needed, grinds_per_hour):
    # Total points you would get from the average number of grinds
    total_points = average_grinds_needed * points_per_grind

    # Points per hour calculation
    points_per_hour = grinds_per_hour * points_per_grind

    return points_per_hour
