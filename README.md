# SummSaem - 동해 BE

## 환경 세팅
1. Python 3.10.13 설치 (pyenv 활용)
    ```bash
    # 사전에 필요한 라이브러리 설치
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

    # pyenv 설치
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    # 환경 변수 세팅
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc

    # 파이썬 3.10.13 설치
    pyenv install 3.10.13

    # 파이썬 3.10.13 설정
    pyenv global 3.10.13

    # 버전 확인
    python --version  # Python 3.10.13
    pip --version     # pip 23.0.1 .. (python 3.10)
    ```
2. 프로젝트 및 필수 라이브러리 설치
    ```bash
    # 프로젝트 깃 클론
    git clone https://github.com/10EastSea/summsaem.git
    
    # FastAPI 및 dependency 라이브러리 설치
    pip install -r requirements.txt
    ```
3. `.env` 파일 생성
    ```bash
    vim app/.env

    # openai api key 값 추가
    OPENAI_API_KEY='{openai_api_key}'
    ```
4. 실행
    ```bash
    uvicorn app.main:app --reload

    # 아래 처럼 host 및 port 옵션을 줘서 실행 가능
    # uvicorn app.main:app --reload --host=0.0.0.0 --port=80
    ```

<details>
<summary>참고: Environment</summary>

### Language
- Python 3.10.13

### Library
- fastapi 0.104.0
- uvicorn[standard] 0.24.0
- requests 2.31.0
- openai 1.3.8
- python-dotenv 1.0.0

### `.env`
```bash
vim app/.env

OPENAI_API_KEY='{openai_api_key}'
# NCP_APIGW_API_KEY_ID='{client_id}'  # fadeout
# NCP_APIGW_API_KEY='{client_secret}' # fadeout
```

## Run
```bash
uvicorn app.main:app --reload
```

</details>
