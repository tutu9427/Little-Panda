import json
from datetime import datetime
import requests

class apiRequest:
    BASE_URL = "http://10.10.194.74:80"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_token_here"
    }

    def __init__(self):
        pass  # 可以在这里初始化其他需要的属性

    def _call_api(self, endpoint, payload):
        """
        统一调用接口的方法。

        :param endpoint: 接口的具体路径
        :param payload: 发送的 JSON 数据
        :return: 接口响应
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.post(url, headers=self.HEADERS, json=payload)  # 使用 json 参数
            # response.raise_for_status()  # 如果响应状态码不是 200，将引发异常
            # return response.json()
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_desc = response.json().get("errorDesc", "No error description provided")
                raise ValueError(error_desc)

            else:
                response.raise_for_status()  # 对于其他非200状态码，引发异常
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Response: {response.text}")  # 输出响应内容
        except ValueError as ve:
            print(f"Value error occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



    def _generate_customer_payload(self, custName):
        """
        生成客户请求的 JSON 数据。

        :param custName: 客户姓名
        :return: 生成的 JSON 字符串
        """
        current_time = datetime.now().strftime('00%m%d%H%M%S')

        data = {
            "address": "saaa, bbbb, 10560 Pulau Pinang, Pulau Pinang",
            "attrs": [{"attrCode": "TM_IND_IMPORTANCE_TAG"}],
            "birthday": 958492800000,
            "certExpDate": 1993737600000,
            "certNbr": current_time,
            "certTypeCode": "MYKAD",
            "contactManList": [{
                "contactManName": custName,
                "emailAddr": "Yuzhu@qq.com",
                "mobileAreaCode": "60",
                "mobilePhone": "13222444212",
                "primaryFlag": "Y"
            }],
            "custDocList": [{
                "docId": "m/+07vM3ZlMqUjTDszmljmm1vgmcQ0VS9h8REeLU+K9/JYbXljvDrM2SzTMiL7BTsOi1UqSRn1arQ5rqZc4EjLldA179kMxPu3lxzyB/J109FhmoX+ExAiIsk2oWnNnh0RcbH6rPZtR1",
                "docName": "3f881e2b-5b92-4c2e-b248-5dda9955d75b",
                "docTypeId": "2",
                "operationType": "A",
                "state": "A",
                "stateDate": 1738893220025
            }],
            "custFlag": "V",
            "custName": custName,
            "custType": "A",
            "email": "te399@qq.com",
            "gender": "F",
            "netType": "A",
            "phoneNumber": "124785698745"
        }
        print(type(data))
        return data  # 返回字典而不是 JSON 字符串


    def create_customer(self, customer_data):
        """
        创建客户并返回客户 ID。

        :param custName: 客户姓名
        :return: 客户 ID 或 None
        """
        try:
            # 调用 _call_api 方法创建客户
            response = self._call_api("cvbs/custc/v1/custs", customer_data)
            # 从响应中提取客户 ID
            customer_id = response.get("custId")
            return customer_id

        except Exception as e:
            # 如果发生任何异常，打印错误消息并返回 None
            print(f"Failed to create customer: {e}")
