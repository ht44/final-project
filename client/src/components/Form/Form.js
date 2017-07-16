import React, { Component } from 'react';
import './Form.css'

const formInit = {
  values: [],
  legend: [],
  value: '',
}

class Form extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.state = formInit;
  }

  handleChange(ev) {
    if (!Number.isNaN(parseFloat(ev.target.value))) {
      const stateCopy = this.state.values.slice()
      stateCopy[ev.target.name] = parseFloat(ev.target.value)
      this.setState({values: stateCopy})
    } else {
      const stateCopy = this.state.values.slice()
      stateCopy[ev.target.name] = 0;
      this.setState({values: stateCopy})
    }
  }


  handleSubmit(ev) {
    const xhr = new XMLHttpRequest()
    let url = `http://localhost:8000/dash/${this.props.level}/${this.props.year}/?`;
    this.state.values.forEach((value, index) => {
      if (value !== 0 && typeof value !== NaN ) {
        url = url + index + '=' + value + '&';
      }
    })

    if (url[url.length - 1] === '&') {
      url += 'arg=tax';
      xhr.open('GET', url)
      xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            const parsed = JSON.parse(xhr.response)

            if (parsed.hasOwnProperty('rel_unit_price')) {
              this.props.showRelative(parsed);
            }
          }
        }
      }
      console.log(url);
      xhr.send()
    } else {
      this.props.restore();
      console.log(url);
    }
    ev.preventDefault()
  }

  render() {
    console.log(this.state.values);
    const year = this.props.year
    const inputs = this.props.legend.map((item, i) =>
      <input
        className="Input"
        type="number"
        min="0"
        max="10"
        step="0.01"
        key={i}
        placeholder={item}
        name={i}
        onChange={this.handleChange}
      />
    )

    return (
      <form className="Form" key={year} onSubmit={this.handleSubmit}>
        {inputs}
        <input type="submit"/>
      </form>
    )
  };
}

export default Form;
