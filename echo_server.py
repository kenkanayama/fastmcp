from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

# FastMCPの初期化
mcp = FastMCP("Echo")

@mcp.resource("echo://{message}")  # GETリクエスト的なもの
def echo_resource(message: str) -> str:
    """リソースを提供する"""
    return f"リソース : {message}"

@mcp.tool()
def echo_tool(message: str) -> str:
    """加工する"""
    return f"メッセージを加工: {message * 2}"

# Prompt定義
@mcp.prompt()  # Promptの補完など
def echo_prompt(message: str) -> str:
    """プロンプトを定義する"""
    return f"Please process this message: {message}"

# ASGIアプリ作成（mcp.sse_app()をStarletteにマウント）
app = Starlette(
    routes=[
        Mount("/", app=mcp.sse_app()),
    ]
)

# サーバー起動用エントリーポイント（uvicornから実行する場合）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("echo_server:app", host="0.0.0.0", port=8080, reload=True)
