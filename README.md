# VECTOR_SEARCH 과제

## 1차 제출
### 2024.10.11(금)
#### 현재까지 진행 상황
- (완료) elasticsearch index `abo_products_selected` 생성
  - `### 1. 프로젝트 세팅 및 기본 환경 구축`
  - `### 2. 데이터셋 이해 및 전처리 계획 수립`
  - `### 3. Elasticsearch 인덱스 설계, 매핑 정의, 인덱싱`

- (진행 중) 
  - `### 4. 배치 인덱스 파이프라인 구축`
  - `### 5. Kafka를 활용한 업데이트 파이프라인 설계 및 테스트`

#### 인덱싱 결과
- 총 인덱싱 문서 수: 20,600개
- 인덱싱 Rule
  1. indexing 대상 field: 총 11개로 선별(제품 검색에 유용할 것으로 판단되는 field를 선택)
  2. `en_US` 필터링: `product_description`, `item_keywords` 모두 `language_tag`가 `en_US`인 경우만 인덱싱
  3. nested 구조의 document는 'value'값만 추출해 document로 indexing
    - 예
      - `"brand": "[{'language_tag': 'en_US', 'value': 'Signature Design by Ashley'}]"`
        - `"brand": "Signature Design by Ashley"`로 document를 구성해 indexing 수행

#### 참고 사항
##### indexing 대상 field 11개
```python
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
```

##### indexing 문서 수, sample 문서 조회(3개)
```bash
root@0527e810dbbe:/usr/src/app# python validate_index.py 

INFO:elastic_transport.transport:POST http://elasticsearch:9200/abo_products_selected/_count [status:200 duration:0.004s]
INFO:ESInfoLogger:인덱스 'abo_products_selected'의 전체 문서 수: 20600
INFO:elastic_transport.transport:POST http://elasticsearch:9200/abo_products_selected/_search [status:200 duration:0.004s]
INFO:ESInfoLogger:인덱스 'abo_products_selected'에서 랜덤하게 3개의 문서를 조회했습니다.
INFO:ESInfoLogger:문서 ID: B07ZS8DXZL
소스 데이터: {'brand': '365 by Whole Foods Market', 'bullet_point': 'Brought to you by Whole Foods Market.\xa0 The packaging for this product has a fresh new look. During this transition, you may get the original packaging or the new packaging in your order, but the product and quality is staying exactly the same. Enjoy!', 'color': None, 'fabric_type': None, 'item_id': 'B07ZS8DXZL', 'item_keywords': 'Essentials Baby Products Baby Food Baby Products Feeding Baby Foods', 'item_name': '365 by Whole Foods Market, Organic Baby Food, Apricot Banana Spinach Yogurt with Ground Chia, 4 Ounce', 'material': None, 'product_description': None, 'product_type': 'GROCERY', 'style': None}

INFO:ESInfoLogger:문서 ID: B074WS74CX
소스 데이터: {'brand': 'AmazonBasics', 'bullet_point': '0.5-cubic-foot security safe with electronic lock and 2 emergency override keys', 'color': None, 'fabric_type': None, 'item_id': 'B074WS74CX', 'item_keywords': 'fire', 'item_name': 'AmazonBasics Steel, Security Safe Lock Box, Black - 0.5-Cubic Feet & AA Performance Alkaline Batteries - Pack of 20', 'material': 'Alloy Steel', 'product_description': None, 'product_type': 'SAFE', 'style': 'Safe + Batteries Bundle'}

INFO:ESInfoLogger:문서 ID: B074H5LYFZ
소스 데이터: {'brand': 'Engine 2', 'bullet_point': 'Brought to you by Whole Foods Market.', 'color': None, 'fabric_type': None, 'item_id': 'B074H5LYFZ', 'item_keywords': 'Grocery Frozen Plant Based Protein Burgers Grocery & Gourmet Food Meat Substitutes Burgers & Patties Meatless Burgers', 'item_name': 'Engine 2, Plant Burgers Tuscan Kale White Bean, 8 Ounce', 'material': None, 'product_description': None, 'product_type': 'GROCERY', 'style': None}
```

