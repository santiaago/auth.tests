import React, { Component } from 'react'
import logo from './logo.svg'
import './App.css'
import 'whatwg-fetch'

class App extends Component {

  constructor(props){
    super(props)
    this.state = {version: 'na'}
    this.fetchVersion = this.fetchVersion.bind(this)
    this.fetchVersion()
  }

  fetchVersion(){
    fetch('/api/version', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    })
      .then(r => {
        if(r.status == 200)
        return r.json()
      })
      .then(json => {
        this.setState({version: json.version})
      })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
          <h4 className="App-title">Version: {this.state.version}</h4>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    )
  }
}

export default App
