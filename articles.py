import jp
import uvicorn
import re
import random
from crawler import SubTitleCrawler


class Word(jp.Span):
    def __init__(self, **kwargs):
        kwargs['class_'] = 'text-green-500 text-xl pr-2 cursor-pointer'
        kwargs['on_click'] = self.on_click
        self.is_green = True
        super().__init__(**kwargs)

    def on_click(self, _):
        if self.is_green:
            self.set_class('text-gray-500')
        else:
            self.set_class('text-green-500')

        self.is_green = not self.is_green
        card = self.page.card
        print()


class Watchcard(jp.Div):
    html_render = """
    <div class="w-2/3 bg-white mt-20  rounded-lg shadow p-12" style="min-height: 20rem;">
    <textarea rows="4" cols="50" name="textarea"></textarea>
    <button class="text-5xl px-6 m-2 text-lg text-indigo-100 transition-colors duration-150 bg-indigo-700 rounded-lg focus:shadow-outline hover:bg-indigo-80" @click="click">送出</button>
    </div>
    """

    async def click(self, _):
        textarea = self.name_dict['textarea']
        if textarea.value:
            self.page.original_english = textarea.value
        item = self.page.name_dict['item']
        item.delete()
        card = Card()
        self.page.card = card
        item.add_component(card)
        await card.build()


class Card(jp.Div):
    def __init__(self, **kwargs):
        kwargs['class_'] = 'w-2/3 bg-white mt-20  rounded-lg shadow p-12 flex flex-wrap'
        kwargs['style'] = 'min-height: 20rem;'
        super().__init__(**kwargs)
        self.en_area = None
        self.tw_area = None

    async def make_sound(self, target):
        eval_text = f"""
            let utterance = new window.SpeechSynthesisUtterance("{target.replace('"', '')}");
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance)
            console.log("{target}")
            """
        await self.page.run_javascript(eval_text)

    async def build(self):
        self.delete_components()
        for word in self.page.original_english.split():
            self.add_component(Word(text=word))
        self.add_component(jp.Div(class_='bg-gray-600 h-px my-6 w-full'))
        self.en_area = jp.Div(text=self.page.original_english)
        self.add_component(self.en_area)
        self.add_component(jp.Div(class_='bg-gray-600 h-px my-6 w-full'))
        self.tw_area = jp.Div(text='我是中文翻譯')
        self.add_component(self.tw_area)


@jp.SetRoute('/')
async def demo():
    wp = jp.justpy_parser_to_wp("""
    <div class="bg-red-200 h-screen">
        <div class="flex flex-col items-center" name="item">
        <WatchCard></WatchCard>
        </div>
      </div>
    """)

    return wp


app = jp.app

if __name__ == '__main__':
    uvicorn.run('d10:app', debug=True)
