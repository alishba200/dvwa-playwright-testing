# DVWA Testing with Playwright and Python

Complex Engineering Activity (CEA) by Alishba Sardar and Bisma Ahmed.

## Setup
1. Run DVWA: `docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa`
2. Open http://localhost:8080/setup.php and click Create / Reset Database
3. Install tools: `pip install -r requirements.txt` then `playwright install`

## Run the tests
`pytest --browser chromium --browser firefox --browser webkit --html=report_all.html`

## Contents
- `tests/`: 18 tests (12 end-to-end, 4 API, 2 network mocking)
- `screenshots/`: screenshots saved by the tests
- `report_all.html`: results on 3 browsers (46 passed)
- `report_bug.html`: results with the intentional bug (6 failed)
- `STS_CEA_Report.docx`: final report
