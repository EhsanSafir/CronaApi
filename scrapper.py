import requests


class WorldMeterScrapper:
    STATIC_URL = 'https://www.worldometers.info/coronavirus/'
    data = {}

    @staticmethod
    def load_page():
        return requests.get(WorldMeterScrapper.STATIC_URL)

    @staticmethod
    def page_status(page):
        return page.status_code

    @staticmethod
    def create_soup(data):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')
        return soup

    @staticmethod
    def get_table(soup):
        table_all_data = []

        def get_table_header():
            table = soup.find('thead')
            heads = table.find_all('th')
            head_list = []
            for head in heads:
                head_list.append(head.text.strip())
            table_all_data.append({"head": head_list})

        def get_table_data():
            rows = soup.find_all("tr")
            table_data = []
            for row in rows[1:]:
                lst = []
                for data in row.find_all('td'):
                    dat = '0' if data.text.strip() == '' else data.text
                    lst.append(dat)
                table_data.append(lst)
            table_all_data[0]['body'] = table_data
            print()
        get_table_header()
        get_table_data()
        return table_all_data

    @staticmethod
    def get_basic_data(soup):
        data = {}
        heading = soup.find_all('div', {"id": "maincounter-wrap"})
        for part in heading:
            key = part.find_all('h1')[0].text
            value = part.find_all('span')[0].text
            data[key] = value
        return data

    @staticmethod
    def get_all_div(soup):
        data = {}
        active_close = soup.find_all('div', {'class': 'panel panel-default'})
        for i, part in enumerate(active_close):
            if i < 2:
                pack = part.find('div', {'class': 'panel-heading'})
                # print("================")
                # print(pack.text.strip())
                key1 = part.find('div', {'style': 'font-size:13.5px'}).text
                value1 = part.find('div', {'class': 'number-table-main'}).text
                # print(f'{key1} : {value1}')
                key2 = part.find_all('div', {'style': 'font-size:13px'})[0].text
                value2 = part.find_all('span', {'class': 'number-table'})[0].text
                value22 = part.find_all('strong')[0].text
                # print(f'{key2} : {value2} {value22}')
                key3 = part.find_all('div', {'style': 'font-size:13px'})[1].text
                value3 = part.find_all('span', {'class': 'number-table'})[1].text
                value33 = part.find_all('strong')[1].text
                # print(f'{key3} : {value3} {value33}')
                data[pack.text] = [
                    {
                        key1: value1,
                        key2: [
                            value2, value22
                        ],
                        key3: [
                            value3, value33
                        ]
                    }
                ]
            else:
                # print("===========")
                pack = part.find('div', {'class': 'panel-heading'})
                # print(pack.text)
                content = part.find('div', {'style': 'font-size:24px; color:#999; font-weight:bold;'}).text
                # print(content)
                data[pack.text] = content
                # print(data)
        return data
