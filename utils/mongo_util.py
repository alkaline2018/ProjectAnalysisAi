import sys

from pymongo import MongoClient, errors

import config


# MongoDB 설정을 초기화하는 함수
def initialize_mongo():
    try:
        client = MongoClient(config.MONGODB_URI)
        db = client[config.DATABASE_NAME]
        collection = db[config.COLLECTION_NAME]
        return collection
    except errors.ConnectionFailure as e:
        print(f"MongoDB 연결 실패: {e}")
        sys.exit(1)


def store_in_db(collection, project_data):
    # 프로젝트 데이터를 DB에 저장하는 함수
    try:
        collection.insert_one(project_data)
        print("\n[DB 저장] 데이터가 성공적으로 저장되었습니다.")
    except errors.PyMongoError as e:
        print(f"MongoDB 저장 오류: {e}")
