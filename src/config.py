from environs import Env

env = Env()

NOTION_AUTH_TOKEN: str = env("NOTION_AUTH_TOKEN")

# https://www.notion.so/<database_id>?v=<view_id>
NOTION_ROADMAP_DATABASE_ID: str = env("NOTION_ROADMAP_DATABASE_ID", default="9104a4d0d3fd446aa3e64f31d8b4df1a")
NOTION_DQ_ISSUES_DATABASE_ID: str = env("NOTION_DQ_ISSUES_DATABASE_ID", default="57afd1c840f741a3848be503ef9a49f6")
NOTION_DASHBOARD_PAGE_ID: str = env("NOTION_DASHBOARD_PAGE_ID", default="9b5e8065f69846419bdc335beffc3479")

S3_ACCESS_KEY = env("S3_ACCESS_KEY")
S3_SECRET_KEY = env("S3_SECRET_KEY")
BUCKET_NAME = env("BUCKET_NAME")
