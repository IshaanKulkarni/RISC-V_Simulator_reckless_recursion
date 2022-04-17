import React, { useState, useEffect } from "react";
import DarkModeToggle from "react-dark-mode-toggle";

export default function Togglemode(props){
  // const [isDarkMode, setIsDarkMode] = useState(() => false);


  useEffect(() => {
    localStorage.setItem("Mode", JSON.stringify(props.mode))
  }, [props.mode]);

  

  const Togglemode = () => {
    if (props.mode === true) {
      document.body.style.backgroundColor = "white"
      props.setMode(() => false)
    }
    else {
      document.body.style.backgroundColor = "#1c1c1c"
      document.body.style.color = "white"
      props.setMode(() => true)
    }
  }



  return (
    <DarkModeToggle
      onChange={Togglemode}
      checked={props.dark}
      size={80}
    />
  );
};