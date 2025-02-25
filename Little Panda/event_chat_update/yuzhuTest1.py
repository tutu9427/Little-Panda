import openai
import json

class aiAnalysis:
    openai.api_key = "sk-zk7Bkm7cgVmE2GPlL9I4IYTCQG3juQXYQqAIqWxrFpzRQsAgd9N0"
    openai.api_base = "https://model-bridge.okeeper.com/v1" #在这里设置即可,需要特别注意这里的/v1是必须的，否则报错。前面的地址注意替换即可。
    model = "gpt-3.5-turbo"
    temperature = 0.5
    sysMessage = """
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

    def __init__(self):
        pass

    def createModel(self, userMsg):
        # 调用OpenAI的API进行分析
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{self.sysMessage}"},
                {"role": "user", "content": f"请分析以下文本并提取客户信息：{userMsg}"}
            ],
            temperature=self.temperature
        )
        return response

    def analysisResult(self, modelResopnse):
        analysis_result = json.loads(modelResopnse.choices[0].message.content)
        print("分析成功，这是我获取到的信息：")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")
        return analysis_result

    def replace_json(self, source_json, target_json):
        """
        将目标JSON合并到源JSON中
        :param source_json: 源JSON
        :param target_json: 目标JSON
        :return: 合并后的JSON
        """
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

        return json.dumps(source_json, indent=4)


# 定义原始JSON结构
cresteCustomer = {
    "address": "Yuzhu Country",
    "attrs": [
        {
            "attrCode": "TM_IND_IMPORTANCE_TAG",
            "attrValue": "Not Applicable"
        },
        {
            "attrCode": "EXP_CUST_NATIONALITY",
            "attrValue": "MYS"
        },
        {
            "attrCode": "UM_NATIONALITY",
            "attrValue": "MYS"
        }
    ],
    "birthday": 942163200000,
    "certNbr": "010503232333",
    "certTypeCode": "MYKAD",
    "contactManList": [
        {
            "contactManName": "Yuzhu",
            "emailAddr": "Yuzhu@qq.com",
            "mobileAreaCode": "60",
            "mobilePhone": "13222222222",
            "primaryFlag": "Y"
        }
    ],
    "custDocList": [
        {
            "docId": "cmV0OmNybS9maWxlL2JkZWNkZTI4YjhmZS8yMDI1MDIxMS8xNS85LzUtMzIwMy5wbmc=",
            "docName": "010503232333.png",
            "docTypeId": "2",
            "operationType": "A",
            "state": "A",
            "stateDate": 1739257745807
        }
    ],
    "custName": "Yuzhu",
    "email": "Yuzhu@qq.com",
    "gender": "F",
    "netType": "A",
    "phoneNumber": "13389090321",
    "stdAddrId": "520000",
    "zipcode": "52000"
}

# # 用户消息
# user_message = """
# 我是来自Taipei的Mary，我在2000年1月1日出生，我有一张护照，证件号码是EK282839，
# 我的联系人是来自中国东北的马丽，她是我的主要联系人，她的电话号码是132121221，邮箱是Mali@qq.com，我的电话号码是1355555555，
# 我的邮箱是Mary@qq.com
# """
#
# a=aiAnalysis()
# model = a.createModel(user_message)
# result = a.analysisResult(model)
# b=a.replace_json(cresteCustomer,result)
# print(b)


