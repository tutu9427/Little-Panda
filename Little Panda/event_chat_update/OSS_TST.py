import requests
import json
from datetime import datetime
import cx_Oracle
import time
import traceback

bssDatabaseCRM = 'CRM/1jian8Shu)@172.16.24.120:1525/ccee'
ossDatabaseOD = 'ossod/smart123@10.10.194.215:11521/cc'

ossUrl = 'http://10.10.194.216:8000/oss/tmfapi/serviceOrder/v1/event/notification'
headers = {'Content-Type': 'application/json'}




class OSS_TST:
    def __init__(self):
        self.bssConnection()
        self.ossConnection()
        self.AcknowledgedRequest = {"href": "", "eventId": "C2024082711120016131", "eventTime": "2024-01-29 15:26:06","eventType": "ServiceOrderStateChangeEvent", "event": {"serviceOrder": {"id": "C202408271112001631", "state": "Acknowledged", "serviceOrderItem": []}}}
        self.completeRequest = {"href": "", "eventId": "P2408280952003303", "eventTime": "2024-01-29 15:26:06","eventType": "ServiceOrderStateChangeEvent", "event": {"serviceOrder": {"id": "C202408280952003251", "state": "Completed","serviceOrderItem": [{"id": "P2408280952003303", "state": "Completed"}]}}}

        self.serviceList = ['HSI', 'Fix Access', 'VoIP', 'IPTV Services Standard', 'Cloud Gaming', 'Cloud Storage','OTT Service', 'eCommerce Hub', 'Kaspersky Small Office Security','Kaspersky Small Office Security']
        self.goodsList = ['CPE', 'ONT', 'ATA', 'UPB', 'Dect Phone']
        self.eventList = ['cesTermination', 'cesModify', 'cesNew', 'cesCOwnership']
        self.resMsgList = []

    def genEventId(self):
        eventId = datetime.now().strftime("%Y%m%d%H%M%S")
        return eventId

    def bssConnection(self):
        self.bssConnectionCRM = cx_Oracle.connect(bssDatabaseCRM)
        self.cursorCRM = self.bssConnectionCRM.cursor()

    def ossConnection(self):
        self.ossConnection = cx_Oracle.connect(ossDatabaseOD)
        self.cursorOss = self.ossConnection.cursor()

    def disconnect(self):
        try:
            if self.cursorOss:
                self.cursorOss.close()
            if self.ossConnection:
                self.ossConnection.close()
            if self.cursorCRM:
                self.cursorCRM.close()
            if self.bssConnectionCRM:
                self.bssConnectionCRM.close()
            # print("数据库已断开-------")
        except Exception:
            print(traceback.format_exc())

    def queryOssOrderNo(self, bssOrderNo):
        print("---------------------------------------------------------------\nBSS订单号：{}".format(bssOrderNo))
        queryOssOrderNoSql = "SELECT VALUE FROM CUST_ORDER_ATTR WHERE ATTR_ID=101398 AND CUST_ORDER_ID={}".format(bssOrderNo)
        self.cursorCRM.execute(queryOssOrderNoSql)
        ossOrderNo = self.cursorCRM.fetchall()[0][0]
        print("OSS订单号：{}".format(ossOrderNo))
        return ossOrderNo

    def queryOssOrderDetail(self):
        queryOssOrderDetailSql="SELECT DISTINCT (C.SPEC_NAME),A.ORD_NO,B.CFS_ID,A.CFS_EVENT_SPEC FROM OSSOD.OM_CFS_ORD A LEFT JOIN OSSOD.SRV_CFS_VER B ON A.ORD_NO =B.CREATE_ORD LEFT JOIN OSSOD.EPCS_SPEC C ON C.SPEC_ID=B.cfs_spec_id WHERE A.CUST_ORD_NO = '{}' ORDER BY C.SPEC_NAME DESC".format(self.ossOrderNo)
        self.cursorOss.execute(queryOssOrderDetailSql)
        ossOrderDetail = self.cursorOss.fetchall()
        return ossOrderDetail

    def sendAcknowledgedRequest(self):
        self.AcknowledgedRequest["eventId"] = self.genEventId()
        self.AcknowledgedRequest["event"]["serviceOrder"]["id"] = self.ossOrderNo
        for item in self.queryOssOrderDetail():
            if item[0] in self.serviceList:
                serviceOrderDict = {"state": "Acknowledged"}
                serviceOrderDict["id"] = item[1]
                self.AcknowledgedRequest["event"]["serviceOrder"]["serviceOrderItem"].append(serviceOrderDict)
        reqMsg = "发送Acknowledged请求，报文：\n{}".format(str(self.AcknowledgedRequest).replace("\'", "\""))
        requestJson = json.dumps(self.AcknowledgedRequest)
        try:
            response = requests.post(url=ossUrl,data=requestJson,headers=headers).text
            if response == '{"code":"0","message":"success"}':
                resMsg = "成功!"

            else:
                raise ValueError("订单Acknowledged 状态回单失败，返回报文为：{}".format(response))

        except ValueError as ve:
            print(ve)

        self.resMsgList.extend([reqMsg,resMsg])


    def sendInprogressRequest(self):
        time.sleep(1)
        inProgressRequest = str(self.AcknowledgedRequest).replace('Acknowledged','InProgress').replace('\'','\"')
        inProgressRequest = json.loads(inProgressRequest)
        inProgressRequest["eventId"] = self.genEventId()

        reqMsg = "发送InProgress请求，报文：\n{}".format(str(inProgressRequest).replace("\'", "\""))
        requestJson = json.dumps(inProgressRequest)

        try:
            response = requests.post(url=ossUrl,data=requestJson,headers=headers).text
            if response == '{"code":"0","message":"success"}':
                resMsg = "成功!"
            else:
                raise ValueError("订单InProgress状态回单失败，返回报文为：{}".format(response))

        except ValueError as ve:
            print(ve)

        self.resMsgList.extend([reqMsg,resMsg])

    def sendGoodsRequest(self, ontModel, ataModel, ataPortNum, cpeDelivery='N', upbDelivery='N', dectPhoneDelivery='N'):
        for event in self.eventList:
            for item in self.queryOssOrderDetail():
                if item[0] in self.goodsList and item[3] == event:
                    time.sleep(1)
                    goodsRequest = {"eventId": "C20240826133400016711", "eventTime": "2024-03-19 17:28:06", "href": "","eventType": "ServiceOrderAttributeValueChangeEvent", "event": {"serviceOrder": {"id": "C202408261334000167", "serviceOrderItem": [{"id": "P2408261334000239", "characteristic": [],"service": {"id": "240826133400000265", "href": "", "name": "", "serviceCharacteristic": [{"id": "serialNumber", "name": "SerialNumber", "valueType": "S","value": "240826133400000265"}]}}]}}}
                    goodsRequest["event"]["serviceOrder"]["id"] = self.ossOrderNo
                    goodsRequest["eventId"] = self.genEventId()
                    goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["id"] = item[1]
                    goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["id"] = item[2]
                    goodsESN = str(item[2])

                    if item[0] == 'ONT':
                        goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S", "value": ontModel}
                        goodsModelDict = {"id": "cfsOnt", "href": "", "name": "ONT"}
                        goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"][
                            "serviceCharacteristic"].append(goodsSpecDict)

                    if item[0] == 'ATA':
                        goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S", "value": ataModel}
                        ataPostDict = {"id": "posPortNumber", "name": "POS ports number", "valueType": "S", "value": ataPortNum}
                        goodsModelDict = {"id": "cfsATA", "href": "", "name": "ATA"}
                        goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(ataPostDict)
                        goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"][
                            "serviceCharacteristic"].append(goodsSpecDict)

                    if item[0] == 'UPB':
                        goodsModelDict = {"id": "cfsUpb", "href": "", "name": "UPB"}

                        if upbDelivery == 'Y':
                            goodsESN = ""

                        else:
                            goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S", "value": "Yuzhu UPB"}
                            goodsSpecDict1 = {"id": "vendor", "name": "vendor", "valueType": "S","value": "Yuzhu UPB vendor"}
                            goodsSpecDict2 = {"id": "rgMode", "name": "rgMode", "valueType": "S","value": "Yuzhu UPB rgMode"}
                            goodsSpecDict3 = {"id": "equipmentName", "name": "equipmentName", "valueType": "S","value": "Yuzhu UPB equipmentName"}
                            goodsSpecDict4 = {"id": "materialCode", "name": "materialCode", "valueType": "S","value": "Yuzhu UPB materialCode"}

                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict1)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict2)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict3)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict4)


                    if item[0] == 'CPE':
                        goodsModelDict = {"id": "cfsCpe", "href": "", "name": "CPE"}

                        if cpeDelivery == 'Y':
                            goodsESN = ""

                        else:
                            goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S", "value": "Yuzhu Mesh Wifi"}
                            goodsSpecDict1 = {"id": "vendor", "name": "vendor", "valueType": "S","value": "Yuzhu Mesh Wifi vendor"}
                            goodsSpecDict2 = {"id": "rgMode", "name": "rgMode", "valueType": "S","value": "Yuzhu Mesh Wifi rgMode"}
                            goodsSpecDict3 = {"id": "equipmentName", "name": "equipmentName", "valueType": "S","value": "Yuzhu Mesh Wifi equipmentName"}
                            goodsSpecDict4 = {"id": "materialCode", "name": "materialCode", "valueType": "S","value": "Yuzhu Mesh Wifi materialCode"}

                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict1)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict2)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict3)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict4)

                    if item[0] == 'Dect Phone':
                        goodsModelDict = {"id": "cfsCpe", "href": "", "name": "CPE"}

                        if dectPhoneDelivery == 'Y':
                            goodsESN = ""

                        else:
                            goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S", "value": "Yuzhu Dect Phone"}
                            goodsSpecDict1 = {"id": "vendor", "name": "vendor", "valueType": "S","value": "Yuzhu Dect Phone vendor"}
                            goodsSpecDict2 = {"id": "rgMode", "name": "rgMode", "valueType": "S","value": "Yuzhu Dect Phone rgMode"}
                            goodsSpecDict3 = {"id": "equipmentName", "name": "equipmentName", "valueType": "S","value": "Yuzhu Dect Phone equipmentName"}
                            goodsSpecDict4 = {"id": "materialCode", "name": "materialCode", "valueType": "S","value": "Yuzhu Dect Phone materialCode"}

                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict1)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict2)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict3)
                            goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"].append(goodsSpecDict4)

                    if item[3] in ('cesTermination','cesModify'):
                        goodsSpecDict = {"id": "model", "name": "Model", "valueType": "S"}
                        oldGoodsSpecSql = "SELECT ATTR_VAL FROM SRV_CFS_CTSUB_ATTR WHERE CFS_ID = {} AND ATTR_SPEC_ID='CFS.model'".format(item[2])
                        self.cursorOss.execute(oldGoodsSpecSql)
                        oldGoodsModel = self.cursorOss.fetchall()[0][0]
                        goodsSpecDict["value"] = oldGoodsModel

                    goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceCharacteristic"][0]['value'] = goodsESN
                    goodsRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["service"]["serviceSpecification"] = goodsModelDict
                    reqMsg = "发送{} {}请求，报文：\n{}".format(item[0],item[3], str(goodsRequest).replace("\'", "\""))
                    requestJson = json.dumps(goodsRequest)

                    try:
                        response = requests.post(url=ossUrl, data=requestJson, headers=headers).text
                        if response == '{"code":"0","message":"success"}':
                            resMsg = "成功!"
                        else:
                            raise ValueError("实物{}回单失败，返回为：{}".format(item, response))

                    except ValueError as ve:
                        print(ve)

                    self.resMsgList.extend([reqMsg,resMsg])


    def sendCompleteRequest(self):
        self.completeRequest["event"]["serviceOrder"]["id"] = self.ossOrderNo
        time.sleep(1)
        for event in self.eventList:
            for item in self.queryOssOrderDetail():
                if item[0] == 'HSI' and item[3] == event:
                        time.sleep(1)
                        self.completeRequest["eventId"] = self.genEventId()
                        self.completeRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["id"] = item[1]
                        reqMsg = "发送{} {} Complete请求，报文：\n{}".format(item[0], item[3],str(self.completeRequest).replace("\'", "\""))
                        requestJson = json.dumps(self.completeRequest)

                        try:
                            response = requests.post(url=ossUrl, data=requestJson, headers=headers).text
                            if response == '{"code":"0","message":"success"}':
                                resMsg = "成功!"
                            else:
                                raise ValueError("{} Complete状态回单失败，返回报文为：{}".format(item[0],response))

                        except ValueError as ve:
                            print(ve)

                        self.resMsgList.extend([reqMsg,resMsg])



            for item in self.queryOssOrderDetail():
                if item[0] in self.serviceList and item[0] != 'HSI' and item[3] == event:
                        time.sleep(1)
                        self.completeRequest["eventId"] = self.genEventId()
                        self.completeRequest["event"]["serviceOrder"]["serviceOrderItem"][0]["id"] = item[1]
                        reqMsg = "发送{} {} Complete请求，报文：\n{}".format(item[0], item[3],str(self.completeRequest).replace("\'", "\""))
                        requestJson = json.dumps(self.completeRequest)

                        try:
                            response = requests.post(url=ossUrl, data=requestJson, headers=headers).text
                            if response == '{"code":"0","message":"success"}':
                                resMsg = "成功!"
                            else:
                                raise ValueError("{} Complete状态回单失败，返回报文为：{}".format(item[0],response))

                        except ValueError as ve:
                            print(ve)

                        self.resMsgList.extend([reqMsg,resMsg])



    def newConnectionTST(self,bssOrderNo, ontModel="GN630V",ataModel="IAG400",ataPortNum="4",cpeDelivery="N",upbDelivery="N",dectPhoneDelivery='N'):

        self.ossOrderNo = self.queryOssOrderNo(bssOrderNo)
        self.sendAcknowledgedRequest()
        self.sendInprogressRequest()
        self.sendGoodsRequest(ontModel, ataModel, ataPortNum,cpeDelivery, upbDelivery,dectPhoneDelivery)
        self.sendCompleteRequest()
        self.disconnect()
        resMsg = ("\n".join(self.resMsgList))
        print (resMsg)


#
# a=OSS_TST()
# a.newConnectionTST("2502000039305045")