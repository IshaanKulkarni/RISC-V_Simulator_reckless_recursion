import React from 'react'
import ToggleMode from './ToggleMode'
const Navbar = (props) => {
    return (
        <div>
            <nav class={props.mode ? "navbar navbar-expand-lg navbar-dark bg-dark" : "navbar navbar-expand-lg navbar-light bg-light"}>
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">Navbar</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item">
                                <a class="nav-link active" aria-current="page" href="#">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#">Link</a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link disabled">Disabled</a>
                            </li>



                            {/* <li className="nav-item">
                            <ToggleMode dark={props.dark} Togglemode={props.Togglemode} setMode = {props.setMode}></ToggleMode>
                            
                            </li> */}
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    )
}

export default Navbar
