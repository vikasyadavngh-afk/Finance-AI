import json
import os
from datetime import date
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

DATA_FILE = os.path.join(os.path.dirname(__file__), "finance_data.json")

KV = r"""
<FinanceRoot>:
    orientation: "vertical"
    padding: "14dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: 0.95, 0.97, 0.99, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "[b]Finance AI[/b]"
        markup: True
        font_size: "27sp"
        color: 0.08, 0.18, 0.32, 1
        size_hint_y: None
        height: "42dp"
    Label:
        text: "Personal money tracker"
        color: 0.28, 0.34, 0.42, 1
        size_hint_y: None
        height: "24dp"
    BoxLayout:
        size_hint_y: None
        height: "92dp"
        spacing: "8dp"
        BoxLayout:
            orientation: "vertical"
            padding: "10dp"
            canvas.before:
                Color:
                    rgba: 0.86, 0.93, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [12]
            Label:
                text: "Total expenses"
                color: 0.12, 0.2, 0.3, 1
            Label:
                text: root.total_text
                bold: True
                font_size: "20sp"
                color: 0.05, 0.22, 0.45, 1
        BoxLayout:
            orientation: "vertical"
            padding: "10dp"
            canvas.before:
                Color:
                    rgba: 0.86, 0.96, 0.89, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [12]
            Label:
                text: "Entries"
                color: 0.12, 0.2, 0.3, 1
            Label:
                text: root.count_text
                bold: True
                font_size: "20sp"
                color: 0.08, 0.38, 0.2, 1
    Label:
        text: "Add an expense"
        bold: True
        color: 0.08, 0.18, 0.32, 1
        size_hint_y: None
        height: "26dp"
    TextInput:
        id: amount
        hint_text: "Amount (₹)"
        input_filter: "float"
        multiline: False
        size_hint_y: None
        height: "46dp"
    TextInput:
        id: category
        hint_text: "Category (e.g. Food, Travel, Bills)"
        multiline: False
        size_hint_y: None
        height: "46dp"
    TextInput:
        id: note
        hint_text: "Note (optional)"
        multiline: False
        size_hint_y: None
        height: "46dp"
    Button:
        text: "Save expense"
        size_hint_y: None
        height: "48dp"
        background_normal: ""
        background_color: 0.10, 0.35, 0.72, 1
        on_release: root.add_expense(amount.text, category.text, note.text)
    BoxLayout:
        size_hint_y: None
        height: "34dp"
        Label:
            text: "Recent expenses"
            bold: True
            color: 0.08, 0.18, 0.32, 1
        Button:
            text: "Refresh"
            size_hint_x: None
            width: "90dp"
            on_release: root.refresh()
    ScrollView:
        do_scroll_x: False
        GridLayout:
            id: entries
            cols: 1
            spacing: "6dp"
            padding: "2dp"
            size_hint_y: None
            height: self.minimum_height
    Label:
        text: "Data is saved on this device. Keep a backup of your phone."
        color: 0.35, 0.4, 0.46, 1
        font_size: "11sp"
        size_hint_y: None
        height: "24dp"
"""

class FinanceRoot(BoxLayout):
    total_text = StringProperty("₹0.00")
    count_text = StringProperty("0")
    entries_data = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_data()
        self.refresh()

    def load_data(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.entries_data = data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            self.entries_data = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.entries_data, f, ensure_ascii=False, indent=2)
        except OSError:
            self.show_message("Could not save data. Check device storage.")

    def add_expense(self, amount_text, category, note):
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            self.show_message("Enter a valid amount greater than zero.")
            return
        category = category.strip() or "Other"
        item = {
            "amount": round(amount, 2),
            "category": category,
            "note": note.strip(),
            "date": date.today().isoformat()
        }
        self.entries_data.insert(0, item)
        self.save_data()
        self.ids.amount.text = ""
        self.ids.category.text = ""
        self.ids.note.text = ""
        self.refresh()
        self.show_message("Expense saved.")

    def refresh(self):
        total = sum(float(x.get("amount", 0)) for x in self.entries_data)
        self.total_text = "₹{:,.2f}".format(total)
        self.count_text = str(len(self.entries_data))
        if "entries" not in self.ids:
            return
        box = self.ids.entries
        box.clear_widgets()
        if not self.entries_data:
            box.add_widget(Label(
                text="No expenses yet. Add your first expense above.",
                size_hint_y=None, height="42dp",
                color=(0.35, 0.4, 0.46, 1)
            ))
            return
        for item in self.entries_data[:100]:
            amount = float(item.get("amount", 0))
            title = "{}  •  ₹{:,.2f}".format(item.get("category", "Other"), amount)
            subtitle = "{}{}".format(
                item.get("date", ""),
                ("  —  " + item.get("note", "")) if item.get("note") else ""
            )
            row = BoxLayout(orientation="vertical", size_hint_y=None, height="58dp",
                            padding=("10dp", "4dp"))
            from kivy.graphics import Color, RoundedRectangle
            with row.canvas.before:
                Color(1, 1, 1, 1)
                row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[8])
            row.bind(pos=lambda inst, val: setattr(inst.bg, "pos", val),
                     size=lambda inst, val: setattr(inst.bg, "size", val))
            row.add_widget(Label(text=title, bold=True, color=(0.1, 0.16, 0.23, 1),
                                 halign="left", valign="middle", size_hint_y=0.58,
                                 text_size=(self.width - 50, None)))
            row.add_widget(Label(text=subtitle, color=(0.38, 0.42, 0.48, 1),
                                 halign="left", valign="middle", size_hint_y=0.42,
                                 font_size="12sp", text_size=(self.width - 50, None)))
            box.add_widget(row)

    def show_message(self, message):
        Popup(title="Finance AI", content=Label(text=message),
              size_hint=(0.82, 0.28), auto_dismiss=True).open()

class FinanceAIApp(App):
    title = "Finance AI"

    def build(self):
        Builder.load_string(KV)
        return FinanceRoot()

if __name__ == "__main__":
    FinanceAIApp().run()
