import React, { Component } from 'react';
import Scroll from '../Scroll/Scroll'
import Form from '../Form/Form'
import Console from '../Console/Console'
import Button from '../Button/Button'
import BarChart from '../D3/BarChart'
import './Controller.css'

class Controller extends Component {
  constructor(props) {
    super(props);

    this.balance = this.balance.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.changeModel = this.changeModel.bind(this);
    this.showRelative = this.showRelative.bind(this);
    this.restore = this.restore.bind(this);
    this.buttonClick = this.buttonClick.bind(this)
    this.changeValued = this.changeValued.bind(this)
    this.changeCurrent = this.changeCurrent.bind(this)


    this.state = {
      current: 'Agriculture, forestry, fishing, and hunting',
      currentNum: 0,
      currentVal: 0,
      data: [],
      ones: [],
      legend: [],
      model: false,
      width: 650,
      height: 650,
      barpad: 1,
      valued: false,
    };

  }

  changeCurrent(ev) {
    this.setState({currentNum: ev});
  }

  aSyncXhr(level, year) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', `/dash/${level}/${year}/`)
      xhr.onload = () => resolve(xhr.response)
      xhr.onerror = () => resolve(xhr.statusText)
      xhr.send();
    })
  }

  componentDidMount() {
    this.aSyncXhr(this.props.level, this.props.year).then((resp) => {
      this.balance(resp)
    })
  }

  componentDidUpdate() {
    // console.log('updated');
  }

  componentWillReceiveProps(newProps) {
    console.log('propped', newProps.level, newProps.year);
    this.aSyncXhr(newProps.level, newProps.year).then(response => {
      this.balance(response)
    })
  }

  changeModel(){
    this.setState((prevState, props) => {
      return {model: !prevState.model}
    })
  }

  changeValued(){
    this.setState((prevState, props) => {
      return {valued: !prevState.valued}
    })
  }

  buttonClick(ev) {
    this.restore();
    this.changeValued();
  }

  showRelative(parsed) {
    const data = parsed
    this.setState({
      // zeros: zeros,
      data: parsed['rel_unit_price'],
      year: data['year'],
      level: data['level'],
      model: true
    });
  }

  restore() {
    const legend = this.state.legend;
    const ones = Array.apply(null, Array(legend.length)).map(Number.prototype.valueOf,1);
    this.setState({
      data: ones,
      year: this.state.year,
      level: this.state.level,
      model: true
    });
  }

  balance(payload) {
    const data = JSON.parse(payload);
    const legend = data['legend']
    const ones = Array.apply(null, Array(legend.length)).map(Number.prototype.valueOf,1);

    // let width, height;

    // if (data['level'] === 'sector') {
    //   width = 800;
    //   height = 500;
    // } else {
    //   width = 1100;
    //   height = 700;
    // }

    this.setState({
      // width: width,
      // height: height,
      data: ones,
      legend: legend,
      level: data['level'],
      year: data['year']
    })
  }

  handleHover(ev) {
    this.setState({current: ev.name, currentNum: ev.index, currentVal: ev.data})
  }

  render() {
    const width = this.state.width;
    const height = this.state.height;
    const padding = this.state.barpad;
    const year = this.state.year;
    const level = this.state.level;
    const valued = this.state.valued;
    const isModel = this.state.model;
    const legend = this.state.legend;

    const current = this.state.current + ' | ' + this.state.currentVal.toFixed(2);
    const data = this.state.data

    return(
      <div className="Controller">
        <Console display={current} />

        <div className="Graph">
          <BarChart
            changeModel={this.changeModel}
            model={isModel}
            handleHover={this.handleHover}
            year={year}
            level={level}
            legend={legend}
            data={data}
            height={height}
            width={width}
            barPadding={padding} />

          <div className="Sidebar" style={{height: height}}>
            <Button value={'restore'} handleClick={this.buttonClick} />

            <Scroll key={year}>
              <Form key={valued}
                changeCurrent={this.changeCurrent}
                showRelative={this.showRelative}
                buttonClick={this.buttonClick}
                restore={this.restore}
                current={this.state.currentNum}
                level={level}
                year={year}
                legend={legend}/>
            </Scroll>
          </div>

        </div>

      </div>
    )
  };
}

export default Controller;
