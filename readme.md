## 프로젝트명: Dr.Mozzarella🧀

- Dr.jart+ 클론 프로젝트 (닥터자르트(화장품 판매 업체)를 모티브로 한 치즈 판매 사이트 구현)
- Account, Product category & detail, Cart 구현
- 초기 세팅부터 모델링과 프론트로 보내주는 모든 제품 data를 실제 사용할 수 있는 서비스 수준으로 개발
<br>
<br>
<br>

- 회원가입 & 로그인
```python
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        EMAIL_REGES    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        PASSWORD_REGES = '[A-Za-z0-9@#$%^&+=]{8,}'
        try:
            if not re.search(EMAIL_REGES, data["email"]):
                return JsonResponse ({"MESSAGE":"INVALID EMAIL"}, status = 400)
            
            if not re.search(PASSWORD_REGES, data["password"]):
                return JsonResponse ({"MESSAGE": "INVALID PASSWORD"}, status = 400)

            if Account.objects.filter(email=data["email"]).exists():
                return JsonResponse ({"MESSAGE":"EXISTED EMAIL"}, status = 400)
            
            hashed_passwored = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode()
        
            Account.objects.create(
                name     = data["name"],
                email    = data["email"],
                password = hashed_passwored,
                address  = data["address"]
            )
            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)
```

```python
class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not Account.objects.filter(email=data["email"]).exists():
                return JsonResponse({"MESSAGE":"INVALID USER"}, status = 401)

            user = Account.objects.get(email=data["email"])

            if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                access_token = jwt.encode({"user_id":user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse ({"MESSAGE":"SUCCESS", "TOKEN":access_token}, status = 200)

            return JsonResponse({"MESSAGE":"INVALID USER"}, status = 401)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY ERROR"}, status = 400)
```

<br>

- 유저인증
```python
def user_validator(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        try:
            if token:
                payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user         = Account.objects.get(id = payload["user_id"])
                request.user = user
                return func(self, request, *args, **kwargs)
            
            return JsonResponse({"MESSAGE":"NEED_SIGNIN"}, status = 401)
        
        except jwt.DecodeError:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"MESSAGE":"EXPIRED_TOKEN"}, status = 401)

        except Account.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
 
    return wrapper
```

<br>

- 제품 상세페이지 엔드포인트
```python
class ProductDetailView(View):
    def get(self, request, product_id):
        current_product = Product.objects.select_related('nutrition')\
            .prefetch_related('category', 'option_set', 'image_set', 'category__menu')\
            .get(id=product_id)

        current_category_dict = {}
        
        for category in current_product.category.all():
            current_category_dict[category.menu.name] = category

        routine_products = [current_product]
        compare_products = [current_product]

        routine_products.extend(list(Product.objects\
                            .filter(category=current_category_dict["milk"])\
                            .exclude(category=current_category_dict["style"])\
                            .prefetch_related('category', 'option_set')))
        compare_products.extend(list(Product.objects\
                            .filter(category=current_category_dict["milk"])\
                            .filter(category=current_category_dict["style"])\
                            .exclude(category=current_category_dict["countries"])))

        product_result = {
            'product_id'       : current_product.id,
            'product_name'     : current_product.name,
            'summary'          : current_product.summary,
            'description'      : current_product.description,
            'score'            : current_product.score,
            'description_image': current_product.description_image_url,
            'image_urls'       : [image.image_url for image in current_product.image_set.all()],
            'categories'       : [
                {
                    "category_id"         : category.id,
                    "category_name"       : category.name,
                    "category_image_url"  : category.image_url,
                    "category_description": category.description
                } for category in current_product.category.all()
            ],
            'option' : [
                {
                    "price"     : option.price,
                    "weight"    : option.weight,
                    "option_id" : option.id
                } for option in current_product.option_set.all()
            ],
            'nutrition' : [
                {
                    field.name : field.value_from_object(current_product.nutrition)
                } for field in current_product.nutrition._meta.fields if field.name != "id"
            ]
        }

        routine_results = [
            {
                'product_id'     : product.id,
                'product_name'   : product.name,
                'score'          : product.score,
                'thumbnail_image': product.thumbnail_image_url,
                'hover_image'    : product.hover_image_url,
                'current'        : (product == current_product),
                'option' : [
                    {
                        "price"  : option.price,
                        "weight" : option.weight,
                        "option_id"     : option.id
                    } for option in product.option_set.all()]
            } for product in routine_products[:3]
        ]

        compare_results  = [
            {
                'product_name'   : product.name,
                'description'    : product.description,
                'thumbnail_image': product.thumbnail_image_url,
                'option' : [
                    {
                        "price" : option.price,
                        "weight": option.weight,
                        "option_id"    : option.id
                    } for option in product.option_set.all()
                ]
            } for product in compare_products[:3]
        ]

        results = {
            "product" : product_result,
            "routine" : routine_results,
            "compare" : compare_results
        }

        return JsonResponse ({"results": results}, status = 200)
 ```
 
<br>
<br>
<br>

 ### 개발 인원 및 기간
 
 개발기간 : 2021/7/5 ~ 2021/7/16
 
 개발 인원 : 프론트엔드 3명, 백엔드 3명
 
 https://github.com/wecode-bootcamp-korea/22-1st-DrMozzarella-frontend
 
 https://github.com/wecode-bootcamp-korea/22-1st-DrMozzarella-backend

 ### 프론트
 박정훈, 황소미, 이종민

 ### 백엔드
 이동명, 김한준, 안희수

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
- 회원가입 & 로그인 & 유저인증
    - 이메일, 비밀번호 정규식 검사
    - 비밀번호 bcrypt 암호화
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
