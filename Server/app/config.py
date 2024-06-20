from os import path

def get_env_file() -> str:
    
    topPath = path.join(path.dirname(path.dirname(path.abspath(__file__))), '.env')

    if path.exists(topPath): return topPath
    return '.env'
