import React, { Component } from 'react';
import Control from '../Control/Control';
import Form from '../Control/Form';
import Toggle from '../Toggle/Toggle';
import Display from '../Display/Display'
import './Panel.css'

class Panel extends Component {
  constructor(props) {
    super(props);
    this.xhRequest = this.xhRequest.bind(this);
    this.changeLevel = this.changeLevel.bind(this);
    this.state = {
      values: '',
      level: 'sector',
      year: '2015'
    };
  }

  changeLevel(){
    this.setState((prevState, props) => {
      if (prevState.level === 'sector') {
        return {level: 'summary'}
      } else {
        return {level: 'sector'}
      }
    })
  }

  xhRequest(level, year, handler) {
    const xhr = new XMLHttpRequest();
    const url = `http://localhost:8000/dash/${level}/${year}/`
    xhr.open('GET', url)
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          handler(xhr.response)
        }
      }
    }
    xhr.send()
  }

  render() {
    const level = this.state.level
    const year = this.state.year
    const legend = this.props.legend
    return (
      <div className="Panel">
        <Display>
          <Form current={this.props.current} level={level} year={year} relative={this.props.relative} legend={legend}/>
        </Display>
          <Toggle level={level} onClick={this.changeLevel}/>
        <Control level={level} year='1997' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='1998' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='1999' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2000' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2001' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2002' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2003' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2004' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2005' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2006' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2007' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2008' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2009' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2010' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2011' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2012' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2013' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2014' onClick={this.xhRequest} handler={this.props.populate} />
        <Control level={level} year='2015' onClick={this.xhRequest} handler={this.props.populate} />
      </div>
    )
  };
}

export default Panel;
