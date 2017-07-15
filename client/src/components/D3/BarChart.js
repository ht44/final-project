import React, { Component } from 'react';
import './BarChart.css';
import * as d3 from 'd3';

class BarChart extends Component {
  constructor(props){
   super(props)
    this.createBarChart = this.createBarChart.bind(this)
    this.updateBarChart = this.updateBarChart.bind(this)
    // this.state = {year: this.props.year}
  }

  // shouldComponentUpdate(nextProps) {
  //   console.log(this.state.year);
  //   return nextProps.year !== this.state.year
  // }

  componentDidMount() {
    this.createBarChart()
  }

  componentDidUpdate(prevProps) {
    this.updateBarChart(prevProps)
  }

  createBarChart() {
    console.log('D3CREATE ---------------');
    const legend = this.props.legend
    const node = this.node
    const dataMax = d3.max(this.props.data)
    // const dataMin = d3.min(this.props.data)
    // const handleHover = this.props.handleHover

    const yScale = d3.scaleLinear()
                     .domain([0, dataMax])
                     .range([0, this.props.height / 2])

    // const xScale = d3.scaleBand()
    //                  .domain(this.props.data.map(function(d, i) { return i; }))
    //                  .range([0, this.props.width])
    //
    // const ryScale = d3.scaleLinear()
    //                  .domain([dataMax, 0])
    //                  .range([0, this.props.height / 2])

    d3.select(node)
      .style('border', '1px solid black')
      .attr('cursor', 'pointer')

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
      .style('fill', '#fe9922')
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('id', (d, i) => legend[i])
      .attr('height', 0)
      .transition()
      .attr('height', d => yScale(d))
      .duration(2000)
      // .on('end', function(data, i) {
      //   console.log('over');
      //   d3.select(this).on('mouseover', function(data, i) {
      //           let x = d3.event.target.id
      //           console.log(x);
      //           handleHover(x);
      //   });
      // });
  }

  updateBarChart(prevProps) {
    console.log('d3update');
    // console.log('WE ARE UPDATING');
    const handleHover = this.props.handleHover
    const legend = this.props.legend
    const node = this.node
    const dataMin = d3.min(this.props.data)
    const yScale = d3.scaleLinear()
                     .domain([0, dataMin])
                      .range([0, this.props.height / 2])

    if (this.props.data.length !== prevProps.data.length || this.props.year !== prevProps.year) {
      console.log('WAS------------------');
      this.props.changeModel()
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
        .attr('id', (d, i) => legend[i])
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('y', d => this.props.height - yScale(d))
        .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
        .attr('height', 0)
        .transition()
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('height',  d => yScale(d))
        .duration(2000)
        .on('end', function(data, i) {
          // console.log('over');
          d3.select(this).on('mouseover', function(data, i) {
                  let x = d3.event.target.id
                  // console.log(x);
                  handleHover(x);
          });
        });

    } else if (this.props.model) {
      this.props.changeModel()
      console.log('NOT-------------');
      d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .transition()
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('height', d => yScale(d))
      .duration(2000)
      .on('end', function(data, i) {
        d3.select(this).on('mouseover', function(data, i) {
            let x = d3.event.target.id
            // console.log(x);
            handleHover(x);
        });
      })

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
