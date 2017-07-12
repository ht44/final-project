import React, { Component } from 'react';
import './BarChart.css';
import * as d3 from 'd3';

class BarChart extends Component {
  constructor(props){
   super(props)
    this.createBarChart = this.createBarChart.bind(this)
    this.updateBarChart = this.updateBarChart.bind(this)
    this.state = {}
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

    const sScale = d3.scaleLinear()
      .domain([dataMax, 0])
      .range([0, this.props.height / 2])


    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .enter()
      .append('rect')
      // .attr('width', xScale.bandwidth())

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
      .attr('height', d => yScale(d))
      // .on('mouseover', function(d){
      //     d3.select(this)
      //       .style("opacity", 0.2)})

    d3.select(node)
      .style('border', '1px solid black')


    const axis = d3.axisLeft(sScale)
    axis.ticks(5, "1%")
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
      console.log(prevProps.data.length);
    if (this.props.data.length !== prevProps.data.length) {
      console.log('doin');
      d3.select(node)
        .selectAll('rect')
        .data(this.props.data)
        .exit()
        // .transition()
        // .attr('height', '0')
        // .duration(4000)
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
        .attr('height', d => yScale(d))
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
    return <svg className="BarChart"ref={node => this.node = node} width={500} height={500}>
    </svg>
  }

}

export default BarChart
