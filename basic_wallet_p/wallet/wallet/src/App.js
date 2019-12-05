import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [coinData, setCoinData] = useState();
  const test =
    /[a-z\d]{1, 12}$/i /
    useEffect(() => {
      axios
        .get("http://localhost:5000/chain")
        .then(
          res => setCoinData(res.data.chain)
          // console.log("res", res.data.chain),
          // console.log("coindata", coinData)
        )
        .catch(error => console.log(error));
    }, []);

  const [userInput, setUserInput] = useState();
  const onChangeHandler = e => {
    setUserInput(e.target.value);
    console.log("user input", userInput);
  };

  return (
    <div className="App">
      <h1>Hello from App</h1>
      {/* {console.log("coindata2", coinData)} */}
      <form>
        <div className="group">
          <input
            type="name"
            name="name"
            placeholder="Enter a name"
            onChange={onChangeHandler}
          />
        </div>

        {/* <button type="submit">Finish Registration</button> */}
      </form>
      {/* Check if coinData has been populated with data yet */}
      {coinData ? (
        coinData.map(x => (
          <>
            {x.transactions.map(y => (
              <>
              {/* Check if user input is equal to the data from the backend */}
                {userInput === y.recipient ? (
                  <>
                    <h3>From: {y.sender}</h3>
                    <h3>To: {y.recipient}</h3>
                    <h3>Sent Amount: {y.amount}</h3>
                    <h3>Total Amount: {y.amount += y.amount}</h3>
                  </>
                ) : (
                  <h2>Not for your eyes</h2>
                )}
              </>
            ))}
          </>
        ))
      ) : (
        <h2>Loading, please wait</h2>
      )}
    </div>
  );
}

export default App;
