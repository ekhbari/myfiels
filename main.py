from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
import json, os

KV = '''
<NoteItem@BoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    height: '50dp'
    spacing: '8dp'
    Label:
        text: root.text
        text_size: self.size
        halign: 'right'
        valign: 'middle'
    Button:
        text: '🗑'
        size_hint_x: None
        width: '60dp'
        on_release: app.delete_note(root.index)

<Root>:
    orientation: 'vertical'
    padding: '12dp'
    spacing: '12dp'

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        TextInput:
            id: note_input
            hint_text: 'اكتب ملاحظة جديدة'
            multiline: False
            on_text_validate: add_btn.trigger_action()
        Button:
            id: add_btn
            text: 'إضافة'
            size_hint_x: None
            width: '100dp'
            on_release:
                app.add_note(note_input.text)
                note_input.text = ''
    RecycleView:
        id: rv
        viewclass: 'NoteItem'
        scroll_type: ['bars', 'content']
        bar_width: 8
        RecycleBoxLayout:
            default_size: None, dp(50)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
'''

class Root(BoxLayout):
    pass

class NotesApp(App):
    notes = ListProperty()

    def build(self):
        self.load_notes()
        root = Builder.load_string(KV)
        self.update_rv(root)
        return root

    # ---------- البيانات ----------
    def _file_path(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        return os.path.join(self.user_data_dir, 'notes.json')

    def load_notes(self):
        try:
            with open(self._file_path(), 'r', encoding='utf-8') as f:
                self.notes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = []

    def save_notes(self):
        with open(self._file_path(), 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    # ---------- العمليات ----------
    def update_rv(self, root):
        root.ids.rv.data = [{'text': note, 'index': i} for i, note in enumerate(self.notes)]

    def add_note(self, text: str):
        text = text.strip()
        if text:
            self.notes.append(text)
            self.save_notes()
            self.update_rv(self.root)

    def delete_note(self, index: int):
        self.notes.pop(index)
        self.save_notes()
        self.update_rv(self.root)

if __name__ == '__main__':
    NotesApp().run()
