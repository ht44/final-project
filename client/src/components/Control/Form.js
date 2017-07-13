import React, { Component } from 'react';
import Input from './Input';

import './Form.css'

class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {
      values: Array.apply(null, Array(this.props.legend.length)).map(Number.prototype.valueOf,0),
      legend: this.props.legend
    };
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange(ev) {
    const stateCopy = this.state.values.slice()
    stateCopy[ev.target.name] = parseFloat(ev.target.value)
    this.setState({values: stateCopy})
  }

  handleSubmit(ev) {
    const xhr = new XMLHttpRequest()
    let url = `http://localhost:8000/dash/${this.props.level}/${this.props.year}/?`;
    this.state.values.forEach((value, index) => {
      url = url + index + '=' + value + '&';
    })
    url += 'arg=tax';
    xhr.open('GET', url)
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          const parsed = JSON.parse(xhr.response)
          console.log(parsed);
          console.log(parsed['rel_unit_price']);
          this.props.relative(parsed['rel_unit_price']);
        }
      }
    }
    xhr.send()
    ev.preventDefault()
  }
  render() {
    console.log('current', this.props.current);
    const inputs = this.props.legend.map((item, i) =>
      <Input value={0} legend={item} key={i} name={i} handleChange={this.handleChange}/>
    )
    return (
      <form className="Form" onSubmit={this.handleSubmit}>
        {inputs}
        <input type="submit" />
      </form>
    )
  };
}

export default Form;
