import customtkinter as ctk 
from tkinterdnd2 import TkinterDnD
import os 

from config.settings import APP_TITLE, MAX_LABELS, RESULT_LABEL_CONFIG
from models.LabelModel import LabelInfo
from UI.Components.DragLabel import DragLabel
from services.FileService import FileService
from services.ImageService import ImageService
from utils.DirectoryUtils import cleanTemp

class TelaDragFotos(TkinterDnD.Tk):
    """
    TELA PRINCIPAL PARA ARRASTAR AS PASTAS COM IMAGENS E SEPARAR AS PASTAS PARA TREINAMENTO DO MODELO
    """

    def __init__(self):

        """
        INICIALIZA A TELA PRINCIPAL
        """

        super().__init__()

        self.title(APP_TITLE)
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.geometry(f'{self.h}x{self.w}')

        self.maxLabels = MAX_LABELS
        self.labels = []

        FileService.createBaseDirs()

        self._setupUi()

    #// underline usa pra definir um metodo privado da minha classe 
    def _setupUi(self):

        """
        CONFIGURA OS ELEMENTOS DA UI
        """

        self.container = ctk.CTkFrame(self)
        self.container.pack(expand = True, fill='both', padx=20, pady=20)

        self.buttonContainer= ctk.CTkFrame(self)
        self.buttonContainer.pack(fill='x')

        # eu nem sei direito como explicar o **, mas ele meio que desempacota os valores de 
        # RESULT_LABEL_CONFIg nesse caso, para passar como argumento da função, mt loco
        self.resultLabel = ctk.CTkLabel(self, text="", **RESULT_LABEL_CONFIG)
        self.resultLabel.pack()

        self.addButton = ctk.CTkButton(
            self.buttonContainer,
            text='+',
            command=self.addLabel
        )
        self.addButton.pack(side='right', padx=5)

        self.confirmButton = ctk.CTkButton(
            self.buttonContainer,
            text='confirmar',
            command=self.confirmButtonOnClick
        )
        self.confirmButton.pack(side='right', padx=5)

    def init(self):
        """
        INICIA O LOOP PRINCIPAL DAAPLICAÇÃO 
        """

        self.mainloop()

    def addLabel(self):
        """
        ADICIONA UM NOVO LABEL À INTERFACE
        """    

        if len(self.labels) >= self.maxLabels:
            self.resultLabel.configure(text='limite de labels atingido')
            return 
        
        dialogBoxText = 'Insira o nome da nova label'
        dialogBoxTittle = 'Nova Label'

        name = self.askLabelName(dialogBoxText, dialogBoxTittle)
        if not name:
            return
        
        dragLabel = DragLabel(
            self.container,
            name, 
            resultCallback=self._updateResult
        )

        labelInfo = LabelInfo(name, dragLabel)
        self.labels.append(labelInfo)
        self.organizeLabels()

    def newProjectHandleClick(self):
        text = 'Nome do novo projeto'
        tittle = 'Novo Projeto'
        name = self.askLabelName(text, tittle)
        FileService.createNewProject(name)
        

    def askLabelName(self):
        """
        PERGUNTA PRO USUÁRIO O NOME DA LABEL NOVA

        RETURNS:
            str: nome da label nova ou None caso cancelado
        """

        dialog = ctk.CTkInputDialog(text=f'Insira o nome da label', title=f'{'Nova Label'}')
        return dialog.get_input()
    
    def organizeLabels(self):
        """
        ORGANIZA AS LABELS NA GRADE
        """

        #limpa as labels atuais
        for widget in self.container.winfo_children():
            widget.grid_forget()

        total = len(self.labels)

        #determina o layout baseado no numero de labels
        if total <= 3:
            rows, cols = 1, total
        else:
            rows = 2
            cols = 3 if total > 6 else (total + 1) // 2

        #configura as colunas com pesos iguais
        for i in range(3):
            self.container.grid_columnconfigure(i, weight=1, uniform='col')

        #configura as linhas com pesos iguais
        for i in range(2):
            self.container.grid_rowconfigure(i, weight=1)

        #posiciona as labels na grade
        for idx, label_dict in enumerate(self.labels):
            row = idx // 3
            col = idx % 3
            #nsew significa north, south, east, west, ou seja, vai "grudar" de todos os lados a label, se fosse só n ele colaria só em cima 
            label_dict.label.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
    
    def _updateResult(self, msg):
        """
        ATUALIZA O LABEL DE RESULTADO

        ARGS:
            msg(str): msg a ser exibida
        """

        self.resultLabel.configure(text=msg)
        print(msg)

    def confirmButtonOnClick(self):
        """
        MANIPULA O CLIQUE NO BOTAO DE CONFIRMAR IMAGENS
        """
        

        if not self.labels: 
            self._updateResult('adicione ao menos uma label')
            return
        
        
        for lbl in self.labels:

            destiny = getattr(lbl, 'destiny', None)
            name = lbl.name

            if destiny and os.path.exists(destiny):
                results = ImageService.processImgDir(destiny, name)
                successes = sum(1 for success, _ in results if success)

                if hasattr(lbl, 'dragLabel'):
                    lbl.dragLabel.fileCount = successes
                    lbl.dragLabel._updateLabelColor()

                self._updateResult(f'Processadas {successes} imagens para a label {name}')
            else:
                self._updateResult(f'pasta já criada para a label {name}')

        success, msg = cleanTemp()
        if not success:
            self._updateResult(msg)

    def close(self):
        """
        FECHA A APLICAÇÃO E REALIZA A LIMPEZA NECESSÁRIA
        """

        cleanTemp()
        self.destroy()