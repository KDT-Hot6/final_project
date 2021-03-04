# 폴더 요약
- csv는 가게와 리뷰로 나뉘어져 있습니다.
- trip_advisor_seoul_new.py가 실제로 쓰면 될 파일이고,
- advisor_seoul_res_my_use는 개인 사용입니다.

# 현재 진행상황
- raw data로 12000개 리뷰 수집했습니다.
- 가게는 총 187개입니다.

# tripadvisor 현황
- 밤 10시부터 아침 9시까지 12000개 수집했고, 문제 없었습니다.
  traffic제한 이런 문제가 크게 없는 사이트라고 생각합니다.
- 코드가 driver.implicit_wait()랑 time.sleep()을 사용해서 깔끔하지는 않지만,
  잘 수정해서 서버에 넣으면 잘 돌아갈 것 같습니다. 