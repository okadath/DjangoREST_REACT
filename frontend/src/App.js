import React, { Component } from 'react';
import axios from 'axios';
class App extends Component{
  state={
    todos:[]
  };
  componentDidMount(){
    this.getTodos();
  }
  getTodos(){
    axios
    .get('http://127.0.0.1:8000/api/')
    .then(res=>{
      this.setState({todos:res.data});
    })
    .catch(err=>{
      console.log(err);
    });
  }
  render(){
    return(
      <div>
      {
        this.state.todos.map(item=>(
          <div key={item.id}>
          <h1>{item.title}</h1>
          <span>{item.body}</span>
          </div>
          ))}
        </div>
    );
  }
}
export default App;

// =======nuestra app estatica
// import React, { Component } from 'react';
// const list=[
//   {"id":1,
//   "title":"1rt todo",
//   "description":"asdasdasd"
//   },
//   {"id":2,
//   "title":"2nd todo asd",
//   "description":"qweqweqwe"
//   },
// ]

// class App extends Component{
//   constructor(props) {
//     super(props);
  
//     this.state = {list};
//   }
//   render(){
//     return(
//       <div>
//       {
//         this.state.list.map(item=>(
//           <div key={item.id}>
//           <h1>{item.title}</h1>
//           </div>
//           ))}
//         </div>
//     );
//   }
// }
// export default App;

// import logo from './logo.svg';
// import './App.css';

// class App extends Component {
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <p>
//             Edit <code>src/App.js</code> and save to reload.
//           </p>
//           <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Learn React
//           </a>
//         </header>
//       </div>
//     );
//   }
// }

// export default App;
