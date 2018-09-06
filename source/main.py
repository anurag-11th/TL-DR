from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from summarize import summarize
from webScrape import getArticle
from readfile import getText

class Manager(ScreenManager):

	screen_one = ObjectProperty(None)
	screen_two = ObjectProperty(None)
	screen_three = ObjectProperty(None)
	screen_four = ObjectProperty(None)


class PasteScreen(Screen):
	
	def clear_paste(self):
		self.ids.paste_space.text = ""

	def summarize(self):
		article_text = self.ids.paste_space.text

		if article_text == "":
			lyt = BoxLayout(orientation='vertical')
			lbl = Label(text="No article is given", size_hint=(1, 0.3), font_size=25)
			btn = Button(text="Close", size_hint = (1, 0.2))
			lyt.add_widget(lbl)
			lyt.add_widget(btn)
			popup = Popup(title="Error!", content=lyt, size_hint=(None, None), size=(400, 400))
			btn.bind(on_press=popup.dismiss)
			popup.open()

		else:
			summarized_sentences = summarize(article_text)
		
			self.manager.current = "Screen4"
			self.manager.screens[3].result_box.text = ""
			for s in summarized_sentences:
				self.manager.screens[3].result_box.text += s +"\n\n"

 
class UrlScreen(Screen):
	
	def clear_url(self):
		self.ids.url_space.text = ""

	def url_summarize(self):      
		url = self.ids.url_space.text
		
		if url == "":
			lyt = BoxLayout(orientation='vertical')
			lbl = Label(text="URL cannot be empty!", size_hint=(1, 0.3), font_size=25)
			btn = Button(text="Close", size_hint = (1, 0.2))
			lyt.add_widget(lbl)
			lyt.add_widget(btn)
			popup = Popup(title="Error!", content=lyt, size_hint=(None, None), size=(400, 400))
			btn.bind(on_press=popup.dismiss)
			popup.open()
		
		else:
			article = getArticle(url)
			summarized_sentences = summarize(article[1], article[0])

			self.manager.current = "Screen4"
			self.manager.screens[3].result_box.text = ""
			for s in summarized_sentences:
				self.manager.screens[3].result_box.text += s +"\n\n"


class UploadScreen(Screen):
	
	def clear_upload(self):
		self.ids.upload_space.text = ""

	def upload(self):
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
		filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
		self.ids.upload_space.text = filename

	def upload_summarize(self):
		filepath = self.ids.upload_space.text

		if filepath == "":
			lyt = BoxLayout(orientation='vertical')
			lbl = Label(text="No file is chosen", size_hint=(1, 0.3), font_size=25)
			btn = Button(text="Close", size_hint = (1, 0.2))
			lyt.add_widget(lbl)
			lyt.add_widget(btn)
			popup = Popup(title="Error!", content=lyt, size_hint=(None, None), size=(400, 400))
			btn.bind(on_press=popup.dismiss)
			popup.open()

		else:
			text = getText(filepath)

			if text == -1:
				lyt = BoxLayout(orientation='vertical')
				lbl = Label(text="File type uploaded is not supported. Please try another file.", size_hint=(1, 0.3), font_size=25)
				btn = Button(text="Close", size_hint = (1, 0.2))
				lyt.add_widget(lbl)
				lyt.add_widget(btn)
				popup = Popup(title="Error!", content=lyt, size_hint=(None, None), size=(400, 400))
				btn.bind(on_press=popup.dismiss)
				popup.open()
				clear_upload()

			else:
				summarized_sentences = summarize(text)		
				self.manager.current = "Screen4"
				self.manager.screens[3].result_box.text = ""
				for s in summarized_sentences:
					self.manager.screens[3].result_box.text += s +"\n\n"


class ResultScreen(Screen):
	
	result_box = ObjectProperty(None)

class ScreenApp(App):

	def build(self):
		return Manager()


if __name__ == '__main__':
	ScreenApp().run()
