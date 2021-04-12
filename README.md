# final\_project

## Keyword extractor

![KR-wordrank](https://user-images.githubusercontent.com/23492454/114338713-9c9b0b00-9b8e-11eb-9fa9-bb0194e4d36c.png)

* pure Python code
* author: Lovit \(Hyunjoong Kim\)
* reference: [Kim, H. J., Cho, S., & Kang, P. \(2014\). KR-WordRank: An Unsupervised Korean Word Extraction Method Based on WordRank. Journal of Korean Institute of Industrial Engineers, 40\(1\), 18-33](https://github.com/lovit/KR-WordRank/raw/master/reference/2014_JKIIE_KimETAL_KR-WordRank.pdf)
* code: [https://github.com/lovit/KR-WordRank](https://github.com/lovit/KR-WordRank)
* HITS algorithm을 이용한 키워드 추출 라이브러리를 제공합니다.  
* graph ranking 알고리즘을 사용하기 위해 substring graph를 생성합니다.  
* 한국어 토크나이저 기능은 substring 그래프를 활용해 처리됩니다.  

### Code

`/keyword/key_sentences.py`에서 활용 예시들을 보실 수 있습니다.

`DATA_SAVE_PATH`를 변경하면 원하는 위치에 KR-WordRank를 통해 처리된 데이터들을 저장할 수 있습니다.

```python
DATA_SAVE_PATH = '/home/ubuntu/hot6/data/hot6_db_keysentences_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
```

도메인에 따라서 사용되는 stopwords가 변경되어야 좋은 키워드를 추출할 수 있습니다.  
일반적으로 다른 리뷰들에서 반복되는 키워드들을 stopwords로 설정하면 준수한 성능을 보이는 것을 확인하실 수 있습니다. TF-IDF, BM25 알고리즘 등을 활용하실 수도 있습니다.

### Setup

```text
pip install krwordrank
```

### Requirements

* Python &gt;= 3.5
* numpy
* scipy

## SentenceBERT

Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks \(EMNLP 2019\) 논문, 직접 수집하고 제작한 음식점 리뷰 데이터를 통해 Korean Sentence BERT를 학습하였습니다.

기본 base 코드는 다음 링크에 있으니 참고해주시길 바랍니다.    
[https://github.com/BM-K/KoSentenceBERT\_SKTBERT](https://github.com/BM-K/KoSentenceBERT_SKTBERT)  

![sentenceBERT](https://user-images.githubusercontent.com/23492454/114338837-dcfa8900-9b8e-11eb-80b5-ad926c76582f.png)

현재 KoSentenceBERT는 다음과 같은 setup 과정이 없으면 동작하지 않습니다. 

### Setup 

Sentence-BERT의 토크나이저가 4.1.0 버전 이상에서 동작하여 라이브러리를 수정하였습니다.    
**huggingface transformer, sentence transformers, tokenizers** 라이브러리 코드를 직접 수정하므로 가상환경에서 환경을 세팅하시길 바랍니다.  

```text
git clone https://github.com/SKTBrain/KoBERT.git
cd KoBERT
pip install -r requirements.txt
pip install .
cd ..
git clone https://github.com/BM-K/KoSentenceBERT_SKTBERT.git
pip install -r requirements.txt
!pip uninstall transformers
!pip install transformers = 4.1.1
!pip uninstall tokenizers
!pip install tokenizers = 0.9.4
```

tokenizers 의 init.py를 다음과 같이 수정해줍니다.  

```text
__version__ = "0.5.2"

from dataclasses import dataclass,field

try:
    import tokenizers
    _tokenizers_available=True
except ImportError:
    _tokenizers_available=False

def is_tokenizers_available():
    return _tokenizers_available


@dataclass(frozen=True, eq=True)
class AddedToken:
    """
    AddedToken represents a token to be added to a Tokenizer An AddedToken can have special options defining the
    way it should behave.
    """

    content: str = field(default_factory=str)
    single_word: bool = False
    lstrip: bool = False
    rstrip: bool = False
    normalized: bool = True

    def __getstate__(self):
        return self.__dict__

@dataclass
class EncodingFast:
    """ This is dummy class because without the `tokenizers` library we don't have these objects anyway """

    pass



from .tokenizers import Tokenizer, Encoding
from .tokenizers import decoders
from .tokenizers import models
from .tokenizers import normalizers
from .tokenizers import pre_tokenizers
from .tokenizers import processors
from .tokenizers import trainers
from .implementations import (
    ByteLevelBPETokenizer,
    CharBPETokenizer,
    SentencePieceBPETokenizer,
    BertWordPieceTokenizer,
)
```

transformer, tokenizers, sentence\_transformers 디렉토리를 opt/conda\(가상환경 폴더\)/lib/python3.7/site-packages/ 로 이동합니다.

### Train Models

모델 학습을 원하시면 KoSentenceBERT 디렉토리 안에 KorNLUDatatesㅇ이 존재해야 합니다.    
리뷰 데이터 구조에 맞게 STS데이터를 직접 만들어 사용하였고 데이터예와 학습 방법은 아래와 같습니다.  

```text
뇨끼를 주문했었는데 쫄깃하고 크림 또한 느끼하지 않고 고소하고 맛있었어요.    한식 주문했었는데 쫄깃하고 크림 또한 느끼하지 않고 고소하고 맛있었어요.    1.0
뇨끼를 주문했었는데 쫄깃하고 크림 또한 느끼하지 않고 고소하고 맛있었어요.    파스타를 주문했었는데 쫄깃하고 크림 또한 느끼하지 않고 고소하고 맛있었어요.    4.8
느끼하지 않고 고소하고 맛있었어요.    느끼하지 않고 고소하고 맛없었어요.    0.6
느끼하지 않고 고소하고 맛있었어요.    느끼하지 않고 꼬소하고 맛있었어요.    5.0
느끼하지 않고 고소하고 맛있었어요.    느끼하지 않고 구수하고 맛있었어요.    4.8
```

```bash
python training_sts.py 
```

현재 음식점 리뷰데이터에 최적화된 상태로 학습된 모델은 다음 폴더에 pt파일로 저장되어 있습니다.    
/model/training\_stsbenchmark\_skt\_kobert\_model\_-2021-03-28\_05-25-43\_best/ 

