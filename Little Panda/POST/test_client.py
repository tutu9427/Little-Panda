# test_client.py - 主执行文件（兼容pytest和直接执行）
import pytest  # 新增依赖
import requests
import re
import random
from settings import global_url
from config import create_customer_body


class TestCustomerAPI:  # 正确1：测试类名必须以Test开头（大驼峰）
    @pytest.mark.smoke  # 可选：添加测试标记
    def test_create_customer_success(self):  # 正确2：测试方法名必须test_开头
        """
        客户创建成功场景测试
        Metadata:
          - Author: Tuzki
          - Created: 2025-02-22
          - CaseID: TC-API-001
        """
        # 生成唯一客户编号
        cert_no = f"{random.randint(10000000, 99999999)}"

        # 构造请求头
        headers = {
            "action": "urn:CreateCustomer",
            "charset": "utf-8",
            "Content-Type": "text/xml; charset=utf-8"
        }

        try:
            # 发送SOAP请求
            response = requests.post(
                url=global_url,
                headers=headers,
                data=create_customer_body(cert_no),
                verify=False,
                timeout=10
            )

            # 验证响应状态（pytest断言方式）
            assert response.status_code == 200, f"预期200状态码，实际得到{response.status_code}"

            # 解析客户代码
            match = re.search(r'<CustCode>([1-9]\d{4,})</CustCode>', response.text)
            assert match is not None, "响应中未找到CustCode字段"

            print(f"✅ 客户创建成功 | CertNo: {cert_no} | CustCode: {match.group(1)}")
            return match.group(1)

        except requests.exceptions.RequestException as e:
            pytest.fail(f"请求失败: {str(e)}")  # 正确3：使用pytest失败断言
        except Exception as e:
            pytest.fail(f"处理失败: {str(e)}")


# 保留直接执行能力（不影响pytest）
if __name__ == "__main__":
    from unittest import TestCase, main

    main()  # 使用unittest兼容执行