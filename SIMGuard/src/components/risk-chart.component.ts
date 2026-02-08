import { Component, input, ElementRef, viewChild, effect } from '@angular/core';
import * as d3 from 'd3';
import { RiskDistribution } from '../types';

@Component({
  selector: 'app-risk-chart',
  standalone: true,
  template: `<div #chartContainer class="w-full h-64 flex items-center justify-center"></div>`
})
export class RiskChartComponent {
  data = input.required<RiskDistribution>();
  chartContainer = viewChild<ElementRef>('chartContainer');

  constructor() {
    effect(() => {
      const container = this.chartContainer();
      const dist = this.data();
      if (container && dist) {
        this.createChart(container.nativeElement, dist);
      }
    });
  }

  createChart(element: HTMLElement, data: RiskDistribution) {
    // Clear previous
    d3.select(element).selectAll('*').remove();

    const width = 250;
    const height = 250;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select(element)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal()
      .domain(['High', 'Medium', 'Low'])
      .range(['#ef4444', '#f59e0b', '#14b8a6']); // Tailwind Red-500, Amber-500, Teal-500

    const pieData = [
      { label: 'High', value: data.High },
      { label: 'Medium', value: data.Medium },
      { label: 'Low', value: data.Low }
    ].filter(d => d.value > 0);

    // FIX: Removed <any> generic type argument
    const pie = d3.pie().value((d: any) => d.value);
    const data_ready = pie(pieData);

    // FIX: Removed <any> generic type argument
    const arc = d3.arc()
      .innerRadius(radius * 0.5) // Donut hole
      .outerRadius(radius * 0.8);

    // Build the pie chart
    svg
      .selectAll('allSlices')
      .data(data_ready)
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('fill', (d: any) => color(d.data.label) as string)
      .attr('stroke', '#0f172a')
      .style('stroke-width', '4px')
      .style('opacity', 0.9)
      .transition()
      .duration(1000)
      .attrTween('d', function(d: any) {
        const i = d3.interpolate(d.startAngle+0.1, d.endAngle);
        return function(t: any) {
            d.endAngle = i(t);
            return arc(d) || '';
        }
      });
      
    // Center Text
    svg.append('text')
       .attr('text-anchor', 'middle')
       .attr('dy', '-0.5em')
       .text('Total Users')
       .attr('class', 'fill-slate-400 text-xs font-medium uppercase');
    
    const total = data.High + data.Medium + data.Low;
    svg.append('text')
       .attr('text-anchor', 'middle')
       .attr('dy', '1em')
       .text(total)
       .attr('class', 'fill-white text-3xl font-bold');
  }
}