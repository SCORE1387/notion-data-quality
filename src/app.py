from notion_client import Client

import config
from data_quality_rule import IssueTypeSeverity
from notion_card_data_quality_issue import NotionCardDataQualityIssue
from notion_card_data_quality_rules_config import RULES
from number_image import get_number_image

notion = Client(auth=config.NOTION_AUTH_TOKEN)


def read_roadmap_db_items():
    # Read Roadmap database items from Notion
    roadmap_db_pages = notion.databases.query(database_id=config.NOTION_ROADMAP_DATABASE_ID)
    return roadmap_db_pages["results"]


def clean_data_quality_db():
    data_quality_db_pages = notion.databases.query(database_id=config.NOTION_DQ_ISSUES_DATABASE_ID)
    for page in data_quality_db_pages["results"]:
        notion.pages.update(page_id=page["id"], archived=True)


def recreate_data_quality_db(data_quality_issues: list[NotionCardDataQualityIssue]):
    clean_data_quality_db()
    for data_quality_issue in data_quality_issues:
        notion.pages.create(
            parent={"database_id": config.NOTION_DQ_ISSUES_DATABASE_ID},
            properties={
                "Issue Type": {"title": [{"text": {"content": data_quality_issue.data_quality_rule.name}}]},
                "Related Page": {"relation": [{"id": data_quality_issue.notion_card["id"]}]},
                "Description": {"rich_text": [{"text": {"content": data_quality_issue.data_quality_rule.description}}]},
            }
        )


def update_dq_item_block(callout_block, image_block, data_quality_issues_map):
    data_quality_rule_name = str.strip(callout_block["callout"]["rich_text"][0]["text"]["content"])
    new_count = 0
    if data_quality_rule_name in data_quality_issues_map:
        new_count = len(data_quality_issues_map[data_quality_rule_name])
    print(f"Updating \"{data_quality_rule_name}\" tile count to {new_count}")
    severity = IssueTypeSeverity.GREEN.name if new_count == 0 else RULES[data_quality_rule_name].severity.name
    image_url = get_number_image(new_count, severity)
    print(image_url)

    callout_block["callout"]["rich_text"][0]["text"]["link"]["url"] = RULES[data_quality_rule_name].dashboard_link
    notion.blocks.update(block_id=callout_block["id"], **callout_block)

    image_block["image"]["external"]["url"] = image_url
    image_block["image"]["caption"][0]["text"]["content"] = RULES[data_quality_rule_name].description
    del image_block["image"]["type"]
    notion.blocks.update(block_id=image_block["id"], **image_block)


def generate_dashboard_page(data_quality_issues_map):
    dq_row_blocks = notion.blocks.children.list(block_id=config.NOTION_DASHBOARD_PAGE_ID)
    for callout_dq_row_block_idx, callout_dq_row_block in enumerate(dq_row_blocks["results"]):
        callout_parent_blocks = notion.blocks.children.list(block_id=callout_dq_row_block["id"])
        for callout_parent_block_idx, callout_parent_block in enumerate(callout_parent_blocks["results"]):
            callout_child_blocks = notion.blocks.children.list(block_id=callout_parent_block["id"])
            if callout_child_blocks["results"][0]["type"] == "callout":
                callout_block = callout_child_blocks["results"][0]
                image_dq_row_block = dq_row_blocks["results"][callout_dq_row_block_idx + 1]
                image_parent_blocks = notion.blocks.children.list(block_id=image_dq_row_block["id"])
                image_parent_block = image_parent_blocks["results"][callout_parent_block_idx]
                image_child_blocks = notion.blocks.children.list(block_id=image_parent_block["id"])
                image_block = image_child_blocks["results"][0]
                update_dq_item_block(callout_block, image_block, data_quality_issues_map)


def generate_data_quality_report():
    data_quality_issues = []
    data_quality_issues_map = {}

    # Read Notion Roadmap DB pages
    roadmap_db_pages = read_roadmap_db_items()

    # Evaluate each page against data quality rules
    for item in roadmap_db_pages:
        for rule in RULES.values():
            if rule.evaluate_function(item):
                data_quality_issue = NotionCardDataQualityIssue(rule, item)
                data_quality_issues.append(data_quality_issue)
                if data_quality_issue.data_quality_rule.name not in data_quality_issues_map:
                    data_quality_issues_map[data_quality_issue.data_quality_rule.name] = []
                data_quality_issues_map[data_quality_issue.data_quality_rule.name].append(data_quality_issue)

    print(data_quality_issues)

    # Recreate Data Quality Notion DB
    recreate_data_quality_db(data_quality_issues)

    # Generate notion Dashboard page
    generate_dashboard_page(data_quality_issues_map)


if __name__ == '__main__':
    generate_data_quality_report()
