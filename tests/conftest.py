import os
import sys

from pathlib import Path
from selenium.webdriver.chrome.options import Options


DRIVER_VERSION = "116.0.5802.0"
CHROME_BINARY_VERSION = f"mac-{DRIVER_VERSION}"
# Ensure the project root is on sys.path so `import_app("app")` works when
# pytest is invoked from a different working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def pytest_setup_options():
    """Hook used by dash.testing to configure Chrome options.

    Keeps a local binary path (useful for Google Chrome for Testing),
    adds safer defaults for CI (headless, no-sandbox), and returns the
    Options object expected by dash testing.
    """
    options = Options()

    # Use a local 'Google Chrome for Testing' binary if present. Adjust this
    # path to your system if needed; leaving it here is convenient for local
    # setups that use a pinned Chrome build.
    chrome_binary = (
        Path.home()
        / "Development"
        / "Binaries"
        / "chrome"
        / f"{CHROME_BINARY_VERSION}"
        / "chrome-mac-x64"
        / "Google Chrome for Testing.app"
        / "Contents"
        / "MacOS"
        / "Google Chrome for Testing"
    )

    if chrome_binary.exists():
        options.binary_location = str(chrome_binary)

    # Recommended options for headless CI-friendly execution
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # With browser
    # options.add_argument("--disable-infobars")
    # options.add_argument('--disable-features=SidePanelPinning')

    return options


def _add_driver_dir_to_path(driver_path: str) -> None:
    """Add the directory containing `driver_path` to PATH if not present."""
    if not driver_path:
        return

    driver_dir = str(Path(driver_path).parent)
    current_path = os.environ.get("PATH", "")

    if driver_dir not in current_path.split(os.pathsep):
        os.environ["PATH"] = driver_dir + os.pathsep + current_path


try:
    from webdriver_manager.chrome import ChromeDriverManager
except Exception:
    ChromeDriverManager = None


def pytest_configure(config):
    """Pytest hook: attempt to ensure a chromedriver is available on PATH.

    This is non-fatal: if `webdriver-manager` isn't installed we don't crash —
    but having `webdriver-manager` will download a chromedriver matching the
    locally installed Chrome and add it to PATH automatically which helps
    avoid SessionNotCreatedException errors arising from missing/mismatched
    drivers.
    """
    if ChromeDriverManager is None:
        return

    try:
        driver_path = ChromeDriverManager(
            driver_version=DRIVER_VERSION).install()

        _add_driver_dir_to_path(driver_path)
    except Exception:
        # Don't raise here; tests will fail later with clearer selenium errors
        # if a driver can't be downloaded or installed.
        pass
