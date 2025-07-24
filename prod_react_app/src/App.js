// // src/App.js
// import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route,Navigate } from 'react-router-dom';
import Login from './login';
import Dashboard from './dashboard'
// import Carecloudtable from './carecloud/carecloud.js'

 
function App() {
 
  return (
<Router>
<Routes>
        {/* Redirect from "/" to "/login" */}
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/Dashboard" element={<Dashboard />} />

</Routes>
</Router>
  );
}
 
export default App;



