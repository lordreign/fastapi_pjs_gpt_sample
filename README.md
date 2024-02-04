# FASTAPI PJS GPT SAMPLE
> FASTAPI와 OPENAI API를 활용한 Sample 프로젝트 입니다.<br>
> ORM은 SQLAlchemy를 사용합니다.<br>
> 파이썬 버전은 3.10.12 기준 입니다.

## pyenv와 pyenv-virtualenv 설치 및 적용
### 설치(mac 기준)
```
$ brew install pyenv
$ brew install pyenv-virtualenv
```

### 환경변수 설정(mac 기준)
```
# ~/.zshrc에 추가
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### 적용(mac 기준)
```
$ source ~/.zshrc
```

## python 설치 및 프로젝트 환경 설정
### python 설치
```
$ pyenv install 3.10.12
```

### python 설치 확인
```
$ pyenv versions
```

### 프로젝트 환경 설정
```
$ pyenv virtualenv 3.10.12 3.10.12_gpt_api_boiler
$ pyenv local 3.10.12_gpt_api_boiler
```
### vscode 인터프리터 선택
1. cmd + shift + p(ctrl + shift + p) 키 입력
2. Python: 인터프리터 선택
3. 3.10.12_gpt_api_boiler 선택

## .env 설정
1. project root에 .env 파일 생성
2. .env_sample을 확인하여 .env파일에 키에 맞는 값 설정

## dependency 설치 및 실행
### dependency 설치
```
$ pip install -r requirements.txt
```

### 실행
```
$ ./run.sh
```

## 사용하는 주요 라이브러리
* [openai](https://platform.openai.com/docs/introduction/overview)
* [fastapi](https://fastapi.tiangolo.com/ko/)
* [sqlalchemy](https://www.sqlalchemy.org/)