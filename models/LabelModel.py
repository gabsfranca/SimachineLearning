"""
MODELO PARA ARMAZENAR AS INFO SOBRE AS LABEL
"""

class LabelInfo:
    def __init__(self, name, dragLabelInstance):
        """
        args:
            name(str): o nome da label ne lkkk
            labelWidget: o widget do label do UI
        """

        self.name = name
        self.dragLabel = dragLabelInstance
        self.label = dragLabelInstance.widget
        self.destiny = None

    def setDestiny(self, destinyPath):
        """
        args:
            destinyPath(str): o caminho do resultado 
        """

        self.destiny = destinyPath

    def hasDestiny(self):
        return self.destiny is not None
        