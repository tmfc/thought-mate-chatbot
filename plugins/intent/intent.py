# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
from config import conf
import random


@plugins.register(
    name="Intent",
    desire_priority=900,
    desc="A plugin that use LLM to determine user intent",
    version="0.1",
    author="william Jin",
)
class Intent(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Intent] inited")
        self.config = super().load_config()
        self.intent_list = self.config.get("intent_list")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        
        content = e_context["context"].content
        logger.info("[Intent] on_handle_context. content: %s" % content)
        intent = self.get_intent(content)
        
        logger.info("[Intent] user intent is: %s" % intent)
        # 方便测试逻辑
        # reply = Reply()
        # reply.type = ReplyType.TEXT
        # reply.content = "Your intent is %s" % intent
        # e_context["reply"] = reply
        # e_context.action = EventAction.BREAK_PASS  # 返回用户意图，并终止后续处理
        
        # 正式逻辑
        e_context["intent"] = intent
        e_context.action = EventAction.CONTINUE # 继续处理
        
    def get_intent(self, content):
        prompt = "请判断以下用户指令```%s```的意图是以下意图中的哪一个：```%s```" % (content, ','.join(self.intent_list))
        # TODO:调用LLM来判断用户意图
        return random.sample(self.intent_list, 1) # 测试逻辑，随机选择意图
