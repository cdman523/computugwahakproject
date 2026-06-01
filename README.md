메모할거 하는곳
문서우그는가히전설이라할수있다

계획서에 안적었는데 추가할거
1. Grass 클래스
초식동물들은 Eat으로 Grass를 먹음
Grass는 월드 맵에 타일 형태로 퍼져 있음
Grass는 지속적으로 성장함
양을 나타내는 속성 remain, 성장하는 메서드 grow를 가짐
동물이 Grass를 먹으면 해당 부분 타일에 위치한 Grass가 감소

2. Carcass를 먹는 방식
육식동물들은 주변의 Carcass를 먹음
단 하이에나는 remain 값에 상관 없이 섭취하지만
Lion은 신선한(remain이 70? 이상인) Carcass만 섭취
섭취시 remain이 감소

3.동물의 시스템
health는 hunger가 많이 차 있을 때 천천히 회복
자신의 속력으로 지정된 speed보다 빠르게 이동하면 hunger가 더 빠르게 감소


main.py
실제로 돌아가는 파일

base.py
부모 클래스들이 있는 파일

animals.py
동물 클래스를 구현하는 파일

carcass.py
시체를 구현하는 파일

simulate.py
시뮬레이터 돌리는 파일

behaves.py
행동패턴 작성 파일

Memo
메모할거 적어놓기

images 폴더
이미지 다 넣는곳

나머지
건드리는거아님


추가 메서드
surface
시뮬레이팅 중 이미지 생성