#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
bot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

base_request_url="https://www.bikeseoul.com/app/station/getStationRealtimeStatus.do"
region_param="stationGrpSeq"
ydp_region_code="17"

TOP_LAT=37.531239
BOTTON_LAT=37.517368
LEFT_LONG=126.914925
RIGHT_LONG=126.938881

# 여의도 영역
# 200 국회, 가장 좌측
#stationLatitude : 37.528728
#stationLongitude : 126.914925

# 201. 진미파라곤 앞, 가장 상단
#stationLatitude	:	37.531239
#stationLongitude	:	126.921333

# 222. 시범아파트버스정류장 옆, 가장 우측
#stationLatitude	:	37.520271
#stationLongitude	:	126.938881

# 225. 앙카라공원 앞, 가장 하단
#stationLatitude	:	37.517368
#stationLongitude	:	126.929253


avail_station=[]

def append_available_station( station ):
    # 여의도에 있고, 사용이 가능한 자전거가 있다면 임시 dict에 필요한 정보만
    # 추가해서 생성
    tmp_dict = {
            'stationId' : station['stationId'],
            'stationName' : station['stationName'],
            'parkingBikeTotCnt' :int(station['parkingBikeTotCnt']),
            'rackTotCnt' : int(station['rackTotCnt']),
            'stationLatitude' : float(station['stationLatitude']),
            'stationLongitude': float(station['stationLongitude']),
            'how_far' : -1
            }

    # 임시 dict에 정보 추가
    avail_station.append(tmp_dict)


def bike_status_parser():
    ydp_url = base_request_url + "?" + region_param + "=" + ydp_region_code

    response = requests.get(ydp_url)
    json_obj = response.json()

    for station in json_obj['realtimeList']:
        # 위도와 경도를 기반으로 여의도 안에 있는 따릉이 정거장인지 확인
        if float(station['stationLatitude']) > TOP_LAT or float(station['stationLatitude']) < BOTTON_LAT:
            continue

        if float(station['stationLongitude']) > RIGHT_LONG or float(station['stationLongitude']) < LEFT_LONG:
            continue

        # 현재 사용 가능한 자전거가 있는지 확인
        if int(station['parkingBikeTotCnt']) == 0:
            continue

        append_available_station( station )


def check_distance_from_company():
    COMPANY_LAT=37.523556
    COMPANY_LONG=126.925456

    for station in avail_station:
        lat_sub = abs(station['stationLatitude'] - COMPANY_LAT)
        long_sub = abs(station['stationLongitude'] - COMPANY_LONG)
        station['how_far'] = round(long_sub + lat_sub, 6)

    avail_station.sort(key=lambda k:k['how_far'])

def check_realtime_status():
    print("[여의도]에서 사용 가능한 자전거가 있는 따릉이 정류장을 검색합니다!")

    bike_status_parser()
    check_distance_from_company()

    for idx in range(5):
        print(avail_station[idx])

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    default_response = "지원되지 않는 명령어입니다"

    response = " "

    if command.startswith("여의도"):
        check_realtime_status()
        for idx in range(5):
            response += avail_station[idx]['stationName'] + "-대여소.\t"  + " 가능한 대수 : " + str(avail_station[idx]['parkingBikeTotCnt']) + "\n"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")

        bot_id = slack_client.api_call("auth.test")["user_id"]

        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())

            if command:
                handle_command(command, channel)

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

