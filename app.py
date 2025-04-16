from flask import Flask, render_template, send_file, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)


# --- Scraper Functions ---
def get_pib_links(parsed_date):
    """Fetch PIB press release links for a specific date using POST request simulation."""
    try:
        session = requests.Session()
        params = {'reg': '3', 'lang': '1'}

        day = str(parsed_date.day)
        month = str(parsed_date.month)
        year = str(parsed_date.year)

        # First, perform a GET request to fetch hidden fields and cookies
        response = session.get(
            'https://pib.gov.in/allRel.aspx', params=params, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        cookies = session.cookies.get_dict()

        # Helper to extract hidden field values
        def get_field(name):
            field = soup.find('input', {'name': name})
            return field['value'] if field and field.has_attr('value') else ''

        viewstate = get_field('__VIEWSTATE')
        eventvalidation = get_field('__EVENTVALIDATION')
        viewstategen = get_field('__VIEWSTATEGENERATOR')

        # Construct POST payload
        data = {
            'script_HiddenField': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlday',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategen,
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$Bar1$ddlregion': '3',
            'ctl00$Bar1$ddlLang': '1',
            'ctl00$ContentPlaceHolder1$hydregionid': '3',
            'ctl00$ContentPlaceHolder1$hydLangid': '1',
            'ctl00$ContentPlaceHolder1$ddlMinistry': '0',
            'ctl00$ContentPlaceHolder1$ddlday': day,
            'ctl00$ContentPlaceHolder1$ddlMonth': month,
            'ctl00$ContentPlaceHolder1$ddlYear': year,
        }

        # Perform POST request with cookies and payload
        post_response = session.post(
            'https://pib.gov.in/allRel.aspx',
            params=params,
            data=data,
            cookies=cookies,
            timeout=10
        )
        post_response.raise_for_status()

        post_soup = BeautifulSoup(post_response.text, 'html.parser')

        # Extract relevant links
        links = []
        for tag in post_soup.select("a[href*='PressReleasePage.aspx?PRID=']"):
            href = tag.get("href")
            if href:
                full_link = "https://pib.gov.in/" + href.lstrip("/")
                links.append({"text": tag.text, "link": full_link})

        return links

    except requests.exceptions.RequestException as e:
        print(f"[PIB] Request failed: {e}")
        return []
    except Exception as e:
        print(f"[PIB] Error occurred: {e}")
        return []


def fetch_newsonair_links(parsed_date):
    """Fetch NewsOnAir posts for ±1 day range of selected date using AJAX-based endpoint."""
    try:
        BASE_URL = 'https://www.newsonair.gov.in/wp-admin/admin-ajax.php'
        links = []

        # Get ±1 day around selected date
        date_from = (parsed_date - timedelta(days=1)).strftime("%Y-%m-%d")
        date_to = (parsed_date + timedelta(days=1)).strftime("%Y-%m-%d")
        page = 1

        while True:
            data = {
                'action': 'filter_posts_details',
                'title': '',
                'date_from': date_from,
                'date_to': date_to,
                'paged': str(page),
            }

            response = requests.post(BASE_URL, data=data, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # If "no posts" message is found, stop
            if soup.find("h6", class_="no-posts-found"):
                break

            # Parse bulletin boxes for links
            posts = soup.find_all("div", class_="bulletinBox")
            for post in posts:
                a_tag = post.find("a")
                if a_tag:
                    url = a_tag["href"]
                    links.append({"text": a_tag.text, "link": url})

            page += 1

        return links

    except requests.exceptions.RequestException as e:
        print(f"[NewsOnAir] Request failed: {e}")
        return []
    except Exception as e:
        print(f"[NewsOnAir] Error occurred: {e}")
        return []

# --- Flask Routes ---


@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for date selection and link display."""
    pib_links = []
    air_links = []
    selected_date = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        selected_date = request.form.get("selected_date")
        try:
            parsed_date = datetime.strptime(selected_date, "%Y-%m-%d")

            # Fetch links from both sources
            pib_links = get_pib_links(parsed_date)
            air_links = fetch_newsonair_links(parsed_date)

            pib_links_only = [item["link"] for item in pib_links]
            air_links_only = [item["link"] for item in air_links]

            # Save to text files
            with open("pib_links.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(pib_links_only))
            with open("air_links.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(air_links_only))
        except Exception as e:
            print(f"[Index Route] Error: {e}")

    return render_template(
        "index.html",
        pib_links=pib_links,
        air_links=air_links,
        selected_date=selected_date
    )


@app.route("/download/<source>")
def download_file(source):
    """Route to download the saved links file."""
    filename = f"{source}_links.txt"
    return send_file(filename, as_attachment=True)


# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True)
