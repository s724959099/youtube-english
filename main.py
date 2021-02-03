import jp
import uvicorn
import re
import random


class Word(jp.Span):
    def __init__(self, **kwargs):
        kwargs['class_'] = 'text-green-500 text-5xl'
        super().__init__(**kwargs)


class WordInput(jp.Input):
    def __init__(self, length=1, **kwargs):
        kwargs['class_'] = 'outline-none bg-gray-300 text-green-500 text-5xl'
        kwargs['style'] = f'width: {length * 2}rem;'
        super().__init__(**kwargs)


class Card(jp.Div):
    def __init__(self, sentence, **kwargs):
        self.sentence = sentence
        kwargs['class_'] = 'w-2/3 bg-white mt-20  rounded-lg shadow p-12'
        kwargs['style'] = 'min-height: 20rem;'
        super().__init__(**kwargs)

    def get_word(self, words):
        count = 0
        while True:
            count += 1
            word = random.choice(words)
            if len(word) >= 2 or count > 3:
                return word

    def react(self):
        self.delete_components()
        s = self.sentence
        words = re.findall(r'\w+', s)
        word = self.get_word(words)
        st_index = s.index(word)
        ed_index = st_index + len(word)
        prefix_s = s[:st_index]
        suffix_s = s[ed_index:]
        self.add_component(Word(text=prefix_s))
        self.add_component(WordInput(length=len(word)))
        self.add_component(Word(text=suffix_s))
        print('prefix_s:', prefix_s)
        print('word:', word)
        print('suffix_s:', suffix_s)


@jp.SetRoute('/')
def demo():
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div class="bg-red-200 h-screen">
        <div class="flex flex-col items-center" name="item">
        </div>
      </div>
    """)
    citem = c.name_dict['item']
    card = Card(sentence='Tom works like a horse.')
    citem.add_component(card)
    wp.add_component(c)

    return wp


app = jp.app

if __name__ == '__main__':
    uvicorn.run('main:app', debug=True)
