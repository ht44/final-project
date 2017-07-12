import React, { Component } from 'react';
import Display from '../Display/Display'
import Panel from '../Panel/Panel'
import BarChart from '../D3/BarChart'
import './Controller.css'

class Controller extends Component {
  constructor(props) {
    super(props);
    this.populate = this.populate.bind(this);
    this.state = {
      values: 'values displayed here',
      data: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      width: 500,
      height: 500,
      barpad: 1
    };
  }

  populate(payload) {
    const data = JSON.parse(payload);
    const unitPrice = data['unit_requirements']

    this.setState({values: payload, data: unitPrice})
  }

  render() {
    const values = this.state.values
    const data = this.state.data.map(d => d * 5)
    const width = 500
    const height = 500
    return(
      <div className="Controller">
        <Panel populate={this.populate} />
        <BarChart data={data} height={height} width={width} barPadding={this.state.barpad}/>
        <Display values={values}/>
      </div>
    )
  };
}

export default Controller;
