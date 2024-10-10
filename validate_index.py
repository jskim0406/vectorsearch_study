import logging
from elasticsearch import Elasticsearch

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ESInfoLogger')

def create_elasticsearch_client() -> Elasticsearch:
    """
    Elasticsearch 클라이언트를 생성합니다.
    """
    return Elasticsearch(['http://elasticsearch:9200'])

def get_total_document_count(es: Elasticsearch, index_name: str) -> int:
    """
    주어진 인덱스의 전체 문서 수를 반환합니다.
    """
    try:
        count_result = es.count(index=index_name)
        total_docs = count_result['count']
        logger.info(f"인덱스 '{index_name}'의 전체 문서 수: {total_docs}")
        return total_docs
    except Exception as e:
        logger.error(f"문서 수를 가져오는 중 오류 발생: {str(e)}")
        return 0

def get_random_samples(es: Elasticsearch, index_name: str, sample_size: int = 5):
    """
    주어진 인덱스에서 랜덤하게 샘플 문서를 조회합니다.
    """
    query = {
        "size": sample_size,
        "query": {
            "function_score": {
                "functions": [
                    {
                        "random_score": {}
                    }
                ]
            }
        }
    }

    try:
        response = es.search(index=index_name, body=query)
        hits = response['hits']['hits']
        logger.info(f"인덱스 '{index_name}'에서 랜덤하게 {len(hits)}개의 문서를 조회했습니다.")
        for doc in hits:
            doc_id = doc['_id']
            source = doc['_source']
            logger.info(f"문서 ID: {doc_id}\n소스 데이터: {source}\n")
    except Exception as e:
        logger.error(f"랜덤 샘플을 가져오는 중 오류 발생: {str(e)}")

def main():
    es = create_elasticsearch_client()
    index_name = "abo_products_selected"

    # 전체 문서 수 가져오기
    total_docs = get_total_document_count(es, index_name)

    if total_docs > 0:
        # 랜덤 샘플 문서 조회
        get_random_samples(es, index_name, sample_size=3)
    else:
        logger.info("인덱스에 문서가 없습니다.")

if __name__ == "__main__":
    main()