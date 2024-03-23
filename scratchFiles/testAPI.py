# from bs4 import BeautifulSoup
# import requests

# url = "https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# table = soup.find("table") #Caso precise identificar tabela não precisou
# headers = [header.text.strip() for header in table.find_all("th")] # Extrair os cabeçalhos da tabela
# headers.insert(0, 'Posição:')
# headers.insert(1, '')
# headers.insert(3, 'Status')
# # Extrair os dados da tabela
# data = []
# data2 = []

# for row in table.find_all("tr"):
#     print(row)
#     print('')
#     images = row.findAll('img')
#     row_image = ''
#     for image in images:
#        row_image = image['src']
#     row_data = [cell.text.strip() for cell in row.find_all("td")]
#     if row_data:
#        row_data[1] = row_image
#        data.append(row_data)
#        data2.append(row_image)


# #Print dados
# print(headers)
# for row in data:
#   print(row)
    
from datetime import datetime

data = [
    {'user': 'User 1', 'pontuacao': 55, 'data_confirmacao': datetime(2024, 3, 5, 1, 9, 24)},
    {'user': 'User 2', 'pontuacao': 65, 'data_confirmacao': datetime(2024, 3, 5, 1, 3, 22)},
    {'user': 'User 3', 'pontuacao': 40, 'data_confirmacao': datetime(2024, 4, 5, 3, 6, 29)},
    {'user': 'User 4', 'pontuacao': 65, 'data_confirmacao': datetime(2024, 3, 6, 1, 7, 24)},
    {'user': 'User 5', 'pontuacao': 15, 'data_confirmacao': datetime(2024, 6, 10, 6, 7, 21)},
    {'user': 'User 6', 'pontuacao': 100, 'data_confirmacao': datetime(2024, 3, 5, 4, 7, 22)}
]

sorted_data = sorted(data, key=lambda x: (-x['pontuacao'], x['data_confirmacao']))

for entry in sorted_data:
    print(entry)