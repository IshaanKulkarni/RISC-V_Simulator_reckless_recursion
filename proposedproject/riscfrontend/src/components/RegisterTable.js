import React,{useState, useEffect} from 'react'




const RegisterTable = (props) => {
    const [radix, setradix] = useState("10")
    
    
    // function onChangeradix(val){

    //     console.log(val)
    //     console.log(radix)
    //     setradix(val.target.value)
        
    // }

    const onChangeradix = e => {
        const target = e.target;
        if (target.checked) {
          setradix(target.value);
        }

        console.log(radix)
     }
    const [registervalues, setregistervalues] = useState({
                                                    part1 : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                                    part2 : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                                                    }   
                                                )
    return (
        <div className="row" style = {{padding: 0, margin : 0}}>
            
            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
                <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autoComplete="off"  value="2" checked = {radix === 2} onChange={onChangeradix}  />
                <label class="btn btn-outline-secondary" for="btnradio1">Binary</label>

                <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autoComplete="off"  value = "10" checked = {radix === 10} onChange={onChangeradix} />
                <label class="btn btn-outline-secondary" for="btnradio2">Decimal</label>

                <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autoComplete="off"  value = "16" checked = {radix === 16} onChange={onChangeradix} />
                <label class="btn btn-outline-secondary" for="btnradio3">Hex</label>
              </div>



            {/* set of first 16 registers */}
            <div className="col-md-6" style = {{padding : "2px"}}>
                <table className={props.dark ? "table table-dark" : "table table-dark"}>
                    <thead>
                        <tr>
                            <th scope="col">Reg</th>
                            <th scope="col">Value</th>
                        </tr>
                    </thead>
                        <tbody>


                    {
                        registervalues.part1.map(function( ele , idx){
                            console.log(idx, ele);
                            return <tr> <th scope="row">{idx}</th> <td>{ele }</td> </tr>    
                        })
                    }
                        
                        
                    </tbody>
                </table>
            </div>

            {/* set of second set of 16 registers */}
            <div className="col-md-6" style={{padding : "2px"}}>
            <table class={props.dark ? "table table-dark" : "table table-dark"}>
                    <thead>
                        <tr>
                            <th scope="col">Reg</th>
                            <th scope="col">Value</th>
                        </tr>
                    </thead>
                        <tbody>


                    {
                        registervalues.part2.map(function( ele , idx){
                            // console.log(idx, ele);
                            return <tr> <th scope="row">{idx+16}</th> <td>{ele }</td> </tr>    
                        })
                    }
                        
                        
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default RegisterTable
