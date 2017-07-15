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

  componentDidMount() {
    // this.reset()

    console.log('FORM MOUNTEEEEEEE');

  }

  componentDidUpdate(nextProps) {
    console.log('UPDATEEEEEE');
    // this.setState({values: nextProps.zeros})

  }
  //
  componentWillReceiveProps(nextProps) {
    // this.setState({values: nextProps.zeros})
  }



  handleChange(ev) {
    const stateCopy = this.state.values.slice()
    stateCopy[ev.target.name] = parseFloat(ev.target.value)
    this.setState({values: stateCopy})
  }

  reset() {
    this.setState({values: this.props.zeros});
  }

  handleSubmit(ev) {
    const xhr = new XMLHttpRequest()
    let url = `http://localhost:8000/dash/${this.props.level}/${this.props.year}/?`;
    this.state.values.forEach((value, index) => {
      if (value !== 0) {
        url = url + index + '=' + value + '&';
      }
    })

    url += 'arg=tax';
    console.log(url);
    xhr.open('GET', url)
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          const parsed = JSON.parse(xhr.response)
          this.props.model(parsed);
        }
      }
    }
    xhr.send()
    ev.preventDefault()
}
  render() {
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
