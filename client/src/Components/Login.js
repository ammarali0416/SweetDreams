import React from 'react';
import './Login.css';

const Login = () => {
    const login_function = () =>{
        console.log('Something is happening!')
    };
return (
    <>
        <div className="login-page">
            <h1 style={{textAlign:"center"}}>Login</h1>
            <div className='form'>
                <form className='login-form'>
                   <input type='text' name='' id='' placeholder='username'/>
                   <input type='password' name='' id='' placeholder='password'/> 
                    <button>Login</button>
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