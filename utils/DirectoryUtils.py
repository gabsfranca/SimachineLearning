"""
FUNÇÕES DE UTILIDADE PARA A MANIPULAÇÃO DE DIRETÓRIOS
"""

import os 
from config.settings import TEMP_DIR
from services.FileService import FileService

def cleanTemp():
    """
    REMOVE O DIRETORIO TEMP E O SEU CONTEÚDO 

    RETURNS:
        tuple(bool, str): se a operação foi bem sucedida, e uma mensagem
    """

    if os.path.exists(TEMP_DIR):
        return FileService.removeDir(TEMP_DIR)
    return True, 'Nenhuma limpeza necessária'
    
def createUniqueDestinyPath(originalPath):
    """
    CRIA UM CAMINHO DE DESTINO ÚNICO TEMPORÁRIO

    ARGS:
        originalPath(str): caminho original do diretório

    Returns:
        str: caminho único do diretório temporário
    """

    uniqueName = FileService.generateUniqueName(originalPath)
    return os.path.join(TEMP_DIR, uniqueName)
