import React, { Component } from 'react';
import { toRadians } from '../assets/util';

class Donut extends Component {
  componentDidUpdate() {
    const canvas = document.getElementById('donut');
    canvas.width = 750;
    canvas.height = 750;

    this.draw(canvas, canvas.getContext('2d'), ['#ef0e0e', '#efdc0e']);
  }

  draw(canvas, context, colors) {
    const totalValue = 100;
    let startAngle = toRadians(((this.props.start - 25) / 100) * 360);

    const redSliceAngle = 2 * Math.PI * 6 / totalValue;
    
    this.drawPieSlice(
      context,
      canvas.width/2,
      canvas.height/2,
      Math.min(canvas.width/2, canvas.height/2),
      startAngle,
      startAngle + redSliceAngle,
      colors[0]
    );

    startAngle += redSliceAngle;
    
    const yellowSliceAngle = 2 * Math.PI * 94 / totalValue;
    
    this.drawPieSlice(
      context,
      canvas.width/2,
      canvas.height/2,
      Math.min(canvas.width/2, canvas.height/2),
      startAngle,
      startAngle + yellowSliceAngle,
      colors[1]
    );

    this.drawPieSlice(
      context,
      canvas.width/2,
      canvas.height/2,
      0.85 * Math.min(canvas.width/2, canvas.height/2),
      0,
      2 * Math.PI,
      '#ffffff'
    );
  }

  drawPieSlice(context, centerX, centerY, radius, startAngle, endAngle, color) {
    context.fillStyle = color;
    context.beginPath();
    context.moveTo(centerX,centerY);
    context.arc(centerX, centerY, radius, startAngle, endAngle);
    context.closePath();
    context.fill();
  }
  
  render() {
    return (
      <canvas id="donut"/>
    );
  }
}

export { Donut };
