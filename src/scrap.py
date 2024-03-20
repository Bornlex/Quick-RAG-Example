from bs4 import BeautifulSoup, Tag


def parse_information_one_result(element: Tag):
    try:
        ref_cons_value = element.find_all('div', class_='m-b-1')[0].find('div').text.strip()
        procedure_type = element.find('div', class_='cons_procedure').span.text.strip()
        category = element.find('div', class_='cons_categorie').span.text.strip()

        day = element.find('div', class_='date date-min clearfix').find('div', class_='day').span.text.strip()
        month = element.find('div', class_='month').span.text.strip()
        year = element.find('div', class_='year').span.text.strip()
        date = f"{day} {month} {year}"

        object_description = element.find_all('div', class_='m-b-1')[1].find('div').text.split(':')[1].strip()
        organism_info = element.find_all('div', class_='m-b-1')[2].find('div').text.split(':')[1].strip()
    except Exception as e:
        return None, e

    return {
        'reference': ref_cons_value,
        'procedure_type': procedure_type,
        'category': category,
        'date': date,
        'object_description': object_description,
        'organism_info': organism_info
    }, None


def extract_results(html_content: str):
    parsed_results = []

    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all('div', class_='item_consultation')
    for result in results:
        if not isinstance(result, Tag):
            continue
        result, e = parse_information_one_result(result)
        if result:
            parsed_results.append(result)

    return parsed_results
