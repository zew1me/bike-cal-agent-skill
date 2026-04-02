from pnw_bike_events.registry import classify_family, family_by_slug


def test_classify_family_ride_vicious() -> None:
    assert classify_family("Vicious - Heaven of the South") == "ride-vicious"


def test_family_lookup() -> None:
    family = family_by_slug("cyclocross-series")
    assert family.title == "Cyclocross Series"


def test_classify_family_wider_pnw() -> None:
    assert classify_family("Rebecca's Private Idaho") == "wider-pnw"
