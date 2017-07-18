import React, { Component } from 'react';
import './Button.css'
class Button extends Component {
  constructor(props) {
    super()
  }
  render() {
    return(
      <button className="Button" type="button" onClick={this.props.handleClick}>
        {this.props.value}
      </button>
    )
  }
}

export default Button;
