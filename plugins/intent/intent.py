# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="Hello",
    desire_priority=-1,
    hidden=True,
    desc="A plugin that use LLM to determine user intent",
    version="0.1",
    author="lanvent",
)
class Intent(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Hello] inited")
        self.config = super().load_config()

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        
        content = e_context["context"].content
        logger.debug("[Hello] on_handle_context. content: %s" % content)
        
        e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑
