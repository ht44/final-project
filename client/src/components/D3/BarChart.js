import React, { Component } from 'react';
import './BarChart.css';
import * as d3 from 'd3';

// #fe9922

class BarChart extends Component {
  constructor(props){
   super(props)
    this.createBarChart = this.createBarChart.bind(this)
    this.updateBarChart = this.updateBarChart.bind(this)
  }

  componentDidMount() {
    this.createBarChart();
  }

  componentDidUpdate(prevProps) {
    this.updateBarChart(prevProps);
  }

  createBarChart() {

    console.log('D3CREATE ---------------');

    const legend = this.props.legend
    const node = this.node
    const dataMax = d3.max(this.props.data)
    const dataMin = d3.min(this.props.data)

    const yScale = d3.scaleLinear()
                     .domain([0, 15])
                     .range([0, this.props.height])
                    //  .domain([1, dataMax])
                    //  .range([this.props.height / 2, this.props.height])


    d3.select(node)
      .style('border', '1px solid green')
      .attr('cursor', 'cell')

    // d3.select(node)
    //   .selectAll('rect')
    //   .data(this.props.data)
    //   .exit()
    //   .remove()

    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .enter()
      .append('rect')
      // .style('fill', '#fe9922')
      .style('fill', '#ff004c')
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      // .attr('y', d => this.props.height - yScale(d))
      .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('id', (d, i) => legend[i])
      .attr('height', 0)
      .transition()
      .attr('height', d => yScale(d))
      // .attr('height', d => yScale((((d - 1) / 1) * 100)))
      .duration(2000)
  }

  updateBarChart(prevProps) {

    console.log(this.props.data);
    console.log('D3UPDATE ---------------');
    let result = this.props.data.map(datum => {
      return ((datum - 1) / 1) * 100;
    });
    console.log(result);
    const handleHover = this.props.handleHover
    const legend = this.props.legend
    const node = this.node
    const dataMin = d3.min(this.props.data)
    const dataMax = d3.max(this.props.data)
    console.log(dataMin, dataMax);
    const yScale = d3.scaleLinear()

                     .domain([0, 15])
                     .range([0, this.props.height])
                      //  .domain([0, dataMin])
                      // .range([0, this.props.height / 2])


    if (this.props.data.length !== prevProps.data.length || this.props.level !== prevProps.level) {
      // console.log('AAAAAAAAA ------------------');
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
        .style('fill', '#ff004c')
        .attr('id', (d, i) => i)
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('y', d => this.props.height - yScale(d))
        .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
        .attr('height', 0)
        .transition()
        .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
        .attr('height',  d => yScale(d))
        .duration(2000)
        .on('end', function(data, i) {
          d3.select(this).on('mouseover', function(data, i) {
                  let x = d3.event.target.id
                  d3.select(this).attr('fill', '#fe9922')
                  handleHover(x);
          });
        });

    }
    if (this.props.model || this.props.year !== prevProps.year) {
      this.props.changeModel()
      console.log('BBBBBBBB -------------');

      d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .transition()
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => this.props.height - yScale((((d - 1) / 1) * 100)))
      // .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('height', d => yScale((((d - 1) / 1) * 100)))
      .duration(2000)
      .on('end', function(data, i) {
        d3.select(this)
          .on('mouseover', function(data, i) {

            let id = d3.event.target.id
            d3.select(this).style('fill', '#00f2b1')
            handleHover({name: legend[id], index: parseInt(id, 10)});

        }).on('mouseout', function(data, i) {

          d3.select(this).style('fill', '#ff004c')

        });
      });

    }
  }

  render() {
    return(
      <svg
        className="BarChart"
        ref={node => this.node = node}
        width={this.props.width}
        height={this.props.height}>
      </svg>
    )
  }
}
export default BarChart
