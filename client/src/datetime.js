import  React, { useState , useEffect } from 'react'

const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
};

export const DateTime = () => {

    var [date,setDate] = useState(new Date());
    
    useEffect(() => {
        var timer = setInterval(()=>setDate(new Date()), 1000 )
        return function cleanup() {
            clearInterval(timer)
        }
    
    });

    return(
        <div>
            
            <p className='date'> {date.toLocaleDateString('id-ID', options)}</p>
            <p className='time'> {date.toLocaleTimeString()}</p>
            

        </div>
    )
}

export default DateTime