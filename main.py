from bs4 import BeautifulSoup
import requests
import csv


def get_data(url):

    headers = {
         'Accept': '*/*',
         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
    }

    names, links, types = [], [], []

    for page in range(1, 16):
        print(f'Page: {page} done !')

        req = requests.get(url + f'page={page}', headers=headers)

        src = req.text

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(src)

        with open('index.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            names.extend([div.text for div in soup.select('.item .photo a .desk .t')])
        except Exception:
            names = "No data"

        try:
            links.extend(["https://rud.ua" + a["href"] for a in soup.select('.item .photo a')])
        except Exception:
            links = "No data"

        try:
            types.extend([div.text.strip() for div in soup.select('.item .photo a .desk .date')])
        except Exception:
            types = "No data"

        # res = list(map(lambda name, type_, link: f'{name}, {type_}, {link}', names, types, links))
        # print(*res, sep='\n')

    return list(map(lambda n, t, l: [n, t, l], names, types, links))  # return tuple (names, types, links)


def make_csv(data, filename):
    print(*data, sep='\n')
    with open(f'data_csv/{filename}.csv', 'w', encoding="cp1251", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        for idx in range(len(data)):
            writer.writerow(
                (
                    data[idx][0],
                    data[idx][1],
                    data[idx][2]
                )
            )


def main():
    rud_data = get_data('https://rud.ua/consumer/recipe/')
    make_csv(rud_data, 'rud')


if __name__ == "__main__":
    main()
