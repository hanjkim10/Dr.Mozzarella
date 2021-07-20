## 프로젝트명: Dr.Mozzarella🧀

- Dr.jart+ 클론 프로젝트
- Account, Product category & detail, Cart 구현
- 초기 세팅부터 모델링과 프론트로 보내주는 모든 제품 data를 실제 사용할 수 있는 서비스 수준으로 개발

 ### 개발 인원 및 기간
 개발기간 : 2021/7/5 ~ 2021/7/16
 개발 인원 : 프론트엔드 3명, 백엔드 3명
 https://github.com/wecode-bootcamp-korea/22-1st-DrMozzarella-frontend
 https://github.com/wecode-bootcamp-korea/22-1st-DrMozzarella-backend

 ### 프론트
 박정훈, 황소미, 이종민

 ### 백엔드
 이동명, 김한준, 안희수

 ### API 문서
 - https://documenter.getpostman.com/view/12180757/Tzm3nciR

 ### 기술스텍
 - python
 - django
 - MySQL
 - RESTful API
 - AWS
 - PyJWT
 - bcrypt

### 구현기능
공통
- 프로젝트 초기 세팅
- Database 모델링 및 ERD

김한준
- 회원가입 & 로그인
    - 이메일, 비밀번호 정규식 검사
    - 비밀번호 bcrypt 암호화
    - JWT Access Token 전송
- 유저인증
    - JWT Access Token 유효성 검토
    - Decorator 활용
- 제품 상세페이지 엔드포인트
    - 특정 상품 상세 data
    - 상품에 따른 추천/비교 상품 data

이동명
- 장바구니 엔드포인트
    - 카트 제품 추가 및 수량 변경
    - 요청 수량 및 재고 비교
- 주문 엔드포인트
    - 주문 이력관리
- 쿠폰 엔드포인트
    - 쿠폰 유효성 검토
- 메인페이지 엔드포인트
    - 메인페이지 Banner data 
    - 네비게이션바 data
- 백엔드 서버 배포
    - AWS

안희수
- 카테고리 페이지 엔드포인트
    - 카테고리별 제품 data
    - 가격/판매량/평점에 따른 제품 sorting list 제공

Reference
- 이 프로젝트는 Dr.jart+ 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.