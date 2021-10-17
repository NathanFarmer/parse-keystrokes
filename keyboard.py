class Keyboard:
    def __init__(self, key_set):
        self.key_set = key_set

    def key_tokens(self):
        if self.key_set == 75:
            return [
                "[DEL]",
                "[RIGHT]",
                " ",
                "E",
                "T",
                "A",
                "[LEFT]",
                "[RETURN]",
                "S",
                "C",
                "I",
                "R",
                "O",
                "L",
                "N",
                "[DOWN]",
                "[LEFT-CMD]",
                "D",
                "P",
                "M",
            ]
