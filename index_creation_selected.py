import os
import json
import ast
import logging
import pandas as pd
from mappings import MAPPING_SHCEMA_selected, MAPPING_SHCEMA
from typing import List, Dict, Any
from elasticsearch import Elasticsearch, exceptions as es_exceptions
from elasticsearch.helpers import bulk
from pydantic import BaseModel, Field

# 로그 설정
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'index_creation.log')

# BasicConfig를 활용한 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('IndexCreationLogger')

class ESDocument(BaseModel):
    brand: str = None
    bullet_point: str = None
    color: str = None
    fabric_type: str = None
    item_id: str = None
    item_keywords: str = None
    item_name: str = None
    material: str = None
    product_description: str = None
    product_type: str = None
    style: str = None

def create_elasticsearch_client() -> Elasticsearch:
    """
    Elasticsearch 클라이언트를 생성합니다.
    """
    return Elasticsearch(['http://elasticsearch:9200'])

def create_index_mapping(es: Elasticsearch, index_name: str, csv_file:str) -> None:
    """
    기존 인덱스를 확인하고 필요시 삭제한 후, 새로운 인덱스와 매핑을 생성합니다.
    """
    try:
        # 기존 인덱스 확인 및 삭제
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            logger.info(f"기존 인덱스 '{index_name}'가 삭제되었습니다.")

        # 매핑 설정
        mapping = MAPPING_SHCEMA_selected

        # CSV 파일에서 컬럼 정보 읽기
        df = pd.read_csv(csv_file, nrows=1)
        columns = df.columns.tolist()

        # 새 인덱스 생성
        es.indices.create(index=index_name, body=mapping)
        logger.info(f"새 인덱스 '{index_name}'가 생성되었습니다.")

    except es_exceptions.AuthorizationException:
        logger.error(f"인덱스 '{index_name}' 생성 권한이 없습니다.")
    except es_exceptions.ConnectionError:
        logger.error("Elasticsearch에 연결할 수 없습니다.")
    except Exception as e:
        logger.error(f"인덱스 '{index_name}' 생성 중 오류 발생: {str(e)}")

def parse_json_string(value):
    if isinstance(value, str):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(value)
            except:
                return value
    return value

def preprocess_document(doc):
    processed_doc = {}
    for key, value in doc.items():
        if key in ['brand', 'bullet_point', 'color', 'fabric_type', 'item_keywords', 
                   'item_name', 'material', 'product_description', 'style']:
            parsed_value = parse_json_string(value)
            if isinstance(parsed_value, list):
                # 'en_US' 언어 태그를 가진 값을 찾습니다.
                en_us_value = None
                for item in parsed_value:
                    if item.get('language_tag') == 'en_US':
                        en_us_value = item['value']
                        break
                processed_doc[key] = en_us_value
            elif isinstance(parsed_value, dict) and parsed_value.get('language_tag') == 'en_US':
                processed_doc[key] = parsed_value['value']
            else:
                processed_doc[key] = None
        elif key == 'product_type':
            parsed_value = parse_json_string(value)
            if isinstance(parsed_value, list) and len(parsed_value) > 0 and 'value' in parsed_value[0]:
                processed_doc[key] = parsed_value[0]['value']
            else:
                processed_doc[key] = value
        else:
            processed_doc[key] = value

    # 'product_description'과 'item_keywords' 둘 다 None이면(language_tag가 'en_US'인 element가 없는 경우) 문서를 인덱싱하지 않습니다.
    if processed_doc.get('product_description') is None and processed_doc.get('item_keywords') is None:
        return None

    try:
        return ESDocument(**processed_doc).dict()
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        return None

def index_all_data(es: Elasticsearch, index_name: str, csv_file: str) -> None:
    """
    모든 데이터를 Elasticsearch에 인덱싱합니다. 이미 존재하는 문서는 업데이트합니다.
    'en_US' 언어 태그를 가진 데이터만 Elasticsearch에 인덱싱합니다.
    """
    df = pd.read_csv(csv_file)
    df = df[MAPPING_SHCEMA_selected["mappings"]["properties"].keys()]

    def _doc_generator(df):
        for index, row in df.iterrows():
            doc = preprocess_document(row.to_dict())
            if doc:
                yield {
                    "_op_type": "update",
                    "_index": index_name,
                    "_id": doc['item_id'],
                    "doc": doc,
                    "doc_as_upsert": True
                }

    actions = list(_doc_generator(df))  # generator를 리스트로 변환
    # breakpoint()  # 디버깅 필요 시 활성화
    success, errors = bulk(es, actions, stats_only=False, raise_on_error=False)
    
    logger.info(f"{success}개의 문서가 성공적으로 처리되었습니다.")
    if errors:
        logger.error(f"{len(errors)}개의 문서 처리에 실패했습니다.")

def main():
    es = create_elasticsearch_client()
    index_name = "abo_products_selected"
    csv_file = "abo-listings/preprocessed_abo_listings.csv"
    
    try:
        # 인덱스 생성 및 매핑 정의
        create_index_mapping(es, index_name, csv_file)
        
        # 모든 데이터 인덱싱
        index_all_data(es, index_name, csv_file) # 20667개 인덱싱 완료
        
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main()