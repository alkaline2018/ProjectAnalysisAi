import time

import openai
from pymongo import MongoClient, errors
import config
import sys

# OpenAI API 설정
openai.api_key = config.OPENAI_API_KEY

# MongoDB 클라이언트 설정
try:
    client = MongoClient(config.MONGODB_URI)
    db = client[config.DATABASE_NAME]
    collection = db[config.COLLECTION_NAME]
except errors.ConnectionFailure as e:
    print(f"MongoDB 연결 실패: {e}")
    sys.exit(1)

def get_response(prompt, max_tokens=1500):
    """
    OpenAI ChatGPT API를 사용하여 응답을 가져오는 함수
    """
    try:
        time.sleep(1)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 프로젝트 요구사항 분석을 도와주는 AI입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        print(response.choices[0].message)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return None

def confirm(prompt):
    """
    사용자로부터 'yes' 또는 'no' 응답을 받는 함수
    """
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("유효한 응답이 아닙니다. 'yes,y' 또는 'no,n'로 대답해주세요.")

def input_requirements():
    """
    사용자로부터 요구사항 입력 받기
    """
    print("프로젝트 요구사항을 입력하세요 (완료되면 Enter를 두 번 누르세요):")
    requirements = []
    while True:
        line = input()
        if line == '':
            break
        requirements.append(line.strip())
    return "\n".join(requirements)


def derive_project_goals(requirements):
    while True:
        prompt = f"다음 요구사항을 바탕으로 프로젝트의 한 줄 목표를 도출해줘:\n\n{requirements}"
        goals = get_response(prompt)
        if not goals:
            print("프로젝트 목표 도출에 실패했습니다. 다시 시도합니다.")
            continue
        print("\n[프로젝트 목표 도출]")
        print(goals)
        if confirm("위의 프로젝트 목표가 맞습니까?"):
            return goals
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            requirements += f"\n{additional}"

def derive_main_features(goals):
    while True:
        prompt = f"다음 프로젝트 목표를 바탕으로 주요 기능을 도출해줘:\n\n{goals}"
        features = get_response(prompt)
        if not features:
            print("프로젝트 주요 기능 도출에 실패했습니다. 다시 시도합니다.")
            continue
        print("\n[프로젝트 주요 기능 도출]")
        print(features)
        if confirm("위의 주요 기능이 맞습니까?"):
            return features
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            goals += f"\n{additional}"

def select_tech_stack(features):
    while True:
        prompt = f"다음 주요 기능을 바탕으로 프로젝트에 적합한 기술 스택을 선택해줘:\n\n{features}"
        tech_stack = get_response(prompt)
        if not tech_stack:
            print("프로젝트 주요 기술 스택 선택에 실패했습니다. 다시 시도합니다.")
            continue
        print("\n[프로젝트 주요 기술 스택 선택]")
        print(tech_stack)
        if confirm("위의 기술 스택이 맞습니까?"):
            return tech_stack
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            features += f"\n{additional}"

def recommend_project_name(requirements):
    while True:
        prompt = f"다음 요구사항을 반영하여 적합한 프로젝트명을 추천해줘:\n\n{requirements}"
        project_name = get_response(prompt, max_tokens=300)
        if not project_name:
            print("프로젝트명 추천에 실패했습니다. 다시 시도합니다.")
            continue
        print("\n[프로젝트명 추천]")
        print(project_name)
        if confirm("위의 프로젝트명이 마음에 드십니까?"):
            return project_name
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            requirements += f"\n{additional}"

def generate_documentation(requirements, goals, features, tech_stack, project_name):
    while True:
        prompt = (
            f"다음 정보를 바탕으로 프로젝트 문서를 작성해줘.\n\n"
            f"프로젝트명: {project_name}\n"
            f"요구사항: {requirements}\n"
            f"프로젝트 목표: {goals}\n"
            f"주요 기능: {features}\n"
            f"기술 스택: {tech_stack}\n"
        )
        documentation = get_response(prompt, max_tokens=2000)
        if not documentation:
            print("문서화 도출에 실패했습니다. 다시 시도합니다.")
            continue
        print("\n[문서화 도출]")
        print(documentation)
        if confirm("위의 문서가 맞습니까?"):
            return documentation
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            requirements += f"\n{additional}"

def store_in_db(project_data):
    try:
        collection.insert_one(project_data)
        print("\n[DB화] 데이터가 성공적으로 MongoDB에 저장되었습니다.")
    except errors.PyMongoError as e:
        print(f"MongoDB 저장 오류: {e}")

def main():
    print("=== 프로젝트 요구사항 분석 AI ===\n")

    # 1. 요구사항 입력
    requirements = input_requirements()

    # 2. 프로젝트 목표 도출
    goals = derive_project_goals(requirements)

    # 3. 프로젝트 주요 기능 도출
    features = derive_main_features(goals)

    # 4. 프로젝트 주요 기술 스택 선택
    tech_stack = select_tech_stack(features)

    # 5. 프로젝트명 추천
    project_name = recommend_project_name(requirements)

    # 6. 문서화 도출
    documentation = generate_documentation(requirements, goals, features, tech_stack, project_name)

    # 7. DB화
    project_data = {
        "project_name": project_name,
        "requirements": requirements,
        "goals": goals,
        "features": features,
        "tech_stack": tech_stack,
        "documentation": documentation
    }
    store_in_db(project_data)

    print("\n=== 프로젝트 분석이 완료되었습니다! ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")