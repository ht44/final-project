import React, { Component } from 'react';
import './BarChart.css';
import * as d3 from 'd3';

// #fe9922

class BarChart extends Component {
  constructor(props){
   super(props)
    this.createBarChart = this.createBarChart.bind(this)
    this.updateBarChart = this.updateBarChart.bind(this)
    this.state = {upperLimit: 10, height: this.props.height};
  }

  componentDidMount() {
    this.createBarChart();
  }

  componentDidUpdate(prevProps) {
    this.updateBarChart(prevProps);
  }

  /////////////////////////////////////////////////////////////////////////////

  createBarChart() {

    console.log('D3CREATE ---------------');

    const node = this.node;
    const dMax = this.state.upperLimit;
    const dataMin = d3.min(this.props.data);
    const dataMax = d3.max(this.props.data);
    const legend = this.props.legend;

    const yScale = d3.scaleLinear()
                     .domain([0, dMax])
                     .range([0, this.props.height])

    const rScale = d3.scaleLinear()
                     .domain([0, dMax])
                     .range([this.props.height, 0])

    const tScale = d3.scaleLinear()
                     .domain([0, dMax])
                     .range([this.props.height, 0])

    const axis = d3.axisRight(rScale)
                    .tickFormat(function(d) { return d + "%" })
                    .tickPadding(10)
                    .ticks(10, '%')

    const y_axis = d3.select(node)
                     .append("g")
                     .attr("class", "axis")
                     .attr("transform", "translate(0,0)")
                     .call(axis)


    const bars = d3.select(node)
                   .selectAll('rect')
                   .data(this.props.data)
                   .enter()
                   .append('rect')
                   .style('fill', '#ff004c')
                   .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
                   .attr('y', d => this.props.height - yScale(d))
                   .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
                   .attr('id', (d, i) => legend[i])
                   .attr('height', d => yScale(d))

    d3.select(node)
      .style('border', '1px solid green')
      .attr('cursor', 'cell')


    d3.select(node)
      .call(d3.zoom()
              .scaleExtent([0, 1])
              .on("zoom", () => {

                 let newTScale = d3.event.transform.rescaleY(tScale);
                 let newYScale = d3.event.transform.rescaleY(yScale);

                 let newBaseline = newTScale(0);
                 console.log('NEWBASELINE', newBaseline);
                 let newTop = this.props.height - newTScale(0);

                 y_axis.transition()
                       .duration(50)
                       .call(axis.scale(newTScale));

                 d3.select(node).selectAll('rect')
                                .transition()
                                .duration(50)

                                .attr( 'y', d => {
                                  return newTScale((((d - 1) / 1) * 100));
                                })

                                .attr('height', d => {
                                  return newBaseline - newTScale((((d - 1) / 1) * 100));
                                })
                this.setState({height: newBaseline});
             }));
  }

  /////////////////////////////////////////////////////////////////////////////


  updateBarChart(prevProps) {
    console.log('D3UPDATE ---------------');
    const handleHover = this.props.handleHover
    const legend = this.props.legend
    const node = this.node
    const dMax = this.state.upperLimit;
    const dataMin = d3.min(this.props.data)
    const dataMax = d3.max(this.props.data)
    const yScale = d3.scaleLinear()
                     .domain([0, dMax])
                     .range([0, this.props.height])
    const tScale = d3.scaleLinear()
                     .domain([0, dMax])
                     .range([this.props.height, 0])


    if (this.props.data.length !== prevProps.data.length || this.props.level !== prevProps.level) {
      console.log('AAAAAAAAA ------------------');
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
      const transform = d3.zoomTransform(node)
      const newTScale = transform.rescaleY(tScale)
      const newYScale = transform.rescaleY(yScale)
      console.log(newTScale);

    d3.select(node)
      .selectAll('rect')
      .data(this.props.data)
      .transition()
      .attr('x', (d, i) => i * (this.props.width / this.props.data.length))
      .attr('y', d => newTScale((((d - 1) / 1) * 100)))
      // .attr('y', d => this.props.height - yScale(d))
      .attr('width', this.props.width / this.props.data.length - this.props.barPadding)
      .attr('height', d => this.state.height - newTScale((((d - 1) / 1) * 100)))
      .duration(2000)
      .on('end', function(data, i) {
        d3.select(this)
          .on('mouseover', function(data, i) {
            d3.select(this).style('fill', '#00f2b1')
            const id = d3.event.target.id
            handleHover({name: legend[id], index: parseInt(id, 10)});

        }).on('mouseout', function(data, i) {
          d3.select(this).style('fill', '#ff004c')
        });
      });

    }
  }

  render() {
    console.log(this.state.height);
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
