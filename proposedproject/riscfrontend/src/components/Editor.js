import React,{useState, useEffect} from "react";
import axios from "axios";
import { render } from "react-dom";
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-assembly_x86";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/theme-twilight";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";





const Editor = () => {
    const [theme, settheme] = useState("monokai")
    const [code, setcode] = useState("")
    const [resp, setresp] = useState({})

    function onChange(newValue) {
        setcode(newValue)
      }

   
    function onThemeChange(newval){
        settheme(newval.target.value)
    }


    const onclickhandler = (e) => { 
        const config = {
            headers: {
              'content-type': 'multipart/form-data'
            }
          }

        const formData = new FormData();
        formData.append("code" , code)


        axios.post("http://localhost:5000/postcode", formData, config)
        .then(response=>{
            console.log(response)
        })

    }



    return (
        <div>
            <AceEditor
                mode="assembly_x86"
                theme={theme}
                onChange={onChange}
                name="editordiv"
                editorProps={{ $blockScrolling: true }}
                style={{
                    height:"70vh",
                    width: "60vw"
                }}
            /> 

            

            <select class="form-select form-select-sm" aria-label=".form-select-sm example"
            style={{width : "100px"}} value = {theme} onChange= {onThemeChange} 
            >
            {/* <option selected>{theme}</option> */}
            <option value="monokai">Monokai</option>
            <option value="twilight">Twilight</option>
            <option value="github">Github</option>
            </select>


            <button type="button" class="btn btn-secondary" onClick={onclickhandler}>Run</button>


        </div>
    )
}

export default Editor
