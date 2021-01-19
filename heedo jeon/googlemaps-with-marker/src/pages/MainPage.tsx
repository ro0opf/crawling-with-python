// src/pages/MainPage.tsx
import React from 'react'
import GoogleMapReact from 'google-map-react';

const Marker = (props: any) => {
  const { color, name, id } = props;
  return (
    <div className="marker"
      style={{ backgroundColor: color, cursor: 'pointer'}}
      title={name}>
        {name}
      </div>
  );
};

function MainPage() {
  let defaultProps = {
    center: {
      lat: 59.95,
      lng: 30.33
    },
    zoom: 11
  };

  return (
    <>
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: "AIzaSyCT5wjfqFRNzYHN-yB4iavQdd5kHRfckWQ" }}
          defaultCenter={defaultProps.center}
          defaultZoom={defaultProps.zoom}
        >
          <Marker lat={59.95} lng={30.33} name={"awdaw"} />
        </GoogleMapReact>
      </div>
    </>
  )
}

export default MainPage
