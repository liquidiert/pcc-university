from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable

import objectbox
from models.client import Client
from objectbox_handler import ob

from store.current_client import CurrentClientStore

class RelationsScreen:

    root = None
    client_box = objectbox.Box(ob, Client)
    data_table = None
    add_screen = None

    def init(self, root, sub_screen):
        self.root = root
        self.add_screen = sub_screen

    def build(self):
        self.clients: list[Client] = self.client_box.get_all()

        to_display = map(
            lambda c: (c.id, c.fullname),
            self.clients,
        )

        self.data_table = MDDataTable(
            size_hint=(1, 8),
            use_pagination=True,
            column_data=[
                ("Id", dp(20)),
                ("Name", dp(150)),
            ],
            row_data=to_display,
            rows_num=10
        )

        self.data_table.bind(on_row_press=self.on_client_click)

        return MDScreen(
            MDBoxLayout(
                MDLabel(
                    text="Relations",
                    font_style="H3"
                ),
                self.data_table,
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="relations_screen_box",
            ),
            name="relations",
        )
    
    def on_client_click(self, _, instance_row):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content

        start_indx, _ = instance_row.table.recycle_data[instance_row.index]["range"]
        client_id = int(instance_row.table.recycle_data[start_indx]["text"])

        CurrentClientStore.current_client = self.client_box.get(client_id)

        self.add_screen.refresh()

        screen_manager_content.current = "add_relations"