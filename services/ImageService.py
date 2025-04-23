"""
SERVIÇOS ESPECÍFICOS PARA A MANIPULAÇÃO DE IMAGENS
"""

import os 
import imghdr
from services.FileService import FileService

class ImageService:

    @staticmethod
    def validateImage(imgPath):
        """
        VERIFICA SE UM ARQUIVO É UMA IMAGEM VÁLIDA

        ARGS:
            imgPath(str): CAMINHO PRO ARQUIVO A SER VALIDADE

        RETURNS: 
            bool: True caso seja uma imagem válida
        """

        imgType = imghdr.what(imgPath)
        return imgType is not None
    
    @staticmethod
    def processImgDir(dirPath, labelname):
        """
        PROCESSA TODAS AS IMAGENS EM UMA PASTA, MANTENDO APENAS OS FORMATOS DE IMAGEM ACEITOS PELO PROGRAMA

        ARGS: 
            dirPath(str): caminho da pasta a ser varrida
            labelName(str): nome do label que a pasta foi arrastada(que vai ser o nome da pasta final)

        RETURNS:
            list: lista de resultados de processamento para cada arquivo
        """

        results = []
        destinyDir = FileService.createLabelDir(labelname)

        for file in os.listdir(dirPath):
            filePath = os.path.join(dirPath, file)

            if os.path.isfile(filePath):
                #verifica se e uma imagem mesmo
                if ImageService.validateImage(filePath):
                    #é uma imagem válida, copia para a pasta final
                    destinyPath = os.path.join(destinyDir, file)
                    success, msg = FileService.copyFile(filePath, destinyPath)

                    if success:
                        FileService.removeFile(filePath)
                    
                    results.append((success, msg))
                
                else:
                    #n é uma img, apaga da temp daí 
                    success, img = FileService.removeFile(filePath)
                    results.append((False, f'arquivo {filePath} não é uma imagem válida'))
            else:
                #se for um diretório e nao um arquivo, ele remove também
                success, msg = FileService.removeDir(filePath)
                results.append((False, 'subdiretório removido'))

        return results
