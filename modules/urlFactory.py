import requests
import urllib
import json
import pandas as pd
import os

from .getKeyFromEnv import getKey

class urlFactory:
    API_KEY = getKey()
    
    # private methods
    def _fetchCCTVList(DEBUG_MODE=False):
        """
        CCTV 리스트를 API에서 받아와 JSON 파일로 저장

        Args:
            None

        Returns:
            int: 0 (성공), 1 (실패)
        """

        if urlFactory.API_KEY is None:
            if DEBUG_MODE: print("[ERROR] ValueError: CCTV_API_KEY environment variable not set")
            return 1

        
        url_cctv = f"https://openapi.its.go.kr:9443/cctvInfo?apiKey={urlFactory.API_KEY}&type=ex&cctvType=4&minX=127.17&maxX=127.18&minY=37.4&maxY=37.5&getType=json"
        response = urllib.request.urlopen(url_cctv)
        json_str = response.read().decode("utf-8")
        json_object = json.loads(json_str)

        # 각 CCTV 데이터에 tag 추가 (cctvname에서 괄호 안의 값)
        for item in json_object.get("response", {}).get("data", []):
            import re
            m = re.search(r'(\([^)]+\))', item.get("cctvname", ""))
            item["tag"] = m.group(1)[1:-1] if m else ""

        json.dump(json_object, open("cctv.json", "w", encoding="UTF-8"), indent=4, ensure_ascii=False, sort_keys=True)
        if DEBUG_MODE: print("[INFO] CCTV List fetched successfully.")
        return 0
    
    def _getCCTVList(DEBUG_MODE=False):
        """
        JSON 파일에서 CCTV 데이터를 로드

        Args:
            None

        Returns:
            dict: CCTV 데이터가 담긴 딕셔너리
        """

        json_object = open("cctv.json", "r", encoding="UTF-8")
        cctvList = json.load(json_object)
        if DEBUG_MODE: print("[INFO] CCTV List Loaded Successfully.")
        return cctvList

    def _getCCTVNameList(DEBUG_MODE=False, mode="name"):
        """
        CCTV 이름 목록 반환

        Args:
            mode (str): "name" 또는 "tag" (기본값: "name")

        Returns:
            list: CCTV 이름 리스트
        """

        cctvList = urlFactory._getCCTVList(DEBUG_MODE=DEBUG_MODE)

        if mode == "name":
            cctvNameList = [item["cctvname"] for item in cctvList["response"]["data"]]
        elif mode == "tag":
            cctvNameList = [item["tag"] for item in cctvList["response"]["data"]]
        else:
            if DEBUG_MODE: print(f"[ERROR] Invalid mode: {mode}. Use 'name' or 'tag'.")
            return []

        if DEBUG_MODE: print("CCTV Names:", cctvNameList)
        return cctvNameList
    
    def _getCCTVUrl(DEBUG_MODE=False, cctvName=""):
        """
        WIP

        CCTV 이름으로 URL 반환
        
        Args:
            cctvName (str): 검색할 CCTV 이름
            
        Returns:
            str: 해당 CCTV의 URL, 없으면 None 반환
        """
        
        if not cctvName:
            return None

        # 대소문자 구분 없이 검색
        cctvName_lowercase = cctvName.lower()

        return "asdf"
    
    # public methods
    def showAllCCTVs(DEBUG_MODE=False, mode="name"):
        """
        모든 CCTV 이름을 출력

        Args:
            mode (str): "name" 또는 "tag" (기본값: "name")

        Returns:
            None (Only Print)
        """
        import re
        names = urlFactory._getCCTVNameList(DEBUG_MODE=False, mode=mode)
        def sort_key(name):
            m = re.search(r'(\D+)(\d+)', name)
            if m:
                prefix = m.group(1)
                num = int(m.group(2))
                return (prefix, num)
            return (name, 0)
        if names:
            names_sorted = sorted(names, key=sort_key)
            print("사용 가능한 CCTV 목록 (오름차순)")
            for name in names_sorted:
                print(f" - {name}")
        else:
            print("사용 가능한 CCTV가 없습니다.")
    