# 사용방법

#### 1. 미리학습된 모델로 어텐션 시각화하는 모듈 사용방법

- head_view_bert.ipynb 파일은 colab에서 실행하시면 됩니다.
- 다만 테스트를 위해서는 토크나이저 파일을 임포트 해주셔야합니다.
- **파일 경로**
  - KoBERT-Transformers/tokenization_kobert.py
- sentence_a 변수에 테스트 하고 싶은 문장 넣으시고 돌리면 됩니다.

#### 2.Transformer를 통한 개체명 인식 모듈 사용방법 

- 기존 프로젝트는 개체명 인식 + 챗봇이나 챗봇 기능은 필요가 없어 저는 출력 부분을 막아두었습니다.
[출처]https://github.com/eagle705/pytorch-transformer-chatbot
- 소스코드 다운받으신 후 `python inference.py` 명령어로 실행하시면 됩니다.
- **출처 링크에 있는 원프로젝트로 테스트하시는걸 추천드립니다.**
