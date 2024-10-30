# gpt를 이용한 reminder 애플리케이션

## 소개

이 프로젝트는 gpt를 이용한 reminder 애플리케이션입니다.

## 주요 기능

- **사용자 인증**: 회원가입, 로그인, 로그아웃 기능
- **To-Do 관리**: To-Do 항목 추가, 수정, 삭제, 완료 토글
- **마감일 설정**: Flatpickr를 이용한 날짜 및 시간 선택, 빠른 선택 옵션(현재, 30분 뒤, 1시간 뒤) 제공
- **반응형 디자인**: 모바일 환경 최적화를 위한 UI 개선
- **정렬 기능**: 마감일 기준으로 To-Do 항목 내림차순 정렬

## 실행
  1. docker-compose.yml 파일에 환경 변수 입력
  2. $ docker-compose up -d
  
## 종료
  1. $ docker-compose down