---

## Plan
프로젝트를 시작하기 위해 우선순위에 따라 설정한 진행 단계는 아래와 같습니다.

### 1. **프로젝트 세팅 및 기본 환경 구축**
   - **로컬 개발 환경 설정**: 프로젝트를 로컬에서 진행할 수 있도록 개발 환경을 구축합니다.
     - Java (Kafka, Spark를 위해 필요)
     - Python (데이터 전처리, Spark 작업, Elasticsearch 연동 등)
     - Docker (Kafka, Elasticsearch를 컨테이너로 배포할 경우)
   - **기술 스택 설치**: 
     - **Apache Kafka**, **Apache Spark**, **Elasticsearch** 설치 및 설정
     - Docker Compose 파일을 작성해 각 서비스를 로컬에서 손쉽게 실행할 수 있도록 준비합니다.
     - 각 서비스가 제대로 동작하는지 간단한 예제로 확인합니다.

### 2. **데이터셋 이해 및 전처리 계획 수립**
   - **ABO 데이터셋 다운로드 및 탐색**:
     - `abo-listings.tar` 파일을 다운로드하고 데이터를 탐색하여 어떤 필드가 있는지 확인합니다.
     - 주요 필드(`item_keywords`, `product_description` 등)를 파악하고, Elasticsearch 인덱싱에 필요한 스키마를 정의합니다.
   - **전처리 계획 수립**:
     - 데이터를 어떻게 전처리할 것인지 정의합니다. 예를 들어, 불필요한 데이터를 제거하거나, 텍스트 데이터를 정제하고, 필요한 포맷으로 변환합니다.
     - 전처리 단계에서 Spark의 기능을 활용할 수 있는 방법을 고민합니다.

### 3. **Elasticsearch 인덱스 설계, 매핑 정의, 인덱싱**
   - **Elasticsearch 인덱스 매핑**:
     - `item_keywords`와 `product_description` 필드를 포함하여 인덱스 구조를 설계합니다.
     - 텍스트 필드의 분석기(예: 표준 분석기, 커스텀 분석기) 설정을 고려합니다.
     - 데이터의 검색 최적화를 위해 필드 타입과 매핑을 설계합니다.
   - **테스트 데이터 인덱싱**:
     - 데이터를 몇 개 추출하여 Elasticsearch에 수동으로 인덱싱하고, 제대로 인덱싱되는지 확인합니다.
     - 샘플 검색 쿼리를 실행해 기대한 결과가 나오는지 확인합니다.

### 4. **배치 인덱스 파이프라인 구축**
   - **Spark 기반 데이터 처리 스크립트 작성**:
     - Spark를 사용해 `abo-listings` 데이터를 전처리하고 Elasticsearch로 인덱싱하는 코드를 작성합니다.
     - 각 단계별로 데이터가 어떻게 변형되는지 로그를 남겨 디버깅과 테스트를 용이하게 합니다.
   - **Elasticsearch와의 연동 테스트**:
     - Spark에서 처리된 데이터를 Elasticsearch에 보내고, 인덱싱이 제대로 되는지 확인합니다.
     - 초기 배치 데이터를 인덱싱한 후 Elasticsearch에서 샘플 쿼리를 실행하여 결과를 확인합니다.

### 5. **Kafka를 활용한 업데이트 파이프라인 설계 및 테스트**
   - **Kafka 설정 및 토픽 정의**:
     - `item_keywords`와 `product_description` 업데이트를 처리할 Kafka 토픽을 정의합니다.
     - Kafka의 Producer를 통해 샘플 업데이트 메시지를 토픽에 전송하고, Consumer로 메시지를 확인해 테스트합니다.
   - **Spark/Flink를 사용한 업데이트 처리**:
     - Spark 또는 Flink 스트리밍 작업을 통해 Kafka의 메시지를 읽고, 이를 Elasticsearch에 업데이트하는 스크립트를 작성합니다.
     - 작은 테스트 데이터를 사용해 실시간 업데이트가 Elasticsearch에 반영되는지 검증합니다.

