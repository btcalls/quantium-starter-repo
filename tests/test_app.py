from dash.testing.application_runners import import_app
from app import HEADER, GRAPH_ID, RADIO_ID


def test_001_header_present(dash_duo):
    """Test that the header is present and rendered."""
    app = import_app("app")

    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", HEADER, timeout=4)


def test_002_visualisation_present(dash_duo):
    """Test that the visualisation (line graph) is present and rendered."""
    app = import_app("app")

    dash_duo.start_server(app)

    assert dash_duo.find_element(f"#{GRAPH_ID}") is not None


def test_003_region_picker_present(dash_duo):
    """Test that the region picker (RadioItems) is present and rendered."""
    app = import_app("app")

    dash_duo.start_server(app)

    # Verify the RadioItems container exists
    radio_element = dash_duo.find_element(f"#{RADIO_ID}")
    assert radio_element is not None

    # Verify the "Region:" label is present
    label = dash_duo.find_element("label")
    assert label is not None
    assert "Region:" in label.text
