import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login/Login';
import SweetDreams from './Components/SweetDreams/SweetDreams'; 
//import Dashboard from './Components/App'; 
//import ErrorPage from './Components/ErrorPage'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/login' element={<Login />} />
        <Route path='/SweetDreams' element={<SweetDreams />} /> 
        {/*<Route path='*' element={<ErrorPage />} />*/}
      </Routes>
    </Router>
  );
}

export default App;
