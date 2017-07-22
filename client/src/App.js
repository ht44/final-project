// import './normalize.css';
import './App.css';
import logo from './logo.svg';
import React, { Component } from 'react';
import Controller from './components/Controller/Controller';
import { BrowserRouter as Router, Route, Link, NavLink } from 'react-router-dom';

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
        <li><NavLink to="/summary" activeClassName="router-selected">Summary</NavLink></li>
        <li><NavLink to="/sector" activeClassName="router-selected">Sector</NavLink></li>
        {panels}
      </ul>
    </div>
  )
}

const SiteRouter = ({ location }) => {
  console.log(location);
  return (
    <Router>
      <div className="App-List">
        <Route exact path="/" render={() => (
          <div className="App-List">
            <ul>
              <li><NavLink to="/" activeClassName="router-selected">Home</NavLink></li>
              <li><NavLink to="/summary" activeClassName="router-selected">Summary</NavLink></li>
              <li><NavLink to="/sector" activeClassName="router-selected">Sector</NavLink></li>
            </ul>
          </div>
        )}/>
        <Route path="/:level" component={YearNav}/>
        <img src={logo} className="App-logo" alt="logo" />
        <Route path="/:level/:year" component={Year}/>
      </div>
    </Router>
  )
}



class App extends Component {
  render() {
    return (
      <div className="App">
        <SiteRouter className="App" />
      </div>
    );
  }
}

export default App;
