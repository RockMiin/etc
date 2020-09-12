## 데이터 베이스 개념 정리 CHAPTER01

**집계 함수 및 쿼리 구현할 때 팁**

SUM, AVG, COUNT 등이 있다.

집계함수에서는 NULL값이 무시가 된다.

그룹별로 집계함수를 사용하고 싶을 때는 GROUP BY를 사용한다.

HAVING은 간단하게 말해서 GROUP BY에서 만든 GROUP에 대하여 조건을 거는 느낌

WHERE과 HAVING의 차이

WHERE은 모든 행에 대한 조건을 적용하지만, HAVING은 GROUP BY를 통해 만들어진 GROUP에 대해서만 조건을 적용한다.

집계함수는 두 개를 중복해서 바로는 쓸 수 없는 것 같다.

MAX(SUM()) 이런 식으로 사용이 불가능 해서, FROM 쪽에 SELECT문으로 SUM() 컬럼이 들어간 테이블을 만들어줘서 그 것에 별칭을 취한 뒤 사용하는 느낌으로 사용 <- 이렇게 할 때도 where에 테이블 간의 관계를 적어줘야한다. 그렇지 않으면 이상한 값이 나오게 됨..

```mysql
select c.customerNumber, c.customerName, od.orderNumber,  
	count(distinct o.orderNumber) as order_count, 
	sum(sum_price)/ count(distinct o.orderNumber) as avg_price, max(sum_price)
from customers as c, orders as o, 
	(select orderNumber, sum(quantityOrdered*priceEach) as sum_price
from orderdetails group by orderNumber) as od
where c.customerNumber=o.customerNumber and o.orderNumber= od.orderNumber
group by c.customerNumber;
```

위에 보이는 코드는 mysql sample 데이터베이스인 classicmodels에서 

Q. 고객 회사들에 대해 매출 성향을 분석하려고 한다. 각 고객 회사에 대해 회사명, 주문 횟수, 평균 주문 금액, 최대 주문 금액을 구하시오.

를 구하는 쿼리문이다. MAX(SUM())과 같은 기능을 만들어 주기 위해 max(sum_price)를 사용해 준 것을 볼 수있다.

또한 group에 따라 출력양이 바뀌게 되는데 잘못 조정하면 질의에 해당하는 첫번째 row만 가져오게 되므로 주의해야 한다.

COUNT를 할 때 distinct를 주고 안주고 그런 옵션에 따라서 값이 바뀌게 되므로 주의해야 한다. <- 필자가 애를 많이 먹었음.

**뷰(VIEW)**

뷰는 사용자에게 접근이 허용된 자료만을 제한적으로 보여주기 위해 만들어진 가상의 테이블

뷰는 기본 테이블로부터 유도된 테이블이기 때문에 기본 테이블과 같은 구조를 가지지만 가상 테이블이기 때문에 물리적으로 구현되지 않는다. + **데이터의 논리적 독립성을 제공할 수있다.** 

뷰를  통해서만 데이터에 접근하게 되면 뷰에 나타나지 않는 데이터를 안전하게 보호할 수  있다.

**제약조건(Constraint)**

constraint(제약조건):  결점 없이 정확하고 유효한 데이터가 데이터 베이스에 저장될 수 있도록 하기 위하여 데이터를 조작하는데 한계를 규정.

제약조건을 추가, 삭제 변경할 때에는 alter 명령문을 이용해 변경을 한다.

```mysql
alter table 테이블명 add constraint 제약 이름 제약 조건;
alter table 테이블명 modify 컬럼 조건;
alter table 테이블명 drop constraint 제약이름;
```

컬럼을 추가할 때 주의사항

외래키 제약조건이 걸려있는 경우 부모 테이블부터 추가를 해줘야 한다. (error code 1452 방지)

E-R다이어그램을 보고 실선으로 연결되어 있는 최상위 부모로부터 차근차근 입력해줘야 하는 것 같다.

