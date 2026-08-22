import requests


def is_valid_coordinate(lat: float, lon: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lon <= 180


def reverse_geocode(lat: float, lon: float) -> str:
    if not is_valid_coordinate(lat, lon):
        return "Invalid coordinates"

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "road-damage-detector-app"},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("display_name", f"{lat}, {lon}")
    except Exception:
        return f"{lat}, {lon} (address lookup unavailable)"
