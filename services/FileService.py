"""
SERVIÇOS PARA MANIPULAÇÃO DE ARQUIVOS E DIRETORIOS
"""

import os 
import shutil
import time
from config.settings import TEMP_DIR, UPLOADS_DIR

class FileService:
    """
    CLASSE PARA A MANIPULAÇÃO DE ARQUIVOS E DIRETÓRIOS
    """
    @staticmethod
    def createBaseDirs():
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(UPLOADS_DIR, exist_ok=True)

    @staticmethod
    def copyDir(origin, destiny):
        """
        RETORNA UM BOOL INFORMANDO SE A OPERAÇÃO FOI BEM SUCEDIDA
        """
        try:
            shutil.copytree(origin, destiny)
            return True, f'diretório copiado para {destiny}'
        except Exception as e:
            return False, f'erro ao copiar diretório: {e}'

    @staticmethod
    def copyFile(origin, destiny):
        """
        BOOL IGUAL O COPYDIR
        """
        try:
            shutil.copyfile(origin, destiny)
            return True, f'arquivo copiado para {destiny}'
        except Exception as e:
            return False, f'erro ao copiar arquivo: {e}'

    @staticmethod
    def removeFile(path):
        try:
            os.remove(path)
            return True, f'arquivo removido: {path}'
        except Exception as e:
            return False, f'erro ao remover arquivo: {e}'
        
    @staticmethod
    def removeDir(path):
        try:
            shutil.rmtree(path)
            return True, f'diretorio removido: {path}'
        except Exception as e:
            return False, f'erro ao remover diretorio: {e}'
        
    @staticmethod
    def generateUniqueName(dirPath):
        """
        GERA UM NOME ÚNICO PRO ARQUIVO COM O TIMESTAMP, PARA QUE NÃO HAJA CONFLITO DE NOME NÉ 
        """

        nomeArquivo = os.path.basename(dirPath)
        timeStamp = time.strftime("%Y%m%d_%H%M%S")
        return f'{nomeArquivo}_{timeStamp}'
    
    @staticmethod
    def createLabelDir(labelName):
        finalDir = os.path.join(UPLOADS_DIR, labelName)
        os.makedirs(finalDir, exist_ok=True)
        return finalDir