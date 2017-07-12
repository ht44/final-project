import React, { Component } from 'react';
import './BarChart.css';
import * as d3 from 'd3';

class BarChart extends Component {
  constructor(props){
   super(props)
    this.createBarChart = this.createBarChart.bind(this)
    this.updateBarChart = this.updateBarChart.bind(this)
  }

  componentDidMount() {
    this.createBarChart()
  }

  componentDidUpdate(prevProps) {
    this.updateBarChart(prevProps)
  }

  createBarChart() {

    const node = this.node
    const dataMax = d3.max(this.props.data)
    const dataMin = d3.min(this.props.data)

    const yScale = d3.scaleLinear()
                     .domain([0, dataMax])
                     .range([0, this.props.height / 2])

    const xScale = d3.scaleBand()
                     .domain(this.props.data.map(function(d, i) { return i; }))
                     .range([0, this.props.width])

    const ryScale = d3.scaleLinear()
                     .domain([dataMax, 0])
                     .range([0, this.props.height / 2])

    d3.select(node).style('border', '1px solid black')

    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .enter()
      .append('rect')

    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .exit()
      .remove()

    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .style('fill', '#fe9922')
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('height', 0)
      .transition()
      .attr('height', d => yScale(d))
      .duration(2000)




    const axis = d3.axisLeft(ryScale)
    axis.ticks(8, "1%")
    // const xAxis = d3.axisBottom(xScale)
    // xAxis.ticks(17, 's')

    d3.select(node).append("g")
      .attr('class', 'axis')
      .attr("transform", "translate(30,250)")
      .call(axis)
    // d3.select(node).append("g")
    //   .attr('class', 'axis')
    //   .attr("transform", "translate(0,480)")
    //   .call(xAxis)

  }

  updateBarChart(prevProps) {

    const node = this.node
    const dataMax = d3.max(this.props.data)
    const yScale = d3.scaleLinear()
                     .domain([0, dataMax])
                     .range([0, this.props.height / 2])

    if (this.props.data.length !== prevProps.data.length) {
      console.log('special update');

      d3.select(node)
        .selectAll('rect')
        .data(this.props.data)
        .exit()
        .remove()

      d3.select(node)
        .selectAll('rect')
        .data(this.props.data)
        .enter()
        .append('rect')

      d3.select(node)
        .selectAll('rect')
        .data(this.props.data)
        .style('fill', '#fe9922')
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('y', d => this.props.height - yScale(d))
        .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
        .attr('height', 0)
        .transition()
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('height',  d => yScale(d))
        .duration(2000)

    } else {

      d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .transition()
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('height', d => yScale(d))
      .duration(2000)

    }
  }

  render() {
    return(
      <svg
        className="BarChart"
        ref={node => this.node = node}
        width={500}
        height={500}>
      </svg>
    )
  }
}
export default BarChart