### **예상되는 초기 순서 요약**
1. 로컬 개발 환경 및 도구 설치 (Kafka, Spark, Elasticsearch)
2. 데이터셋 다운로드 및 탐색
3. Elasticsearch 인덱스 구조 설계, 인덱싱
4. Spark 기반 배치 인덱싱 파이프라인 구축 및 테스트
5. Kafka 기반 실시간 업데이트 파이프라인 구축 및 테스트

---

## ENV

---

## 1. 환경 준비
### 1.1 Docker 설치 확인

Ubuntu에 Docker가 이미 설치되어 있는지 확인합니다.

```bash
docker --version
```
Docker가 설치되어 있지 않다면, [Docker 공식 문서](https://docs.docker.com/engine/install/ubuntu/)를 참고하여 설치하세요.

---

## 2. Elasticsearch 및 Kibana 설정

### 2.1 Elasticsearch 및 Kibana 이미지 다운로드

```bash
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:8.15.0
sudo docker pull docker.elastic.co/kibana/kibana:8.15.0
```

### 2.2 Docker 네트워크 생성

Elasticsearch와 Kibana가 통신할 수 있도록 Docker 네트워크를 생성합니다.

```bash
sudo docker network create elastic
```

### 2.3 Elasticsearch 컨테이너 실행

```bash
sudo docker run -d \
  --name elasticsearch \
  --net elastic \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ELASTIC_PASSWORD=password" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.enrollment.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.0
```

### 2.4 Kibana 컨테이너 실행

```bash
sudo docker run -d \
  --name kibana \
  --net elastic \
  -p 5601:5601 \
  docker.elastic.co/kibana/kibana:8.15.0
```

### 2.5 Kibana 접속 확인

웹 브라우저에서 [http://localhost:5601](http://localhost:5601)에 접속하여 Kibana가 정상적으로 실행되는지 확인합니다.

- **로그인 정보**:
  - 아이디: `elastic`
  - 비밀번호: `password`

---

## 3. Java 설치 및 환경 변수 설정

### 3.1 OpenJDK 17 설치

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
```

### 3.2 JAVA_HOME 환경 변수 설정

`~/.bashrc` 파일을 편집하여 환경 변수를 설정합니다.

```bash
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 3.3 Java 설치 확인

```bash
java -version
echo $JAVA_HOME
```

---

## 4. Spark 설치 및 설정

### 4.1 Spark 다운로드

```bash
curl -O https://dlcdn.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz
```

### 4.2 Spark 압축 해제 및 이동

```bash
tar -xzf spark-3.4.3-bin-hadoop3.tgz
sudo mv spark-3.4.3-bin-hadoop3 /opt/spark-3.4.3
```

### 4.3 Spark 설정 파일 복사 및 수정

```bash
sudo cp /opt/spark-3.4.3/conf/spark-defaults.conf.template /opt/spark-3.4.3/conf/spark-defaults.conf
echo 'spark.driver.extraJavaOptions   -Djava.security.manager=allow' | sudo tee -a /opt/spark-3.4.3/conf/spark-defaults.conf
echo 'spark.executor.extraJavaOptions   -Djava.security.manager=allow' | sudo tee -a /opt/spark-3.4.3/conf/spark-defaults.conf
```

### 4.4 심볼릭 링크 생성

```bash
sudo ln -s /opt/spark-3.4.3 /opt/spark
```

### 4.5 SPARK_HOME 환경 변수 설정

`~/.bashrc` 파일에 다음을 추가합니다.

```bash
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 4.6 Spark 설치 확인

```bash
spark-shell --version
```

---

## 5. Spark와 Elasticsearch 연동

### 5.1 Elasticsearch Spark 커넥터 JAR 파일 다운로드

```bash
curl -L -o elasticsearch-spark-30_2.12-8.15.0.jar \
"https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-30_2.12/8.15.0/elasticsearch-spark-30_2.12-8.15.0.jar"
```

### 5.2 JAR 파일을 Spark의 JAR 디렉토리로 이동

```bash
sudo mv elasticsearch-spark-30_2.12-8.15.0.jar /opt/spark-3.4.3/jars/
```

---

## 6. Kafka 설정

### 6.1 Docker Compose 파일 작성

프로젝트 디렉토리에 `docker-compose.yml` 파일을 생성하고 다음 내용을 추가합니다.

```yaml
version: '3.8'

services:
  zookeeper:
    image: bitnami/zookeeper:latest
    container_name: zookeeper
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes  # 익명 로그인을 허용하여 Zookeeper가 시작되도록 설정
    ports:
      - "2181:2181"
    networks:
      - kafka-net

  kafka:
    image: bitnami/kafka:latest
    container_name: kafka
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_LISTENERS=PLAINTEXT://:9092
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper
    networks:
      - kafka-net

  python-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: python-app
    volumes:
      - /home/js.kim/search:/usr/src/app
    ports:
      - "8000:8000"  # 예: 웹 서버를 위한 포트 매핑
      - "8888:8888"  # 예: Jupyter Notebook을 위한 포트 매핑
    networks:
      - elastic
      - kafka-net
    depends_on:
      - kafka
      - zookeeper

networks:
  kafka-net:
    driver: bridge
  elastic:
    external: true  # 이미 존재하는 elastic 네트워크를 사용
```

### 6.2 Kafka 및 Zookeeper 실행

```bash
docker-compose up -d
```

### 6.3 Kafka 동작 확인

Kafka CLI 도구를 사용하여 토픽을 생성하고 메시지를 주고받을 수 있습니다.

---

## 7. Jupyter Notebook 설치 및 설정 (선택 사항)

### 7.1 Python 3.9 설치

```bash
sudo apt update
sudo apt install -y python3.9 python3.9-venv python3.9-dev
```

### 7.2 pip 및 Jupyter Notebook 설치

```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.9
sudo python3.9 -m pip install jupyter ipykernel
```

### 7.3 Python 3.9 커널 추가

```bash
python3.9 -m ipykernel install --user --name="Python-3.9"
```

### 7.4 Jupyter Notebook에서 Spark 연동 환경 변수 설정

`~/.bashrc` 파일에 다음을 추가합니다.

```bash
echo 'export PYSPARK_PYTHON=python3.9' >> ~/.bashrc
echo 'export PYSPARK_DRIVER_PYTHON=jupyter' >> ~/.bashrc
echo 'export PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=8889"' >> ~/.bashrc
source ~/.bashrc
```

### 7.5 Jupyter Notebook 실행

```bash
pyspark
```

- 터미널에 표시되는 URL을 복사하여 웹 브라우저에서 Jupyter Notebook에 접속합니다.
- Spark 세션이 자동으로 생성되며, Spark와의 연동이 가능합니다.

---

## RUN
### docker container Up
- 만약 build가 안돼있던 상태라면,
  ```bash
  sudo docker-compose up -d --build
  ```
- 만약 특정 app만 하려면(예: `python-app`)
  ```bash
  sudo docker-compose up -d python-app
  ```
### docker container `python-app` run
```bash
docker run -it \
  -v /home/js.kim/search:/usr/src/app \
  -p 8000:8000 \  # 웹 서버를 위한 포트 매핑
  -p 8888:8888 \  # Jupyter Notebook을 위한 포트 매핑
  --network elastic \
  search-python-app /bin/bash

# RUN
sudo docker run -it -v /home/js.kim/search:/usr/src/app -p 8000:8000 -p 8888:8888 --network elastic search-python-app /bin/bash

# 접속
sudo docker exec -it "CONTAINER ID" /bin/bash
```

### docker container 간 network 추가 연결
앞서 docker network는 `elastic`뿐만 아니라 `kafka-net`도 설정했었습니다.
컨테이너가 실행된 후, `kafka-net` 네트워크에도 연결하려면 다음 명령어를 실행합니다:
```bash
sudo docker network connect kafka-net python-app
```