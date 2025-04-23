import customtkinter as ctk 
from tkinterdnd2 import TkinterDnD
import tkinter.filedialog as fd

from config.settings import APP_TITLE
from services.FileService import FileService

class MainMenu(TkinterDnD.Tk):
    """
    MENU PRINCIPAL
    """

    def __init__(self):
        """
        INICIALIZA O MENU PRINCIPAL
        """

        super().__init__()

        self.title(APP_TITLE)
        self.w = 250
        self.h = 250
        self.geometry(f'{self.w}x{self.h}')

        self._setupUi()

    def _setupUi(self):

        """
        CONFIGURA OS ELEMENTOS DA UI
        """

        self.container = ctk.CTkFrame(self)
        self.container.pack(expand = True, fill = 'both')

        self.titleLabel = ctk.CTkLabel(
            self.container,
            text = f'Gerador\nDe\nRedes\nNeurais',
            font=ctk.CTkFont(size=20, weight='bold')
        )
        self.titleLabel.pack(pady=(20, 10))

        self.newProjectButton = ctk.CTkButton(
            self.container, 
            text = 'Criar Novo Projeto',
            command = self._handleNewProjectButtonClick
        )
        self.newProjectButton.pack(pady=(30, 10))

        self.openProjectButton = ctk.CTkButton(
            self.container, 
            text = 'Abrir Projeto Existente',
            command = self._handleOpenProjectButtonClick
        )
        self.openProjectButton.pack()


    def init(self):
        """
        INICIA O LOOP PRINCIPAL DA JANELA
        """

        self.mainloop()

    def askNewProjectName(self):
        """
        CRIA UMA CAIXA DE DIALOGO PERGUNTANDO O NOME DO NOVO PROJETO

        RETURNS: 
            str: nome do projeto, q vai ser o nome da pasta  
        """

        dialog = ctk.CTkInputDialog(text='Nome do projeto:', title='NiuProjequiti')
        dialog.geometry('250x100')
        return dialog.get_input()


    def _handleNewProjectButtonClick(self):
        newProjectName = self.askNewProjectName()
        FileService.createNewProject(newProjectName)

    def _handleOpenProjectButtonClick(self):
        existingProjectPath = fd.askdirectory(
            title='Cade o projetinho do nenem? cade? cade?',
            initialdir='./uploads'
        )
        print(existingProjectPath)