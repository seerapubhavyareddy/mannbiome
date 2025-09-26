// components/Charts/Gauge.jsx
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './Gauge.css';

const Gauge = ({ value, label, color = '#00BFA5', max = 5 }) => {
  const svgRef = useRef();
  const containerId = useRef(`gauge-${Math.random().toString(36).substr(2, 9)}`);

  useEffect(() => {
    createGauge(value, color, label);
  }, [value, color, label]);

  // Handle window resize
  useEffect(() => {
    let resizeTimer;
    const handleResize = () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        createGauge(value, color, label);
      }, 250);
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(resizeTimer);
    };
  }, [value, color, label]);

  function createGauge(gaugeValue, primaryColor, labelText) {
    // Clear existing content
    const container = svgRef.current;
    if (!container) return;
    
    container.innerHTML = '';
    
    // Get container dimensions
    const containerWidth = container.clientWidth;
    const containerHeight = Math.floor(containerWidth * 0.65);
    
    // Scale factors
    const baseSize = 200;
    const scale = Math.min(containerWidth, containerHeight * 2) / baseSize;
    
    // Configuration
    const config = {
      minValue: 0,
      maxValue: 5,
      value: gaugeValue,
      transitionDuration: 1500,
      arcInnerRadius: 60 * scale,
      arcOuterRadius: 80 * scale,
      needleLength: 60 * scale,
      needleWidth: 6 * scale,
      needleRadius: 8 * scale,
      containerWidth: containerWidth,
      containerHeight: containerHeight,
      arcSegments: 50,
      scoreSize: 24 * scale,
      labelSize: 9 * scale,
      scaleSize: 8 * scale,
      primaryColor: primaryColor,
      labelText: labelText
    };
    
    // Create SVG with viewBox
    const svg = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
      .attr('preserveAspectRatio', 'xMidYMid meet');
    
    // Create a group for all gauge elements - adjust vertical position
    const gaugeGroup = svg.append('g')
      .attr('transform', `translate(${containerWidth / 2}, ${containerHeight / 2 + 20})`);
    
    // Angle scale
    const angleScale = d3.scaleLinear()
      .domain([0, config.maxValue])
      .range([-90, 90]);
    
    // Color scale
    const colorScale = d3.scaleLinear()
      .domain([0, 1, 2, 3, 4, 5])
      .range(['#FF4136', '#FF851B', '#FFDC00', '#9EE09E', '#5AC85A', '#01CF01'])
      .interpolate(d3.interpolateRgb.gamma(2.2));
    
    // Background arc path
    const backgroundArc = d3.arc()
      .innerRadius(config.arcInnerRadius)
      .outerRadius(config.arcOuterRadius)
      .startAngle(-Math.PI / 2)
      .endAngle(Math.PI / 2)
      .cornerRadius(10 * scale);
    
    // Add subtle shadow
    svg.append('defs')
      .append('filter')
      .attr('id', `gauge-shadow-${containerId.current}`)
      .append('feDropShadow')
      .attr('dx', '0')
      .attr('dy', '1')
      .attr('stdDeviation', '2')
      .attr('flood-opacity', '0.2');
    
    // Add background
    gaugeGroup.append('path')
      .attr('class', 'background-arc')
      .attr('d', backgroundArc)
      .attr('filter', `url(#gauge-shadow-${containerId.current})`)
      .style('fill', '#F7F7F7')
      .style('stroke', '#E0E0E0')
      .style('stroke-width', `${Math.max(1 * scale, 0.5)}px`);
    
    // Create colored segments
    const angleStep = Math.PI / config.arcSegments;
    const arcsGroup = gaugeGroup.append('g').attr('class', 'arcs-group');
    
    for (let i = 0; i < config.arcSegments; i++) {
      const startAngle = -Math.PI / 2 + (i * angleStep);
      const endAngle = startAngle + angleStep;
      const value = (i / config.arcSegments) * config.maxValue;
      const color = colorScale(value);
      
      const segmentArc = d3.arc()
        .innerRadius(config.arcInnerRadius)
        .outerRadius(config.arcOuterRadius)
        .startAngle(startAngle)
        .endAngle(endAngle)
        .cornerRadius(i === 0 || i === config.arcSegments - 1 ? 10 * scale : 0);
      
      arcsGroup.append('path')
        .attr('d', segmentArc)
        .style('fill', color);
    }
    
    // Add gauge border
    gaugeGroup.append('path')
      .attr('d', backgroundArc)
      .style('fill', 'none')
      .style('stroke', '#DDD')
      .style('stroke-width', `${Math.max(1 * scale, 0.5)}px`)
      .style('filter', `drop-shadow(0px 2px 2px rgba(0,0,0,0.1))`);
    
    // Add tick marks and labels
    const tickData = [0, 1, 2, 3, 4, 5];
    const tickGroup = gaugeGroup.append('g').attr('class', 'ticks');
    
    // Add tick marks
    tickGroup.selectAll('.tick')
      .data(tickData)
      .enter()
      .append('line')
      .attr('class', 'tick')
      .attr('x1', 0)
      .attr('y1', -config.arcOuterRadius - (1 * scale))
      .attr('x2', 0)
      .attr('y2', -config.arcOuterRadius + (3 * scale))
      .attr('stroke', '#555')
      .attr('stroke-width', Math.max(1 * scale, 0.5))
      .attr('transform', d => `rotate(${angleScale(d)})`);
    
    // Add numeric labels
    tickGroup.selectAll('.tick-label')
      .data(tickData)
      .enter()
      .append('text')
      .attr('class', 'tick-label')
      .attr('x', d => Math.sin(angleScale(d) * Math.PI / 180) * (config.arcOuterRadius + (10 * scale)))
      .attr('y', d => -Math.cos(angleScale(d) * Math.PI / 180) * (config.arcOuterRadius + (10 * scale)))
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'central')
      .attr('font-size', `${Math.max(9 * scale, 8)}px`)
      .attr('font-weight', '600')
      .attr('fill', d => colorScale(d))
      .text(d => d);
    
    // Add needle
    const needleGroup = gaugeGroup.append('g')
      .attr('class', 'needle')
      .attr('transform', 'rotate(-90)'); // Start at zero position
    
    // Needle
    needleGroup.append('path')
      .attr('d', `M 0 ${-config.needleLength} L ${-config.needleWidth} 0 L ${config.needleWidth} 0 Z`)
      .attr('fill', '#333')
      .style('filter', 'drop-shadow(0px 1px 2px rgba(0,0,0,0.3))');
    
    // Needle center circle
    needleGroup.append('circle')
      .attr('cx', 0)
      .attr('cy', 0)
      .attr('r', config.needleRadius)
      .attr('fill', '#444')
      .attr('stroke', '#333')
      .attr('stroke-width', Math.max(1 * scale, 0.5));
    
    // Needle inner circle
    needleGroup.append('circle')
      .attr('cx', 0)
      .attr('cy', 0)
      .attr('r', config.needleRadius * 0.6)
      .attr('fill', '#666')
      .attr('stroke', '#555')
      .attr('stroke-width', Math.max(0.5 * scale, 0.3));
    
    // Add score value
    const textGroup = gaugeGroup.append('g')
      .attr('class', 'text-group')
      .attr('text-anchor', 'middle')
      .attr('transform', `translate(0, ${config.arcOuterRadius * 0.3})`);
    
    // Large score value
    const scoreValue = textGroup.append('text')
      .attr('class', 'score-value')
      .attr('y', 0)
      .attr('font-size', `${config.scoreSize}px`)
      .attr('font-weight', 'bold')
      .attr('fill', config.primaryColor)
      .attr('dominant-baseline', 'central')
      .text('0.0');
    
    
    function updateNeedle(value, duration) {
  // Ensure value is safe
  const safeValue = (value != null && !isNaN(value)) ? Number(value) : 0;
  
  needleGroup
    .transition()
    .duration(duration)
    .attr('transform', `rotate(${angleScale(safeValue)})`);
  
  // Safe text animation
  scoreValue
    .transition()
    .duration(duration)
    .tween('text', function() {
      const i = d3.interpolate(0, safeValue);
      return function(t) {
        try {
          const currentValue = i(t);
          if (currentValue != null && !isNaN(currentValue) && isFinite(currentValue)) {
            this.textContent = currentValue.toFixed(1);
          } else {
            this.textContent = '0.0';
          }
        } catch (e) {
          this.textContent = '0.0';
        }
      };
    });
}
    // Run animation after a slight delay
    setTimeout(() => {
      updateNeedle(config.value, config.transitionDuration);
    }, 300);
  }

  return (
    <div className="gauge-container">
      <div ref={svgRef} className="gauge-chart" />
    </div>
  );
};

export default Gauge;