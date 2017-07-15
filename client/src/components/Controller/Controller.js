import React, { Component } from 'react';
import Display from '../Display/Display'
import Form from '../Form/Form'
import Console from '../Console/Console'
import BarChart from '../D3/BarChart'
import './Controller.css'

class Controller extends Component {
  constructor(props) {
    super(props);

    this.balance = this.balance.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.changeModel = this.changeModel.bind(this);
    this.showModel = this.showModel.bind(this);

    this.state = {
      data: [],
      zeros: [],
      legend: [],
      current: 'Agriculture, forestry, fishing, and hunting',
      model: false,
      width: 500,
      height: 500,
      barpad: 1,
    };

  }

  aSyncXhr(level, year) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', `http://localhost:8000/dash/${level}/${year}/`)
      xhr.onload = () => resolve(xhr.response)
      xhr.onerror = () => resolve(xhr.statusText)
      xhr.send();
    })
  }

  componentDidMount() {
    // console.log('CONTROLLERMOUNT--------');
    this.aSyncXhr(this.props.level, this.props.year).then((resp) => {
      this.balance(resp)
    })
  }

  componentDidUpdate() {
    // console.log('updated');
  }

  componentWillReceiveProps(newProps) {
    console.log('propped');
    console.log(newProps.level, newProps.year);
    // console.log('depropped');
    this.aSyncXhr(newProps.level, newProps.year).then(response => {
      this.balance(response)
    })
  }

  changeModel(){
    this.setState((prevState, props) => {
      return {model: !prevState.model}
    })
  }

  showModel(parsed) {
    const data = parsed
    const legend = data['legend']
    const zeros = Array.apply(null, Array(legend.length)).map(Number.prototype.valueOf,0);
    this.setState({
      zeros: zeros,
      data: parsed['rel_unit_price'],
      year: data['year'],
      level: data['level'],
      model: true
    });
  }

  balance(payload) {
    const data = JSON.parse(payload);
    const legend = data['legend']
    const zeros = Array.apply(null, Array(legend.length)).map(Number.prototype.valueOf,0);
    this.setState({
      zeros: zeros,
      data: data['unit_price'],
      legend: legend,
      level: data['level'],
      year: data['year']
    })
  }

  handleHover(ev) {
    this.setState({current: ev})
  }



  render() {
    const year = this.state.year
    const isModel = this.state.model
    const level = this.state.level
    const current = this.state.current
    const zeros = this.state.zeros
    const width = 500
    const height = 500
    const legend = this.state.legend

    ///////////////
    const data = this.state.data.map(d => d * 5)
    ////////////////

    return(
      <div className="Controller">
        <Console display={current} />

        <Display key={year}>
          <Form
            model={this.showModel}
            zeros={zeros}
            current={this.props.current}
            level={level}
            year={year}
            legend={legend}/>
        </Display>

        <BarChart
          changeModel={this.changeModel}
          model={isModel}
          handleHover={this.handleHover}
          year={year}
          legend={legend}
          data={data}
          height={height}
          width={width}
          barPadding={this.state.barpad} />

      </div>
    )
  };
}

export default Controller;
