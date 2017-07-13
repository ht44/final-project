import React, { Component } from 'react';
import './Input.css'

class Input extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    return (
      <input
        type="Number"
        className="Input"
        min="0"
        max="5"
        step="0.01"
        name=""
      />
    )
  };
}

export default Input;
