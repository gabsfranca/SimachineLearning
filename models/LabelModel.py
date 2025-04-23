"""
MODELO PARA ARMAZENAR AS INFO SOBRE AS LABEL
"""

class LabelInfo:
    def __init__(self, name, labelWidget):
        """
        args:
            name(str): o nome da label ne lkkk
            labelWidget: o widget do label do UI
        """

        self.name = name
        self.label = labelWidget
        self.destiny = None

    def setDestiny(self, destinyPath):
        """
        args:
            destinyPath(str): o caminho do resultado 
        """

        self.destiny = destinyPath

    def hasDestiny(self):
        return self.destiny is not None
        