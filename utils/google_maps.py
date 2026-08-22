from config import GOOGLE_MAPS_API_KEY


def get_maps_link(lat: float, lon: float) -> str:
    """A clickable Google Maps link. Works without any API key."""
    return f"https://www.google.com/maps?q={lat},{lon}"


def get_static_map_url(lat: float, lon: float, zoom: int = 16, size: str = "600x300"):

    if not GOOGLE_MAPS_API_KEY:
        return None

    return (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?center={lat},{lon}&zoom={zoom}&size={size}"
        f"&markers=color:red%7C{lat},{lon}"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )
