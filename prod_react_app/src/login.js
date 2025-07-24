import React from 'react';
import {  MDBInput,
    MDBCol,
    MDBRow,
    MDBCheckbox,
    MDBBtn } from 'mdb-react-ui-kit';
import './login.css';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import { FaEye, FaEyeSlash } from 'react-icons/fa';


function Login() {
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()

    const navigate = useNavigate()

    const [showPassword, setShowPassword] = useState(false);
    const toggleShowPassword = () => {
      setShowPassword(!showPassword);
    };


const btnclick = (e) => {
    e.preventDefault();

    let bearerToken = null;

    let formData = new FormData();
 
        // Adding files to the formdata
        formData.append("username", username);
        formData.append("password", password);
 
        axios({
 
            // Endpoint to send files
            url: "http://127.0.0.1:1234/login/",
            method: "POST",
            headers: {
            },
 
            // Attaching the form data
            data: formData,
        })
 
            // Handle the response from backend here
            .then((res) => 
            
            { try {
                
                if (res.data.success === true) 
                { 
                    // Store the Bearer token
                    bearerToken = res.data.jwt_token;
                    localStorage.setItem('bearerToken', bearerToken);
                    navigate('/Dashboard')  
                }
                else 
                {
                    alert('Invalid Credentials')
                    return
                }
            } catch (error) {
                if (res.status === 403) {
                    alert('You are Blocked due to multiple invalid attempts, wait for one minute');
                }
            }
            
            })
            // Catch errors if any
            .catch((err) => { 
                if (err.response && err.response.status === 403) {
                    alert('You are Blocked due to multiple invalid attempts, wait for one minute');
                } else {
                }
            });  
    }

  return (

    <div className='login_page'>
        <form>
            <MDBRow className='row'>
            <MDBCol>
            </MDBCol>

            <MDBCol  className='login py px '>
                    <h4 style={{marginBottom:40}}>
                        Welcome To Productivity Dashboard
                    </h4>
                
            <MDBInput className='mb-4' type='text' id='user' label='User Name' onChange={(e)=>setUsername(e.target.value)} />
            {/* <MDBInput className='mb-4' type='password' id='pass' label='Password' onChange={(e)=>setPassword(e.target.value)}  /> */}
       
    <div className='password-input-container'>
        <MDBInput
        className='mb-4'
        type={showPassword ? 'text' : 'password'}
        id='pass'
        label='Password'
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        />
        <span onClick={toggleShowPassword} className='eye-icon' style={{ cursor: 'pointer' }}>
        {showPassword ? <FaEyeSlash /> : <FaEye />}
        </span>
    </div>


            <MDBBtn type='submit' block onClick={btnclick} >
                Sign in
            </MDBBtn>
            </MDBCol>

            <MDBCol>
            </MDBCol>

            </MDBRow>
        </form>
    </div>
    
  );
}

export default Login;


