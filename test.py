import requests
from bs4 import BeautifulSoup

#예약희망일
start_date='20250304'
#숙박일수
res_day=1
end_date=str(int(start_date)+res_day-1)

slack_url = "https://hooks.slack.com/services/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"
def sendSlackWebHook(strText):
    headers = {
        "Content-type" : "application/json"
    }
    data = {
        "text":strText
    }
    res = requests.post(slack_url, headers=headers, json=data)
    if res.status_code == 200:
        return "전송완료"
    else:
        return "전송오류"
    

# 사이트 번호와 이름 매핑
site_mapping = {
    "1": "데크사이트",
    "2": "파쇄석사이트",
    "3": "카라반캠핑A(4인용)",
    "4": "카라반캠핑B(3인용)",
    "5": "카라반캠핑C(2인용)"
}
url = "https://m.thankqcamping.com/resv/axResCampSite.hbb"
payload = {
    'campseq': '16706',
    'res_dt': start_date,
    'res_edt': end_date,
    'res_days': str(res_day),
    'site_tp': ''
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://m.thankqcamping.com/resv/view.hbb?cseq=16706&go_main=Y&path=RP'
}
previous_output=''
try:
    response = requests.post(url, data=payload, headers=headers)
    response.encoding = 'utf-8'  # 한글 응답을 올바르게 표시하기 위해 인코딩 설정
    soup = BeautifulSoup(response.text, 'html.parser')

    # class가 'q_tip'인 span 태그 모두 찾기
    html_list = soup.find_all('span', class_='q_tip')

    # 결과를 한 번에 합쳐서 출력
    output = f"{start_date}({str(res_day)}박) 조회결과\n"  # 조회결과 제목
    sendYN = False  # 예약 가능한 사이트 여부

    for idx, tag in enumerate(html_list, start=1):
        status = tag.text.strip()  # 텍스트 추출
        site_name = site_mapping.get(str(idx), f"사이트{idx}")  # 매핑된 이름 가져오기

        if "예약가능" in status:
            sendYN = True  # 예약 가능한 사이트가 하나라도 있으면 True
            output += f"{site_name} : {status}\n"

    slack_result = sendSlackWebHook(output)
    print(slack_result)
    previous_output = output  # 현재 output을 이전 기록으로 저장

except Exception as e:
    print(f"오류 발생: {str(e)}")
