import React, { Component } from 'react';
import Display from '../Display/Display'
import Panel from '../Panel/Panel'
import BarChart from '../D3/BarChart'
import './Controller.css'

class Controller extends Component {
  constructor(props) {
    super(props);
    this.populate = this.populate.bind(this);
    this.relative = this.relative.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.state = {
      values: 'values displayed here',
      data:  [1.0061641709544444, 1.0041627769347108, 1.0050611239464429, 1.0049726128179277, 1.0076491968781796, 1.004884935517597, 1.004580056289883, 1.0213202583986682, 1.0122195139985455, 1.0085797400333913, 1.0050652025534217, 1.0037229578137747, 1.0051803872114877, 1.0030223390437152, 1.0071376053912848, 1.0070243754971835, 1.0071392864379751],
      current: 0,
      width: 500,
      height: 500,
      barpad: 1,
      legend: ['Agriculture, forestry, fishing, and hunting', 'Mining', 'Utilities', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing', 'Information', 'Finance, insurance, real estate, rental, and leasing', 'Professional and business services', 'Educational services, health care, and social assistance', 'Arts, entertainment, recreation, accommodation, and food services', 'Other services, except government', 'Government', 'Scrap, used and secondhand goods', 'Noncomparable imports and rest-of-the-world adjustment']
    };
  }

  populate(payload) {
    const data = JSON.parse(payload);
    const unitPrice = data['unit_price']
    const legend = data['legend']
    this.setState({values: payload, data: unitPrice, legend: legend})
  }

  handleHover(ev) {
    this.setState({current: ev})
  }

  relative(arg) {
    this.setState({data: arg})
  }

  render() {
    const current = this.state.current
    const values = this.state.values
    const data = this.state.data.map(d => d * 5)
    const width = 500
    const height = 500
    const legend = this.state.legend
    return(
      <div className="Controller">
        <Panel current={current} populate={this.populate} relative={this.relative} legend={legend}/>
        <BarChart handleHover={this.handleHover}data={data} height={height} width={width} barPadding={this.state.barpad}/>
      </div>
    )
  };
}

export default Controller;
