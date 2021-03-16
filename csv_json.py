import re
import csv, json

def data2hangul(data):
    data = data.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    data = re.sub(pattern = r'\[[^]]*\]', repl='', string = data)
    return data


def csv2json(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8-sig", newline="") as input_file, \
            open(output_file_path, "w", encoding="utf-8", newline="") as output_file:
        reader = csv.reader(input_file)
        col_names = next(reader) # csv에서 컬럼명을 받아옵니다. 
        docs = [] # JSON 객체를 담습니다. 
        id_count = 1
        for cols in reader:
            doc = {col_name: data2hangul(col) for col_name, col in zip(col_names, cols) if col_name in ['Restaurant','Review']}
            doc['id'] = id_count
            id_count += 1
            docs.append(doc)
        print(json.dumps(docs, ensure_ascii=False), file=output_file)

input_path = '/Users/byeongheon/programmers/final_project/data/(연세대) 37.560873_126.9353833_df.csv'
output_path = '/Users/byeongheon/programmers/final_project/data/test.json'
csv2json(input_path, output_path)

#{"": "0", "Restaurant": "흥부찜닭-신촌점", 
# "UserID": "hs**님", "Menu": "흥부 간장찜닭 （순살）/1(맛 선택(2단계 기본맛))", 
# "Review": "기본맛 맛있게맵고 양도 많네요", "Total": "5", "Taste": "5", "Quantity": "5", 
# "Delivery": "4", "Date": "23시간 전", "OperationTime": "15:21 - 22:00", 
# "Address": "서울 서대문구 창천동 33-43 2층"},