# config.py - 请求模板配置
from settings import username, password


def create_customer_body(cert_no):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://com.ztesoft.zsmart/xsd">
    <soapenv:Header>
        <xsd:AuthHeader>
            <Username>{username}</Username>
            <Password>{password}</Password>
        </xsd:AuthHeader>
    </soapenv:Header>
    <soapenv:Body>
        <xsd:CreateCustBO>
            <!-- 保持原有XML结构不变 -->
            <CustType>A</CustType>
            <CertType>02</CertType>
            <CertNO>{cert_no}</CertNO>
            <CertExpDate>2030-09-08</CertExpDate>
            <FirstName>AUTO</FirstName>
            <LastName>tuzki</LastName>
            <UserPwd>111111</UserPwd>
            <CustAttrDtoList>
                <CustAttrCode>POST_CUST_COUNTRY_OF_BIRTH</CustAttrCode>
                <AttrValue>LU</AttrValue>
            </CustAttrDtoList>
            <CustAttrDtoList>
                <CustAttrCode>POST_CUST_PLACE_OF_BIRTH</CustAttrCode>
                <AttrValue>jiangsu</AttrValue>
            </CustAttrDtoList>
            <CustAttrDtoList>
                <CustAttrCode>POST_GROUP_EMPLOYEE</CustAttrCode>
                <AttrValue>N</AttrValue>
            </CustAttrDtoList>
            <CustAttrDtoList>
                <CustAttrCode>POST_MANUAL_BLOCKING_ORDER</CustAttrCode>
                <AttrValue>NULL</AttrValue>
            </CustAttrDtoList>
            <Gender>2</Gender>
            <Title>2</Title>
            <DefaultLanguage>2</DefaultLanguage>
            <BirthDate>1999-05-16</BirthDate>
            <ContactEmail>gu22o.mengmeng@post.lu</ContactEmail>
            <AddressID>000000050953#000000000000</AddressID>
            <Nationality>GE</Nationality>
            <CustomerSegment>1</CustomerSegment>
            <DocIssuingCountry>LU</DocIssuingCountry>
            <ContactPhone>3528989893</ContactPhone>
        </xsd:CreateCustBO>
    </soapenv:Body>
</soapenv:Envelope>"""
