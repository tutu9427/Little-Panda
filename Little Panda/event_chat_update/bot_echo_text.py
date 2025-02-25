# !/usr/bin/env python

import argparse
import logging
import settings
from dingtalk_stream import AckMessage
import dingtalk_stream
from test_client import TestCustomerAPI
from OSS import OSS
from OSS_TST import OSS_TST
from bssApi import apiRequest
from dingtalk_info_deal import convert_dingtalk_name


def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client_id', dest='client_id', required=True,
        help='app_key or suite_key from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--client_secret', dest='client_secret', required=True,
        help='app_secret or suite_secret from https://open-dev.digntalk.com'
    )
    options = parser.parse_args()
    return options


class EchoTextHandler(dingtalk_stream.ChatbotHandler):
    def __init__(self, logger: logging.Logger = None):
        super(dingtalk_stream.ChatbotHandler, self).__init__()
        if logger:
            self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        text = incoming_message.text.content.strip()
        sender = incoming_message.sender_nick

        if "回单" in text:
            numbers = [char for char in text if char.isdigit()]
            numbers_str = ''.join(numbers)
            try:
                if "TST" in text:
                    a = OSS_TST()
                    b = a.newConnectionTST(bssOrderNo=numbers_str, ontModel="GN630V", ataModel="H516C", ataPortNum="16",
                                           cpeDelivery="N", upbDelivery="N", dectPhoneDelivery='N')

                else:
                    a = OSS()
                    b = a.newConnection(bssOrderNo=numbers_str, ontModel="GN630V", ataModel="H516C", ataPortNum="16",
                                        cpeDelivery="N", upbDelivery="N", dectPhoneDelivery='N')
                response = "好了，你瞅瞅"

            except Exception as e:
                response = "不行，报错了"

        elif "创建" in text and "客户" in text:
            custName = convert_dingtalk_name(sender)
            createRequest = apiRequest()
            request = createRequest._generate_customer_payload(custName)
            try:
                custId = createRequest.create_customer(request)
                response = f"创建成功，你的客户名为{custName},客户ID为{custId}"
            except Exception as e:
                print(f"创建失败: {str(e)}")

        elif "POST创" in text and "客" in text:
            cert_no = convert_dingtalk_name(sender)
            createRequest = apiRequest()
            request = settings.create_customer_body(cert_no)
            try:
                CustCode = TestCustomerAPI.test_create_customer_success(request)
                response = f"创建成功，你的客户CustCode为{CustCode:}"
            except Exception as e:
                print(f"创建失败: {str(e)}")

        else:
            response = "你想说啥"

        print(response)
        self.reply_text(response, incoming_message)
        return AckMessage.STATUS_OK, 'OK'


def main():
    logger = setup_logger()
    options = define_options()

    credential = dingtalk_stream.Credential(options.client_id, options.client_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.chatbot.ChatbotMessage.TOPIC, EchoTextHandler(logger))
    client.start_forever()


if __name__ == '__main__':
    main()

