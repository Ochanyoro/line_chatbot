from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import pya3rt

app = Flask(__name__)

# 環境変数
linebot_api = LineBotApi('yourself')
handler = WebhookHandler('yourself')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ai_message = talk_ai(event.message.text)
    linebot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_message))


def talk_ai(word):
    apikey = "yourself"
    client = pya3rt.TalkClient(apikey)
    reply_message = client.talk(word)
    return reply_message['results'][0]['reply']

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
