import openai
import config

from utils.mongo_util import initialize_mongo, store_in_db
from utils.requirement_input_util import input_requirements
from utils.openai_util import derive_information, recommend_name


# 메인 프로세스
def main():
    openai.api_key = config.OPENAI_API_KEY

    collection = initialize_mongo()

    print("=== 프로젝트 요구사항 분석 AI ===\n")
    requirements = input_requirements()

    goals = derive_information("프로젝트 목표", requirements, max_tokens=300, additional_requirements="최대 3줄로 정리해줘")
    features = derive_information("주요 기능", goals)
    tech_stack = derive_information("필요한 기술", features)
    project_name = recommend_name(requirements)

    # 문서화 생성
    documentation = derive_information("프로젝트 문서", f"프로젝트명: {project_name}\n요구사항: {requirements}\n목표: {goals}\n기능: {features}\n기술 스택: {tech_stack}", max_tokens=3000)

    # 프로젝트 데이터 생성 및 DB 저장
    project_data = {
        "project_name": project_name,
        "requirements": requirements,
        "goals": goals,
        "features": features,
        "tech_stack": tech_stack,
        "documentation": documentation
    }
    store_in_db(collection, project_data)

    print("\n=== 프로젝트 분석이 완료되었습니다! ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
