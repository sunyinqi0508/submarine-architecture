import React from 'react';
import { toRadians } from '../assets/util';

const Submarine = (props) => (
  <div
    className="sea"
    style={{
      left: 255 + 346.875 * Math.cos(toRadians(((props.pos - 25)/100) * 360)), 
      top: 313 + 346.875 * Math.sin(toRadians(((props.pos - 25)/100) * 360))
    }}
  >
    <div className="circle-wrapper">
      <div className="bubble"></div>
      <div className="submarine-wrapper">
        <div className="submarine-body">
          <div className="window"></div>
          <div className="engine"></div>
          <div className="light"></div>
        </div>
        <div className="helix"></div>
        <div className="hat">
          <div className="leds-wrapper">
            <div className="periscope"></div>
            <div className="leds"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

const Probe = (props) => (
  <div
    className='needle'
    style={{
      left: (375 + 30) + 346.875 * Math.cos(toRadians(((props.pos - 25)/100) * 360)), 
      top: (375 + 30 + 24) + 346.875 * Math.sin(toRadians(((props.pos - 25)/100) * 360))
    }}
  />
);
  
  export { Submarine, Probe };