## やったこととやりたかったこと

Docker環境でFastMCPを使ってMCPサーバーを自作し使用してみたかった。

## 感想（MCPサーバーをDocker環境で構築して試した所感）
浅いところでいうと、prompt や resource はLLMを活用した各社ツールの裏側にあるプロンプト設計やリソース取得機構に近く、
tool はまさに OpenAI の Function Calling に対応するようなものだと感じた。

ただしこのMCPという規格に則って構築することが大事であり強み。
MCPサーバー側がtool, prompt, resourceといった統一されたインターフェースで実装されていれば、
あらゆるMCPクライアントに対してサーバー側の設計は一切変えずに使い回せる。（←当前のこと書いてる）  
API仕様の標準化（例：RESTなど）と似た思想で、今後のLLM連携系の構築・運用コストを確実に下げる可能性を感じた。

全体的に、まだエコシステムとしてはこれから拡大していく段階だとは思うが、
開発者目線で見れば、LLMを中心としたツールのモジュール化・相互運用性の基盤として簡易的だと感じた。

## Claude for Desktop に当MCPサーバーを設定する

### 1. `claude_desktop_config.json`に以下を登録する

```
{
    "mcpServers": {
        "MCP_DOCKER": {
            "command": "docker",
            "args": [
                "run",
                "--rm",
                "-i",
                "--name",
                "mcp_server",
                "-v",
                "type=bind,src=<YOUR_LOCAL_PATH>,dst=/projects/usr/src/app",
                "mcp_server"
            ]
        }
    }
}
```

- <YOUR_LOCAL_PATH>: 当ディレクトリの絶対パス


### 2. ビルドする

```
docker build --force-rm=true -t mcp_server . --no-cache=true
```

### 3. Claude for Desktopを起動する

完了


## Claude for Desktopでの使用

トンカチマークに連携しているツールの数が表示される。今回のMCPサーバーしか連携されていないため「1」が表示されている
![image](https://github.com/user-attachments/assets/4c761443-0318-4f38-b37b-9341016f7eb8)


---

`prompt`と`resource`はトンカチマークの右隣のアイコンから選択ができる。これらはチャット時に選択して使用していく。

![image](https://github.com/user-attachments/assets/3fece53a-3fba-41e8-8c18-a19a902066f5)


---

`resource`を選択し、チャット送信前の状態↓
画面上ではテキストファイルが添付されたような形になる。
![image](https://github.com/user-attachments/assets/6c0c85e5-c574-4054-b0f0-68cab62cfc97)




---



実行すると以下の回答。  
`resource`のreturn値に設定している内容以外も出力される。  
回答の中でreturn値に設定している内容が含まれて、そこにLLMが補完するような出力をしていくような形。


![image](https://github.com/user-attachments/assets/d33f83b5-3aaf-4b46-bcb4-b5acb06a0109)




---


次は`prompt`の`answer_in_user_specified_lang`を選択し、同じ質問をしてみる。  
この`prompt`は`language`を受け取るので、選択後に`language`の入力欄が表示される。  
その後そのまま先ほど同じ質問をしている。
前回と`resource`は同じなので架空人物は同じもの。回答はイタリア語になっている。


![image](https://github.com/user-attachments/assets/5a93730e-2252-43c5-995f-0087402738c4)


![image](https://github.com/user-attachments/assets/bd1b98e9-879c-4385-9533-6e9a14a72caa)


![image](https://github.com/user-attachments/assets/a67605f4-4ec3-4840-b426-18f81ed6ec75)

---

最後に、`tool`が使用されるか試してみる。  
「さきほどの情報の文字数を教えて」と入力し送信すると、2枚目の「ツールを許可するか」というポップアップが出てくる。  
許可すると、引数`message`に文字が渡され、return値に設定した内容を含めた回答が返ってきた。

![image](https://github.com/user-attachments/assets/6ac43c58-018c-4425-8f4e-6c75cddd626b)

![image](https://github.com/user-attachments/assets/60939615-66e7-46c4-9902-2b726a0e7f3f)

