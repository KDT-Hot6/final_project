# final\_project

### Keyword extractor

* pure Python code
* author: Lovit \(Hyunjoong Kim\)
* reference: [Kim, H. J., Cho, S., & Kang, P. \(2014\). KR-WordRank: An Unsupervised Korean Word Extraction Method Based on WordRank. Journal of Korean Institute of Industrial Engineers, 40\(1\), 18-33](https://github.com/lovit/KR-WordRank/raw/master/reference/2014_JKIIE_KimETAL_KR-WordRank.pdf)
* code: [https://github.com/lovit/KR-WordRank](https://github.com/lovit/KR-WordRank)



* HITS algorithm을 이용한 키워드 추출 라이브러리를 제공합니다.  
* graph ranking 알고리즘을 사용하기 위해 substring graph를 생성합니다.  
* 한국어 토크나이저 기능은 substring 그래프를 활용해 처리됩니다.  

#### Code

`/keyword/key_sentences.py`에서 활용 예시들을 보실 수 있습니다.  

`DATA_SAVE_PATH`를 변경하면 원하는 위치에 KR-WordRank를 통해 처리된 데이터들을 저장할 수 있습니다.

```python
DATA_SAVE_PATH = '/home/ubuntu/hot6/data/hot6_db_keysentences_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
```

도메인에 따라서 사용되는 stopwords가 변경되어야 좋은 키워드를 추출할 수 있습니다.    
일반적으로 다른 리뷰들에서 반복되는 키워드들을 stopwords로 설정하면 준수한 성능을 보이는 것을 확인하실 수 있습니다. TF-IDF, BM25 알고리즘 등을 활용하실 수도 있습니다.  

#### Setup

```text
pip install krwordrank
```

#### Requirements

* Python &gt;= 3.5
* numpy
* scipy

### SentenceBERT

Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks \(EMNLP 2019\) 논문, 직접 수집하고 제작한 음식점 리뷰 데이터를 통해 Korean Sentence BERT를 학습하였습니다.



