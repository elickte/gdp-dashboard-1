# streamlit 라이브러리를 불러옵니다. 'st'라는 별칭으로 사용할게요.
import streamlit as st
import random  # 무작위 선택을 위해 random 라이브러리를 불러옵니다.
import time    # 시간 지연(잠깐 기다리기) 기능을 위해 time 라이브러리를 불러옵니다.

# --- 앱 초기 설정 ---
# 앱의 제목을 설정합니다.
st.title("🧠 순발력 동체시력 게임")

# 게임에 사용할 아이콘 목록입니다.
DIRECTIONS = ["⬆️", "⬇️", "⬅️", "➡️"]

# --- 세션 상태(Session State) 초기화 ---
# 세션 상태는 사용자가 앱과 상호작용하는 동안 변수를 저장하는 공간입니다.
# 웹 페이지가 새로고침 되어도 값이 유지되어 게임 상태를 기억할 수 있습니다.

# 'level'이 아직 세션 상태에 없으면, 초기값 1로 설정합니다. (게임 레벨)
if 'level' not in st.session_state:
    st.session_state.level = 1

# 'display_time'이 없으면, 초기값 1.0초로 설정합니다. (아이콘 보여주는 시간)
if 'display_time' not in st.session_state:
    st.session_state.display_time = 1.0

# 'sequence'가 없으면, 빈 리스트로 설정합니다. (정답 아이콘 순서)
if 'sequence' not in st.session_state:
    st.session_state.sequence = []

# 'user_input'이 없으면, 빈 리스트로 설정합니다. (사용자 입력 순서)
if 'user_input' not in st.session_state:
    st.session_state.user_input = []

# 'show_sequence'가 없으면, False로 설정합니다. (아이콘을 보여줄지 말지 결정)
if 'show_sequence' not in st.session_state:
    st.session_state.show_sequence = False

# 'game_over'가 없으면, False로 설정합니다. (게임이 끝났는지 확인)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- 함수 정의 ---

def start_new_round():
    """새로운 라운드를 시작하는 함수"""
    # 현재 레벨에 맞춰 정답 순서를 생성합니다. (레벨만큼 아이콘 개수 증가)
    st.session_state.sequence = random.choices(DIRECTIONS, k=st.session_state.level)
    # 사용자 입력을 초기화합니다.
    st.session_state.user_input = []
    # 아이콘을 보여줘야 한다는 신호를 True로 바꿉니다.
    st.session_state.show_sequence = True
    # 게임 종료 상태를 False로 되돌립니다.
    st.session_state.game_over = False

def check_answer():
    """사용자 입력과 정답을 비교하는 함수"""
    if st.session_state.user_input == st.session_state.sequence:
        # 정답일 경우
        st.success(f"성공! 레벨 {st.session_state.level} 클리어!")
        # 레벨을 1 올립니다.
        st.session_state.level += 1
        # 아이콘 보여주는 시간을 10%씩 줄여서 더 어렵게 만듭니다. (최소 0.1초)
        st.session_state.display_time = max(0.1, st.session_state.display_time * 0.9)
        # 다음 라운드를 준비합니다.
        start_new_round()
    else:
        # 오답일 경우
        st.error("실패! 처음부터 다시 시작하세요.")
        # 게임 상태를 모두 초기값으로 되돌립니다.
        st.session_state.level = 1
        st.session_state.display_time = 1.0
        # 게임을 다시 시작할 수 있도록 시작 버튼을 누르도록 유도합니다.
        st.session_state.show_sequence = False
        st.session_state.game_over = True # 게임이 끝났음을 표시

# --- 게임 화면 구성 ---

# 게임 시작 버튼
# st.button을 if문과 함께 사용하면, 버튼이 클릭되었을 때 True가 되어 안의 코드가 실행됩니다.
if st.button("게임 시작!"):
    start_new_round()

# 'show_sequence'가 True일 때 (아이콘을 보여줘야 할 때)
if st.session_state.show_sequence:
    # 현재 레벨과 아이콘 표시 시간을 안내합니다.
    st.info(f"레벨: {st.session_state.level} | 표시 시간: {st.session_state.display_time:.2f}초")

    # 아이콘을 표시할 공간을 미리 만듭니다.
    sequence_placeholder = st.empty()
    # 생성된 정답 순서를 공백으로 구분하여 하나의 문자열로 만들어 표시합니다.
    sequence_placeholder.markdown(f"<h1 style='text-align: center;'>{' '.join(st.session_state.sequence)}</h1>", unsafe_allow_html=True)
    
    # 설정된 'display_time' 만큼 프로그램을 잠시 멈춥니다.
    time.sleep(st.session_state.display_time)
    
    # 아이콘을 표시했던 공간을 비웁니다.
    sequence_placeholder.empty()
    # 아이콘을 다 보여줬으므로, 'show_sequence'를 False로 바꿔 다시 보이지 않게 합니다.
    st.session_state.show_sequence = False
    # Streamlit에게 화면을 새로고침하라고 명령하여 아이콘이 즉시 사라지게 합니다.
    st.rerun()

# 게임이 시작되었고, 아이콘을 보여주는 시간이 아닐 때
# len(st.session_state.sequence) > 0: 게임이 시작되었다는 의미
if len(st.session_state.sequence) > 0 and not st.session_state.show_sequence and not st.session_state.game_over:
    st.write("---")
    st.write("방금 본 아이콘의 순서대로 버튼을 누르세요!")

    # 4개의 컬럼을 만들어 버튼을 가로로 나란히 배치합니다.
    cols = st.columns(4)
    if cols[0].button("⬆️", use_container_width=True):
        st.session_state.user_input.append("⬆️")
    if cols[1].button("⬇️", use_container_width=True):
        st.session_state.user_input.append("⬇️")
    if cols[2].button("⬅️", use_container_width=True):
        st.session_state.user_input.append("⬅️")
    if cols[3].button("➡️", use_container_width=True):
        st.session_state.user_input.append("➡️")

    # 사용자가 현재까지 입력한 순서를 보여줍니다.
    st.write("나의 입력:", " ".join(st.session_state.user_input))
    
    st.write("---")

    # 제출 버튼
    if st.button("제출", type="primary"):
        check_answer()

# 최종 결과 메시지 (실패했을 때)
if st.session_state.game_over:
    st.warning("👾 이런! 날라오는 사과에 맞았습니다. 👾")
    st.info("""
    **학습 유형 설명:**
    순발력과 동체시력은 반복 훈련으로 향상될 수 있습니다. 
    이 게임은 빠르게 나타나는 시각 정보를 기억하고 순서대로 반응하는 훈련을 통해, 
    **'운동 지능'**과 관련된 정보 처리 속도를 높이는 데 도움을 줍니다. 
    다시 도전해서 사과를 막아보세요!
    """)