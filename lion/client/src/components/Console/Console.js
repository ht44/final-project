import React, { Component } from 'react';
import './Console.css'
class Console extends Component {
  render() {
    return(
      <div className="Console">{this.props.display}</div>
    )
  }
}

export default Console;
