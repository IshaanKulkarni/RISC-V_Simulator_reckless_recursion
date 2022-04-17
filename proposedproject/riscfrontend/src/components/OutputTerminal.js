import React from 'react'
import Terminal from 'terminal-in-react';


const OutputTerminal = () => {
    return (
        <div
        style={{
            height: "20vh",
            marginTop:"20px"
          }}
        >
        
        <textarea readOnly
        style={{
            width:"60vw",
            height:"30px",
            backgroundColor: "#0d0c0ce0",
            color:"grey"
        }}
        >
             Console
            
        </textarea>    
        <textarea readOnly
        style={{
            width:"60vw",
            height:"20vh",
            backgroundColor: "#0d0c0ce0",
            color:"grey"
        }}

        >
            hello this is soham
            
            
        </textarea>


       </div>
    )
}

export default OutputTerminal
