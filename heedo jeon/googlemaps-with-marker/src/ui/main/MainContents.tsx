// src/ui/main/MainContents.tsx
import React, { useEffect, useState } from 'react'
import Marker from '../../data/Marker'
import Wrapper from './MainContents.css'

declare global {
  interface Window {
    kakao: any
  }
}

const markerData = [
  {
    title: '콜드스퀘어',
    lat: 37.62197524055062,
    lng: 127.16017523675508,
  },
  {
    title: '하남돼지집',
    lat: 37.620842424005616,
    lng: 127.1583774403176,
  },
  {
    title: '수유리우동',
    lat: 37.624915253753194,
    lng: 127.15122688059974,
  },
  {
    title: '맛닭꼬',
    lat: 37.62456273069659,
    lng: 127.15211256646381,
  },
]

function MainContents() {
  let [markers, setMarkers] = useState<Marker[]>([])
  let [map, setMap] = useState<any>()

  useEffect(() => {
    let container = document.getElementById('map') //지도를 담을 영역의 DOM 레퍼런스
    let options = {
      //지도를 생성할 때 필요한 기본 옵션
      center: new window.kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
      level: 3, //지도의 레벨(확대, 축소 정도)
    }

    setMap(new window.kakao.maps.Map(container, options)) //지도 생성 및 객체 리턴
  }, [])

  useEffect(() => {
    console.log(123123)

    console.log(map)

    markers.forEach((marker) => {
      new window.kakao.maps.Marker({
        position: new window.kakao.maps.LatLng(marker.lat, marker.lng),
        title: marker.title,
      }).setMap(map)
    })
  }, [markers])

  return (
    <Wrapper>
      <div id="map" style={{ width: '80vw', height: '100vh' }} />
      <div className="Buttons">
        <div
          className="Button"
          onClick={() => {
            setMarkers(markerData)
            console.log(markers)
          }}
        >
          test
        </div>
      </div>
    </Wrapper>
  )
}

export default MainContents
