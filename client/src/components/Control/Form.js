import React, { Component } from 'react';
import Input from './Input';

import './Input.css'

class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange(ev) {
    this.setState({value: ev.target.value})
  }

  handleSubmit(ev) {
    const xhr = new XMLHttpRequest()
    const url = `http://localhost:8000/dash/${this.props.level}/${this.props.year}/?${'0'}=${this.state.value}&${'1'}=${this.state.value}&${'2'}=${this.state.value}&arg=tax`
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
    return (
      <form className="Form" onSubmit={this.handleSubmit}>
        <label>
          Num:
          <input type="number" min="0" max="5" step="0.01" value={this.state.value} onChange={this.handleChange}/>
        </label>
        <input type="submit" value="Submit"/>
      </form>
    )
  };
}

export default Form;
