# westagram
인스타그램 주요 기능 간단 구현 프로젝트
- 인원 : 1명
- 기간 : 2021년 1월 28일 ~ 2월 12일

<br>
<br>

## 기술 스택
- python 3
- Django
- MySQL

<br>

## 구현 기능
### User
- 회원가입 시 validation 진행
- bcrypt를 통해 비밀번호 암호화 하여 회원가입 진행
- 로그인 후 JWT로 토큰을 발행
- 유저간 팔로우 기능 구현 (하나의 로직으로 팔로우, 언팔로우 진행)

### Posting
- DB에 저장된 모든 posting 목록 반환 구현
- 하나의 posting : 전체 내용 수정(PUT), 일부 내용 수정(PATCH), 게시물 삭제(DELETE) 기능 구현 / 로그인 유저만 가능하도록 validation 진행
- 게시물 작성 로직 구현 (이미지 업로드는 X)
- 게시물에 댓글, 대댓글 작성, 수정, 삭제 로직 구현
- "좋아요" 표시된 게시물 목록 반환 구현
- 특정 게시물의 "좋아요" 갯수 반환 구현
