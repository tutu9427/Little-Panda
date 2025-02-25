import openai
import json


class aiAnalysis:
    def __init__(self, api_key="sk-zk7Bkm7cgVmE2GPlL9I4IYTCQG3juQXYQqAIqWxrFpzRQsAgd9N0",
                 api_base="https://model-bridge.okeeper.com/v1",
                 model="gpt-3.5-turbo",
                 temperature=0.5):
        """
        初始化aiAnalysis类，设置OpenAI API的配置参数。

        :param api_key: OpenAI API密钥，默认从环境变量中获取。
        :param api_base: OpenAI API的基础URL，默认从环境变量中获取。
        :param model: 使用的模型，默认为"gpt-3.5-turbo"。
        :param temperature: 模型的温度参数，默认为0.5。
        """
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.temperature = temperature
        self.system_message = self._load_system_message()

        # 配置OpenAI客户端
        openai.api_key = self.api_key
        openai.api_base = self.api_base

    def _load_system_message(self):
        """
        加载系统消息模板。
        """
        system_message = """
        你是一个马来西亚的一个电信营业厅的营业员，这时有一位客户来到你的营业厅，需要创建资料，你需要提取客户的以下信息，将提取到的以json的格式返回,没有提取到的不返回：
        "address": "居住地址",
        "birthday": 生日，格式为Unix时间戳,
        "certNbr": "证件号码",
        "certTypeCode": "证件类型，有MYKAD，MYKAS，PASSPORT，MYPR和MYTENTERA五种选择",
        "contactManName": "联系人姓名，如果是汉字，需要转换成拼音再返回",
        "emailAddr": "联系人邮箱",
        "mobileAreaCode": "联系号码的国家码，默认为60，可以根据联系人所在国家得出结论",
        "mobilePhone": "联系人的电话号码",
        "primaryFlag": "是否为主要联系人，是为Y，不是为N"
        "custName": "客户姓名，如果是汉字，需要转换成拼音再返回，如果是英文，不需要转换大小写，直接返回",
        "email": "客户邮箱",
        "gender": "客户性别，有F和M两个选项",
        "phoneNumber": "客户的电话号码",
        """
        return system_message.strip()

    def call_openai(self, user_message):
        """
        调用OpenAI的API进行分析。

        :param user_message: 用户提供的消息内容。
        :return: OpenAI API的响应对象。
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": f"请分析以下文本并提取客户信息：{user_message}"}
                ],
                temperature=self.temperature
            )
            return response
        except Exception as e:
            raise ValueError(f"OpenAI API调用失败: {str(e)}")

    def parse_analysis_result(self, model_response):
        """
        解析OpenAI API的响应结果，提取客户信息。

        :param model_response: OpenAI API的响应对象。
        :return: 解析后的客户信息字典。
        """
        try:
            analysis_result = json.loads(model_response.choices[0].message.content)
            return analysis_result

        except json.JSONDecodeError:
            raise ValueError("无法解析OpenAI的响应结果，响应内容不是有效的JSON格式。")
        except IndexError:
            raise ValueError("OpenAI的响应中没有有效的消息内容。")
        except Exception as e:
            raise ValueError(f"解析OpenAI响应时出现错误: {str(e)}")

    def replace_json(self, source_json, target_json):
        """
        将目标JSON合并到源JSON中。

        :param source_json: 源JSON。
        :param target_json: 目标JSON。
        :return: 合并后的JSON字符串。
        """
        try:
            # 如果json1是字典
            if isinstance(source_json, dict):
                for key, value in source_json.items():
                    # 如果key在json2中，则替换值
                    if key in target_json:
                        source_json[key] = target_json[key]
                    # 递归处理嵌套的字典或列表
                    elif isinstance(value, (dict, list)):
                        self.replace_json(value, target_json)
            # 如果json1是列表
            elif isinstance(source_json, list):
                for item in source_json:
                    self.replace_json(item, target_json)
            return source_json

        except Exception as e:
            raise ValueError(f"JSON合并过程中出现错误: {str(e)}")


# # 定义原始JSON结构
# creste_customer = {
#     "address": "Yuzhu Country",
#     "attrs": [
#         {
#             "attrCode": "TM_IND_IMPORTANCE_TAG",
#             "attrValue": "Not Applicable"
#         },
#         {
#             "attrCode": "EXP_CUST_NATIONALITY",
#             "attrValue": "MYS"
#         },
#         {
#             "attrCode": "UM_NATIONALITY",
#             "attrValue": "MYS"
#         }
#     ],
#     "birthday": 942163200000,
#     "certNbr": "010503232333",
#     "certTypeCode": "MYKAD",
#     "contactManList": [
#         {
#             "contactManName": "Yuzhu",
#             "emailAddr": "Yuzhu@qq.com",
#             "mobileAreaCode": "60",
#             "mobilePhone": "13222222222",
#             "primaryFlag": "Y"
#         }
#     ],
#     "custDocList": [
#         {
#             "docId": "cmV0OmNybS9maWxlL2JkZWNkZTI4YjhmZS8yMDI1MDIxMS8xNS85LzUtMzIwMy5wbmc=",
#             "docName": "010503232333.png",
#             "docTypeId": "2",
#             "operationType": "A",
#             "state": "A",
#             "stateDate": 1739257745807
#         }
#     ],
#     "custName": "Yuzhu",
#     "email": "Yuzhu@qq.com",
#     "gender": "F",
#     "netType": "A",
#     "phoneNumber": "13389090321",
#     "stdAddrId": "520000",
#     "zipcode": "52000"
# }
#
# # 使用优化后的代码
# try:
#     # 初始化aiAnalysis实例
#     ai_analyzer = aiAnalysis()
#
#     # 用户消息
#     user_message = """
#     我是来自Taipei的Mary，我在2000年1月1日出生，我有一张护照，证件号码是EK282839，
#     我的联系人是来自东北的马丽，她是我的主要联系人，她的电话号码是132121221，邮箱是Mali@qq.com，我的电话号码是1355555555，
#     我的邮箱是Mary@qq.com
#     """
#
#     # 调用OpenAI进行分析
#     response = ai_analyzer.call_openai(user_message)
#
#     # 解析分析结果
#     analysis_result = ai_analyzer.parse_analysis_result(response)
#
#     # 合并JSON
#     merged_json = ai_analyzer.replace_json(creste_customer, analysis_result)
#     print("合并后的JSON：")
#     print(merged_json)
# except Exception as e:
#     print(f"程序执行失败: {str(e)}")
