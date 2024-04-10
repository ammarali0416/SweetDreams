import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
    const navigate = useNavigate();

    const login_function = () =>{
        console.log('Something is happening!')
        navigate('/SweetDreams');
    };
return (
    <>
        <div className="login-page">
            <h1 style={{textAlign:"center"}}>Login</h1>
            <div className='form'>
                <form className='login-form'>
                   <input type='username_input' name='' id='' placeholder='username'/>
                   <input type='password_input' name='' id='' placeholder='password'/> 
                    <button className='login-sweetdreams' onClick={login_function}>
                        Login
                    </button>
                    <p className='message'>Not registered? <a href='#'>Create an account</a></p>
                </form>
                <button className='login-with-google-btn' onClick={login_function}>
                    Login with Google
                </button>
                <button className= 'login-with-microsoft-btn' onClick={login_function}>
                    Login with Microsoft
                </button>
                <button className= 'login-with-apple-btn' onClick={login_function}>
                    Login with Apple
                </button>
            </div>
        </div>
    </>
  );
};

export default Login;