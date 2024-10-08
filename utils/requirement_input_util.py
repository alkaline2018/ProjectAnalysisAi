def confirm(prompt):
    # 사용자로부터 yes/no 응답을 받는 함수
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("유효한 응답이 아닙니다. 'yes', 'no'로 대답해주세요.")


def input_requirements():
    # 사용자로부터 입력을 받아 요구사항 리스트를 반환하는 함수
    print("요구사항을 입력하세요 (완료되면 Enter를 두 번 누르세요):")
    requirements = []
    while (line := input().strip()):
        requirements.append(line)
    return "\n".join(requirements)


def select_project_name(project_names):
    """
    프로젝트명을 여러 개 받을 때 사용자로부터 선택을 받는 함수
    """
    print("\n[프로젝트명 추천]")
    names = project_names.split("\n")

    # 프로젝트명 목록 표시
    for idx, name in enumerate(names, start=1):
        print(f"{idx}. {name}")

    while True:
        try:
            choice = int(input("원하는 프로젝트명 번호를 선택하세요: "))
            if 1 <= choice <= len(names):
                return names[choice - 1].strip()
            else:
                print("유효한 번호를 선택해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")


