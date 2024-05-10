import requests
import json


def calculate_rank_difference(tier1, division1, lp1, to_compare: list) -> list:
    def calculate_score(tier1, division1, lp1) -> int:
        # Define the order of tiers and divisions
        tier_order = {"IRON": 0, "BRONZE": 1, "SILVER": 2, "GOLD": 3, "PLATINUM": 4}
        division_order = {"IV": 0, "III": 1, "II": 2, "I": 3}

        # Convert tiers and divisions to numerical values
        tier_value1 = tier_order.get(tier1, 0)
        division_value1 = division_order.get(division1, 0)

        # Sum the tier and division values
        return tier_value1 * 400 + division_value1 * 100 + lp1

    total = calculate_score(tier1, division1, lp1)

    # Calculate the difference between the ranks
    results = {}
    for score in to_compare:
        tier2, division2, lp2 = score.get("values")
        difference = abs(calculate_score(tier2, division2, lp2) - total)
        results[score.get("user")] = difference
    # return results sorted by difference
    return sorted(results.items(), key=lambda x: x[1])


if __name__ == "__main__":
    # URLs
    url = "https://p1.xdx.gg/rid/1/alexanderstar-lan"
    url_live = "https://p1.xdx.gg/spectate/1/alexanderstar-lan"

    # Send a GET request to the URL
    response = requests.get(url)
    response_live = requests.get(url_live)

    if response_live.status_code == 200:
        data = json.loads(response_live.text)
        if data:
            print("AlexanderStar is playing!")
        else:
            print("AlexanderStar is not playing.")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract the required information
        solo_tier = data.get("solo-tier", "N/A")
        solo_division = data.get("solo-division", "N/A")
        solo_lp = int(data.get("solo-lp", "N/A"))

        # Print the extracted information
        print(f"AlexanderStar:\n{solo_tier} {solo_division}")
        print(f"{solo_lp} LP")

        score_to_compare = (solo_tier, solo_division, solo_lp)
        scores = [
            {"user": "Juan Becerra", "values": ("PLATINUM", "IV", 3)},
            {"user": "Sebastian", "values": ("GOLD", "I", 32)},
            {"user": "Daniel", "values": ("GOLD", "III", 50)},
            {"user": "Hugo", "values": ("GOLD", "II", 10)},
            {"user": "Elsa", "values": ("GOLD", "III", 70)},
            {"user": "Andres", "values": ("GOLD", "II", 60)},
            {"user": "Calvo", "values": ("GOLD", "IV", 74)},
            {"user": "Gavilan", "values": ("GOLD", "III", 24)},
        ]
        differences = calculate_rank_difference(*score_to_compare, scores)
        # Print the differences pretty
        print()
        print("Differences (lower is better):")
        for user, difference in differences:
            print(f"{user} - {difference}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
