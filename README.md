# bikeseoulNotifier
서울자전거 <따릉이> 실시간 대여현황 조회 알리미 with Slack


# Pre-Requirments
* It is actually possible to hard-code the bot's API Token to the Python code, but there's a chance that we could accidently upload it to GitHub, so I recommend using OS's environment variable.

## Getting Slack Bot's Token
* [Reference Link](https://api.slack.com/bot-users)

## OS Environment Variable setting
* [Reference Link](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)

```Bash
# curl https://_$(workspace)_.slack.com/api/auth.test?token=_$(token_from_aove_step)_
# export SLACK_BOT_TOKEN='_$(token_from_above_step)_'
# export BOT_ID='_$(bot_id_value_from_above_Step)'
```
## requirements
* Installing dependency
  * Please use requirements.txt
  * ```Bash # pip install -r requirements.txt```


# Logic
* 기준 : 2018.06.10

* Slack에서 "여의도" 명령어를 날린다. (그 외는 처리 X)
* 여의도에 위치한 <따릉이> 대여소 중, 최 상/하단, 가장 좌/우측 대여소의 위도/경도를 참고하여 여의도 안에 있는 대여소를 확인
* 여의도에 있는 대여소들 중, 사용 가능한 자전거가 있는 대여소를 확인
* 특정 지점(현재는 개발자 회사)와의 거리(위도/경도 기준)로 가까운 대여소로 정렬
* 상위 5개의 대여소를 Slack 메시지로 응답

* 해당 스크립트는 백그라운드 프로세스로 사내 서버에서 동작


# TODO
* Python 쓰럽게 재개발
* 기능 추가 및 개선 (하드코딩 최대한 제거)
* 다양한 지역과 사용자의 위치값을 받는 받아서 근처만 조회하는 방향도 고려
* 더 이쁘게 보여주는 방향도 고려


# Reference
* [http://jybaek.tistory.com/575](http://jybaek.tistory.com/575)
* [https://www.fullstackpython.com/blog/build-first-slack-bot-python.html](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)