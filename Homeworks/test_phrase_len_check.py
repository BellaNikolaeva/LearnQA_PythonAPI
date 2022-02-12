class TestPhraseLenCheck:
    def test_phrase_len_check(self):
        phrase = input("Введите фразу короче 15 символов: ")
        assert len(phrase) < 15, f"Фраза длиннее 15 символов"