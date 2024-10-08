import time

import openai

from utils.requirement_input_util import confirm, input_requirements, select_project_name


def get_response(prompt, max_tokens=1500):
    # OpenAI API로 응답을 가져오는 함수
    try:
        time.sleep(1)  # API 요청 간 딜레이 추가
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 프로젝트 요구사항 분석을 도와주는 AI입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return None


def derive_information(task:str, context:str, max_tokens: int=None, additional_requirements: str=None):
    # 반복되는 작업을 일반화한 함수 (목표, 주요 기능, 기술 스택, 프로젝트명 등 도출)
    while True:
        prompt = f"다음 {context}을(를) 바탕으로 {task}을(를) 도출해줘:\n\n{context}"
        if additional_requirements:
            prompt = f"{prompt}\n\n단 {additional_requirements}."
        result = get_response(prompt, max_tokens)
        if result:
            print(f"\n[{task} 도출]")
            print(result)
            if confirm(f"위의 {task}이(가) 맞습니까?"):
                return result
        print(f"{task} 도출에 실패했습니다. 추가 요구사항을 입력해주세요.")
        context += f"\n{input_requirements()}"


def recommend_name(requirements):
    while True:
        prompt = f"다음 요구사항을 반영하여 적합한 이름을 추천해줘:\n\n{requirements}\n\n단. 이름 - 이유\n이름 - 이유\n이름 - 이유... 의 형식으로 적어줘 나머지는 적지 말아줘."
        project_names = get_response(prompt, max_tokens=150)
        if not project_names:
            print("이름 추천에 실패했습니다. 다시 시도합니다.")
            continue
        print(project_names)
        if confirm("위의 이름이 마음에 드십니까?"):
            project_name = select_project_name(project_names)
            print(f"\n선택된 이름: {project_name}")
            return project_name
        else:
            print("추가 요구사항을 입력해주세요.")
            additional = input_requirements()
            requirements += f"\n{additional}"
