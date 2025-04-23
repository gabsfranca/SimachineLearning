import os
import customtkinter as ctk
from tkinterdnd2 import DND_FILES

from config.settings import LABEL_CONFIG
from services.FileService import FileService
from services.ImageService import ImageService
from utils.DirectoryUtils import createUniqueDestinyPath

class DragLabel:
    """
    Classe pra encapsular a funcionalidade do label com suporte a drag n drop
    """

    def __init__(self, container, name, resultCallback = None):
        """
        args:
            container: o container pai onde o label será colocado
            nome(str): o nome do label
            callbackResultado: funcao chamada para atualizar o resultado
        """

        self.name = name
        self.resultCallback = resultCallback
        self.destiny = None
        self.fileCount = 0

        self.emptyColor = LABEL_CONFIG.get('gf_colour', 'transparent')
        self.filledColor = '#4CAF50'

        self.widget = ctk.CTkLabel(
            container,
            text=name,
            **LABEL_CONFIG
        )

        self.widget.drop_target_register(DND_FILES)
        self.widget.dnd_bind('<<Drop>>', self._onDrop)

    def _onDrop(self, event): 
        """
        MANIPULA OS EVENTO DE SOLTAR OS ARQUIVO NA LABEL
        """

        dirPath = event.data.strip("{}")

        if not os.path.isdir(dirPath):
            self._updateResult('precisa de uma pasta')
            return

        uniqueName = createUniqueDestinyPath(dirPath)
        self.destiny = uniqueName

        success, msg = FileService.copyDir(dirPath, uniqueName)
        if not success:
            self._updateResult('pasta nao encontrada')
            return
        
        results = ImageService.processImgDir(self.destiny, self.name)

        successes = sum(1 for success, _ in results if success)
        self._updateResult(f'processadas {successes} imagens para o label {self.name}')

    def _updateResult(self, msg):
        """
        ATUALIZA O RESULTADO ATRAVÉS DO CALLBACK
        """

        if self.resultCallback:
            self.resultCallback(msg)
        print(msg)