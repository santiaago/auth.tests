import React, { Component } from 'react'
import logo from './logo.svg'
import './App.css'
import 'whatwg-fetch'

class App extends Component {

  constructor(props){
    super(props)
    this.state = {
      version: 'na',
      loggedIn: false,
      username: null,
      message: null,
    }
    this.fetchVersion = this.fetchVersion.bind(this)
    this.fetchUser = this.fetchUser.bind(this)
    this.fetchVersion()
    this.fetchUser()
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
      if(r.status === 200){
        return r.json()
      }
    })
    .then(json => {
      this.setState({version: json.version})
    })
    .catch(ex =>{
      console.error(ex)
    })
  }

  fetchUser = () => {
    fetch('/api/username', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    }).then(response => {
        if(response.status !== 200){
          this.setState({message: 'user not authenticated'})
          throw new Error('user not authenticated')
        } else {
          return response.json()
        }
    }).then(json => {
      this.setState({loggedIn: true, username: json.username })
    }).catch((ex) => {
      console.error(ex)
      this.setState({message: 'user authentication failed'})
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
          <h4 className="App-title">Version: {this.state.version}</h4>
          {this.state.username && <h4 className="App-title">User: {this.state.username}</h4>}
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        {this.state.loggedIn? null: <a href='/login/facebook'>login</a>}
      </div>
    )
  }
}

export default App
