import React, { Component } from 'react';
import './Display.css'
class Display extends Component {
  render() {
    return(
      <div className="Display">{this.props.values}</div>
    )
  }
}

export default Display;
