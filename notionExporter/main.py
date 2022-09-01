import json
import os
from pprint import pprint

from jinja2 import BaseLoader, Environment, FileSystemLoader, Template
from notion_client import Client

TEMPLATE_FLODER = "./templates"


class Extacter:
    def __init__(self) -> None:
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))

    def export_database(self, database_id: str, out: str = "out.md"):
        resp = self.notion.databases.query(database_id)
        # template = Environment(loader=FileSystemLoader(TEMPLATE_FLODER)).from_string(
        #     open("database.templ", encoding="utf-8").read()
        # )
        # result = template.render(resp)
        content = """| 名称  | 作者  | 打分  | 状态  | 类型  |\n|---|---|---|---|---|\n"""
        for result in resp["results"]:
            name = "".join(
                [i["plain_text"] for i in result["properties"]["Name"]["title"]]
            )
            auhtors = ", ".join(
                [i["name"] for i in result["properties"]["Author"]["multi_select"]]
            )
            score = result["properties"]["Score /5"]["select"]
            score = score.get("name") if score else ""

            statusObj = result["properties"]["Status"]["select"]
            status = statusObj.get("name") if statusObj else ""
            status_color = statusObj.get("color") if statusObj else ""

            categoryObj = result["properties"]["类型"]["select"]
            category = categoryObj.get("name") if categoryObj else ""
            category_color = categoryObj.get("color") if categoryObj else ""

            line = f'|  {name} | {auhtors}  | {score}  | <span style="color:{status_color}">{status}</span>  |  <span style="color:{category_color}">{category}</span> |\n'
            content += line

        with open(out, "w") as f:
            f.write(content)


if __name__ == "__main__":
    DATABASE_ID = "661d5636f6c04255b2836cb5c92f656a"
    Extacter().export_database(DATABASE_ID, "out.md")
