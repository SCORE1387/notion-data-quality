from data_quality_rule import DataQualityRule, IssueTypeSeverity
from helpers import is_more_than_two_weeks_away


def tags_must_not_be_empty(notion_card) -> bool:
    if not notion_card["properties"]["Tags"]["multi_select"]:
        return True
    return False


def number_must_be_more_than_10(notion_card) -> bool:
    number = notion_card["properties"]["Number"]["number"]
    if not number or number <= 10:
        return True
    return False


def no_updates_for_2_weeks(notion_card) -> bool:
    last_edited_str = notion_card["properties"]["Last edited time"]["last_edited_time"]
    return is_more_than_two_weeks_away(last_edited_str)


def name_is_empty(notion_card) -> bool:
    if not notion_card["properties"]["Name"]["title"][0]["text"]["content"]:
        return True
    return False


RULES: dict[str, DataQualityRule] = {
    "Tags Must Not Be Empty":
        DataQualityRule("Tags Must Not Be Empty",
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
                        "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                        "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                        "https://www.notion.so/sekol/57afd1c840f741a3848be503ef9a49f6?v=5a1eec42af4a46e78985b25291684c58&pvs=4",
                        IssueTypeSeverity.RED,
                        tags_must_not_be_empty),

    "Number must be > 10":
        DataQualityRule("Number must be > 10",
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
                        "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                        "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                        "https://www.notion.so/sekol/57afd1c840f741a3848be503ef9a49f6?v=018b66ccf12c4e32808407409daba602&pvs=4",
                        IssueTypeSeverity.BLUE,
                        number_must_be_more_than_10),

    "No updates for 2+ weeks":
        DataQualityRule("No updates for 2+ weeks",
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
                        "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                        "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                        "https://www.notion.so/sekol/57afd1c840f741a3848be503ef9a49f6?v=6133d8397d324f39bb84b2520642562a&pvs=4",
                        IssueTypeSeverity.YELLOW,
                        no_updates_for_2_weeks),

    "Name is empty":
        DataQualityRule("Name is empty",
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
                        "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                        "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                        "https://www.notion.so/sekol/57afd1c840f741a3848be503ef9a49f6?v=cb27fa6faa414ab99732a3b4802ba013&pvs=4",
                        IssueTypeSeverity.RED,
                        name_is_empty),
}
