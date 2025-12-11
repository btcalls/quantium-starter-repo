# Quantium Starter Repository

A Python Dash application for analyzing Pink Morsel sales data with automated testing and CI-friendly browser automation.

## Project Structure

```
.
├── app.py                 # Main Dash application
├── utils.py               # Utility functions for data processing
├── tests/
│   ├── conftest.py        # Pytest configuration and Chrome setup
│   └── test_app.py        # Integration tests using Dash testing
├── data/
│   ├── daily_sales_data_*.csv
│   └── combined_sales_data.csv
├── Pipfile                # Pipenv dependency manifest
├── Pipfile.lock           # Locked dependencies
└── README.md              # This file
```

## Setup

### Prerequisites

- **Python 3.13** (as specified in `Pipfile`)
- **Pipenv** (for dependency management): `pip install pipenv` or `brew install pipenv`
- **Git**

### Environment Setup with Pipenv

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repo-url>
   cd quantium-starter-repo
   ```

2. **Install dependencies**:
   ```bash
   pipenv install
   ```
   This installs:
   - `pandas` for data processing
   - `dash[testing]` for the web app and integration testing
   - `webdriver-manager` (dev) for automatic Chromedriver management

3. **Verify the environment**:
   ```bash
   pipenv run python --version
   pipenv run pip list | grep -E "dash|pandas"
   ```

## Running the Dash Application

### Start the development server:

```bash
pipenv run python app.py
```

The app will be available at **http://localhost:8050** (or the port specified in `app.py`).

**Features:**
- Interactive visualizations of Pink Morsel sales data
- Radio buttons to filter or select time periods
- Responsive layout with Plotly graphs

### Notes:
- The development server hot-reloads on file changes.
- Press `Ctrl+C` to stop the server.
- To run on a custom host/port, edit the `app.run_server()` call in `app.py`.

## Downloading Chrome for Testing Binary

The test suite uses Selenium to automate Chrome. You can either:

### Option A: Use `@puppeteer/browsers` CLI via `npm`

```bash
# Download a specific Chrome for Testing version.
npx @puppeteer/browsers install chrome@116.0.5802.0
```

### Option B: Use Google Chrome for Testing (Pinned Version)

Google Chrome for Testing is a production-like build useful for reproducible CI. Download from:
[https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

**Steps:**

1. Download the macOS (Intel or Apple Silicon) `.zip` file for your desired version.
2. Extract it to a local directory (e.g., `~/Development/Binaries/chrome/`).
3. Make it executable:
   ```bash
   chmod +x ~/Development/Binaries/chrome/mac-*x64/Google\ Chrome\ for\ Testing.app/Contents/MacOS/Google\ Chrome\ for\ Testing
   ```
4. Update `tests/conftest.py` to specify the version of the binaries downloaded:
   ```python
   DRIVER_VERSION = "116.0.5802.0"
   CHROME_BINARY_VERSION = f"mac-{DRIVER_VERSION}"
   ```
5. Point to the path of your extracted binary:
   ```python
   chrome_binary = Path.home() / "Development" / "Binaries" / "chrome" / f"{CHROME_BINARY_VERSION}" / "chrome-mac-x64" / ...
   ```

**Note:** The `conftest.py` will auto-detect and use the local binary if it exists; otherwise, `webdriver-manager` will download a matching Chromedriver.

## Running Tests

### Run all tests:

```bash
pipenv run pytest -q
```

### Run tests with verbose output:

```bash
pipenv run pytest -v -q
```

### Run a specific test:

```bash
# id of the test case (e.g. test_003_sample)
pipenv run pytest -v -k 003
```

### What the tests do:

- **`test_001_header_present`**: Verifies the main header displays "Soul Foods's Pink Morsel Sales Analysis".
- **`test_002_visualisation_present`**: Verifies that the line chart visualisations was present and rendered.
- **`test_003_region_picker_present`**: Verifies that the region picker was present and rendered.

### Test Architecture:

- **`conftest.py`**: Configures Selenium/Chrome and ensures the project root is on `sys.path` for `import_app()`.
- **Dash Testing**: Uses `dash_duo` fixture (provided by `dash[testing]`) to start the app server and interact with it.
- **Chrome Options**: Tests run with headless flags by default (configured in `conftest.py`). Comment headless flags if you wish to open the browser when testing.

### Troubleshooting Tests:

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'app'` | Project root not on `sys.path` | Run pytest from repo root: `cd /path/to/repo && pipenv run pytest` |
| `SessionNotCreatedException` | ChromeDriver version mismatch or missing | `pipenv run python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"` |
| `WebDriverException: ... wrong permissions` | Chrome binary not executable | `chmod +x /path/to/Chrome.app/Contents/MacOS/Google\ Chrome` |
| Tests hang or timeout | Browser not headless in CI, or slow system | Uncomment `--headless=new` in `conftest.py` |

## Development Workflow

### Install new packages:

```bash
# Add a regular dependency
pipenv install <package-name>

# Add a dev dependency (for testing, linting, etc.)
pipenv install --dev <package-name>
```

### Update dependencies:

```bash
pipenv update
```

## CI/CD Notes

For continuous integration (GitHub Actions, GitLab CI, etc.):

1. Use `pipenv install --deploy` to install dependencies from `Pipfile.lock` (no updates).
2. Uncomment headless Chrome options in `conftest.py` to avoid UI overhead.
3. Ensure the CI environment has Python 3.13 available.
4. `webdriver-manager` will auto-download a matching Chromedriver; no manual intervention needed.

Example GitHub Actions snippet:
```yaml
- name: Install dependencies
  run: |
    pip install pipenv
    pipenv install --deploy --dev

- name: Run tests
  run: pipenv run pytest -q
```

## Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Pipenv Documentation](https://pipenv.pypa.io/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Webdriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)

