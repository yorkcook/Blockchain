import React, {useState, useEffect} from 'react';
import axios from "axios"
import './App.css';

function App() {
  const [coinData, setCoinData] = useState()

  useEffect(()=>{
    axios
    .get("http://localhost:5000/chain")
    .then(res=>console.log(res))
    .catch(error=>console.log(error))
  }, [])  
  return (
    <div className="App">
      <h1>Hello from App</h1>
    </div>
  );
}

export default App;
