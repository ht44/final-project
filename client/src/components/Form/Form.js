import React, { Component } from 'react';
import ReactDOM from 'react-dom';
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
    this.focus = this.focus.bind(this)
    this.state = formInit;
  }


  componentDidMount() {
    // let x = ReactDOM.findDOMNode(this.refs[this.props.current])
    // x.focus();
  }

  componentDidUpdate(prevProps, nextProps) {
    console.log(this.props.current);
    let x = ReactDOM.findDOMNode(this.refs[this.props.current])
    x.focus();
  }
  componentWillReceiveProps(prevProps, nextProps) {
    // console.log(nextProps);
    // // console.log(ReactDOM.findDOMNode(this.refs[]));
    // let x = ReactDOM.findDOMNode(this.refs[this.props.current])
    // console.log(x);
    // x.focus();
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
      if (value !== 0) {
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

  focus(ev) {
    let newNum = parseInt(ev.target.name, 10);
    this.props.changeCurrent(newNum);
  }


  render() {
    const year = this.props.year
    const inputs = this.props.legend.map((item, i) =>
      <input
        ref={i}
        className="Input"
        type="number"
        min="0"
        max="10"
        step="0.01"
        key={i}
        placeholder={item}
        name={i}
        onChange={this.handleChange}
        onFocus={(ev) => this.focus(ev)}
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
