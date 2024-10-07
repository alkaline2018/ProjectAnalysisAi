import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'project_analysis_db')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'projects')

# 환경 변수 유효성 검사
missing_vars = []
if not OPENAI_API_KEY:
    missing_vars.append('OPENAI_API_KEY')
if not MONGODB_URI:
    missing_vars.append('MONGODB_URI')

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")