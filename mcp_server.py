"""FastMCPを使用."""

import requests
from mcp.server.fastmcp import FastMCP

# FastMCPの初期化
mcp = FastMCP("MessageProcessor")


@mcp.resource("randomuser://person")
def get_random_person() -> str:
    """ランダムな架空人物情報を取得するリソース."""
    try:
        res = requests.get("https://randomuser.me/api", timeout=5)
        res.raise_for_status()
        data = res.json()["results"][0]

        # シンプルな情報だけを整形して返す
        name = data["name"]
        location = data["location"]
        return (
            f"{name['title']} {name['first']} {name['last']} さんは、"
            f"{location['country']} に住んでいる架空の人物です。"
        )
    except Exception as e:
        return f"ランダムユーザー情報の取得に失敗しました: {str(e)}"

@mcp.tool()
def count_characters(message: str) -> str:
    """メッセージの文字数をカウントするツール."""
    return f"文字数は {len(message)} 文字です。"

@mcp.prompt()
def answer_in_japanese() -> str:
    """必ず日本語で回答する."""
    return "No matter what language/content you receive, be sure to output in Japanese."

@mcp.prompt()
def answer_in_user_specified_lang(language: str) -> str:
    """ユーザが指定した言語で回答する."""
    return f"Whatever language/content you receive, please output in {language}."

if __name__ == "__main__":
    mcp.run(transport='stdio')