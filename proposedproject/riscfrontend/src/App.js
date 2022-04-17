import React, { useState, useEffect } from "react";
import DarkModeToggle from "react-dark-mode-toggle";
import './App.css';
import Navbar from './components/Navbar';
import RegisterTable from './components/RegisterTable';
import Sidebar from './components/Sidebar';
import Editor from './components/Editor';
import OutputTerminal from './components/OutputTerminal';


function App() {

  const getMode = () => {
    if(localStorage.getItem("Mode") != "undefined"){
      if(JSON.parse(localStorage.getItem("Mode")) == "true"){
        document.style.backgroundColor = "#1c1c1c"
      }
       return JSON.parse(localStorage.getItem("Mode"))
    }
    
    document.style.backgroundColor = "#1c1c1c"
    return true
  }

  const [mode, setMode] = useState(getMode)  // whether dark or not

  useEffect(() => {
    localStorage.setItem("Mode", JSON.stringify(mode))
  }, [mode]);


  const Togglemode = () => {
    if (mode === true) {
      document.body.style.backgroundColor = "white"
      document.body.style.color = "black"
      setMode(() => false)
    }
    else {
      document.body.style.backgroundColor = "#1c1c1c"
      document.body.style.color = "white"
      setMode(() => true)
    }
  }

  return (
    <div className="App">

      <Sidebar pageWrapId={'page-wrap'} outerContainerId={'outer-container'} />
      <Navbar mode={mode} Togglemode={Togglemode} setMode={setMode}/>
      <div className="d-flex flex-row-reverse bd-highlight">
          <DarkModeToggle
          onChange={Togglemode}
          checked={mode}
          size={80}

        />
      </div>
      

      <div className="container">
        <div className="row" style={{ height: "70vh" }}>
          <div className="col-md-4">
            <RegisterTable mode={mode} Togglemode={Togglemode}/>
          </div>

          <div className="col-md-8" id="editordiv">
            <Editor />
          </div>
        </div>
        <div className="container my-5" >
          <div className="row">
            <div className="col-md-4">
              <div className="container">





              </div>
              </div>

                  <div className="col-md-8" style={{ marginTop: "10px", height: "20vh" }}>
                    <OutputTerminal />
                  </div>
                </div>
              </div>



            </div>
          </div>
  );
}

export default App;
