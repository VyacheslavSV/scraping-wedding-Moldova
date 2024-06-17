import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FILE_URL_LIST = 'persons_url_list.txt'
DEFAULT_KEYWORDS = 'Wedding venues places Moldova'
DEFAULT_FILE_JSON = 'data_all_companies.json'


def get_driver():
    """
    Initializes and returns a Selenium WebDriver instance with headless Chrome options.

    Returns:
        webdriver.Chrome: A configured Chrome WebDriver instance.
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver


def parser_results_in_page(user_keywords: str) -> list[str]:
    """
    Scrapes Google Maps for wedding venues in Moldova and extracts URLs of individual venues.

    Args:
        keywords(str): Keywords to search for on Google Maps.

    Returns:
        list[str]: A list of URLs of individual wedding venues.
    """
    driver = get_driver()
    results = []
    try:
        keywords_for_url = '+'.join(user_keywords.split())
        driver.get(f'https://www.google.com/maps/search/{keywords_for_url}/')

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
        except Exception:
            pass

        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        driver.execute_script("""
              var scrollableDiv = arguments[0];
              function scrollWithinElement(scrollableDiv) {
                  return new Promise((resolve, reject) => {
                      var totalHeight = 0;
                      var distance = 1000;
                      var scrollDelay = 3000;

                      var timer = setInterval(() => {
                          var scrollHeightBefore = scrollableDiv.scrollHeight;
                          scrollableDiv.scrollBy(0, distance);
                          totalHeight += distance;

                          if (totalHeight >= scrollHeightBefore) {
                              totalHeight = 0;
                              setTimeout(() => {
                                  var scrollHeightAfter = scrollableDiv.scrollHeight;
                                  if (scrollHeightAfter > scrollHeightBefore) {
                                      return;
                                  } else {
                                      clearInterval(timer);
                                      resolve();
                                  }
                              }, scrollDelay);
                          }
                      }, 200);
                  });
              }
              return scrollWithinElement(scrollableDiv);
      """, scrollable_div)

        items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

        for item in items:
            try:
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                if link:
                    results.append(link)
                time.sleep(2)  # Pause between requests
            except Exception:
                pass

        return results
    finally:
        driver.quit()
        time.sleep(40)  # Pause between series of requests


def save_file_with_urls_list(persons_list: list[str]) -> None:
    """
    Saves a list of URLs to a text file.

    Args:
        persons_list (list[str]): List of URLs to save.
    """
    with open(FILE_URL_LIST, 'a') as file:
        for line in persons_list:
            file.write(f'{line}\n')


def read_file_url_list() -> list[str]:
    """
    Reads URLs from a text file into a list.

    Returns:
        list[str]: List of URLs.
    """
    with open(FILE_URL_LIST) as file:
        lines = [line.strip() for line in file]
        return lines


def parser_personal_page(urls: list[str]):
    """
        Parses individual company pages to extract information such as company name, rate, location, image, and URL.

        Args:
            urls (list[str]): List of URLs to parse.

        Returns:
            list[dict]: List of dictionaries containing company information.
        """
    results = []
    for url in urls:
        driver = get_driver()
        try:
            driver.get(url)
            data_html = driver.page_source
            soup = BeautifulSoup(data_html, 'html.parser')

            try:
                company_name = soup.find('h1', {'class': 'DUwDvf lfPIob'}).text
            except AttributeError:
                company_name = None

            try:
                company_rate = soup.find('div', {'class': 'LBgpqf'}).find('span').text
            except AttributeError:
                company_rate = None

            try:
                location_company = soup.find('div', {'class': 'rogA2c'}).text
            except AttributeError:
                location_company = None

            try:
                image_company = soup.find('div', {'class': 'RZ66Rb FgCUCc'}).find('img').get('src')
            except AttributeError:
                image_company = None

            try:
                url_company = soup.find('a', {'class': 'CsEnBe'}).get('href')
            except AttributeError:
                url_company = None

            data = {
                'company_name': company_name,
                'company_rate': company_rate,
                'location_company': location_company,
                'image_company': f'=IMAGE("{image_company}", 4, 100, 100)',
                'url_company': url_company,
            }

            results.append(data)
            time.sleep(2)  # Pause between requests
        finally:
            driver.quit()
            time.sleep(5)  # Pause between series of requests
    return results


def create_json_file(data_list: list[dict[str, list[str]]]) -> None:
    """
    Creates a JSON file from a list of dictionaries containing company information.

    Args:
        data_list (list[dict[str, list[str]]]): List of dictionaries with company data.
    """
    with open(DEFAULT_FILE_JSON, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, indent=3, ensure_ascii=False)


def starts_cod_to_parse(user_keywords: str = DEFAULT_KEYWORDS):
    """
        Initiates the parsing process by searching for specified keywords on Google Maps,
        extracting URLs of individual venues, parsing their details, and saving the data
        to a JSON file.

        Args:
            user_keywords (str, optional): Keywords to search for on Google Maps. If not provided,
                                          DEFAULT_KEYWORDS ('Wedding venues places Moldova') will be used.

        Returns:
            None

        Raises:
            Exception: If an error occurs during any step of the parsing process.

        This function starts by fetching URLs of venues based on the provided or default keywords,
        saves these URLs to a text file, reads them back for parsing individual pages, extracts
        relevant details such as company name, rate, location, image URL, and webpage URL for each
        venue, stores these details in a list of dictionaries, and finally creates a JSON file
        ('data_all_companies.json') containing all parsed data.

        Example usage:
            starts_cod_to_parse()           # Searches for 'Wedding venues places Moldova' on Google Maps
            starts_cod_to_parse('london')   # Searches for 'london' on Google Maps
        """
    try:
        url_list = parser_results_in_page(user_keywords)
        save_file_with_urls_list(url_list)
        lines = read_file_url_list()
        data_list = parser_personal_page(lines)
        create_json_file(data_list)
        print(f'Parsed data successfully saved to {DEFAULT_FILE_JSON}')
    except Exception as e:
        print(f"An error occurred during parsing: {str(e)}")


if __name__ == "__main__":
    starts_cod_to_parse()
