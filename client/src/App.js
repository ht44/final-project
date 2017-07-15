import './App.css';
// import Control from './components/Control/Control'
import React, { Component } from 'react';
import Controller from './components/Controller/Controller';
import { BrowserRouter as Router, Route, Redirect, Link, NavLink } from 'react-router-dom';

function aSyncXhr(level, year) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `http://localhost:8000/dash/${level}/${year}/`)
    xhr.onload = () => resolve(xhr.response)
    xhr.onerror = () => resolve(xhr.statusText)
    xhr.send();
  })
}


const Year = ({ match }) => {
  if (match.params.year) {
    return (
      <Controller level={match.params.level} year={match.params.year} />
    )
  } else {
    return (
      <Controller level={match.url.slice(1)} year={2015} />
    )
  }
}


const YearNav = ({ match }) => {
  const panels = [];
  for (let i = 1997; i < 2016; i++) {
    panels.push(
      <li key={i}>
        <NavLink to={`${match.url}/${i}`} activeClassName="router-selected">
          {i}
        </NavLink>
      </li>
    );
}
  return (
    <div className="App-List">
      <ul>

        <li><Link to="/">Home</Link></li>
        <li><Link to="/sector/2015">Sector</Link></li>
        <li><Link to="/summary/2015">Summary</Link></li>

        {panels}

      </ul>

      {/* <Route path="/:level/:year" component={Year}/> */}



    </div>
  )
}

const SiteRouter = ({ location }) => {
  console.log(location);
  return (
    <Router>
      <div className="App-List">
        <Route exact path="/" render={() => (
          <Redirect to='/sector/2015'/>
        )}/>
        {/* <Redirect from="/sector" to="sector/2015" /> */}
        {/* <Redirect from="/summary" to="summary/2015" /> */}
        <Route path="/:level" component={YearNav}/>
        <Route path="/:level/:year" component={Year}/>


      </div>
    </Router>
  )
}



class App extends Component {
  componentDidMount() {
    console.log('APPMOUNT -----------');

  }
  render() {
    return (
      <div className="App">
        <SiteRouter className="App" />
      </div>
    );
  }
}

export default App;
