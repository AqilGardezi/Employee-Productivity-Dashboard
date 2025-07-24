import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './dashboard.css';
import { CSVLink } from 'react-csv';
import * as XLSX from 'xlsx';
import Loader from './Loader';
import axios from "axios";



// import Carecloudtable from './carecloud/carecloud';
import {  MDBInput,
    MDBCol,
    MDBRow,
    MDBCheckbox,
    MDBBtn } from 'mdb-react-ui-kit';

import {
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBCardSubTitle,
    MDBCardText,
    MDBCardLink
  } from 'mdb-react-ui-kit';
  


// function Dashboard() 
function Dashboard() {


  const [director,setDirector] = useState('All')
  const [timespan,setTimespan] = useState('1')
  const [performance,setPerformance] = useState('1')
  const [ptype,setPtype] = useState('1')

  const [CCData,setCCData] = useState([])
  const [MISData,setMISData] = useState([])
  const [FOXData,setFOXData] = useState([])
  const [GPData,setGPData] = useState([])

  const [ccbit,setCCBit] = useState(false)
  const [foxbit,setFoxBit] = useState(false) 
  const [misbit,setMisBit] = useState(false)
  const [gpbit,setGPBit] = useState(false) 

  const [isLoading, setIsLoading] = useState(false);


  const navigatee = useNavigate()

  const [activeContainer, setActiveContainer] = useState(null);

  const [directordata,setDirectorData] = useState([])

  // Retrieve the bearer token from localStorage
  const bearerToken = localStorage.getItem('bearerToken');

  // debugger

const getDirectorData = () => {
  if (! bearerToken)
  {
    navigatee('/login');
  }

  axios({
    url: "http://127.0.0.1:1234/direct/",
    method: "GET",
    headers: {
        // Include any headers you need, such as Authorization
        'Authorization': `Bearer ${bearerToken}`,
    },
  })
    .then(response => {

      if (response.status === 401) {
        navigatee('/login');
      }

      // If the response.data is a string, parse it into an object
      const parsedData = typeof response.data === 'string' ? JSON.parse(response.data) : response.data;

      setDirectorData(parsedData);
    })
    .catch(error => {
      navigatee('/login');
    });
};

useEffect(() => {
  // Fetch data from your API or perform any other actions on page reload
  getDirectorData();
  ccdata()
}, []);

const btn_click = (e) => 
{
  if (ptype == '1'){
    ccdata(e)
  }
  if (ptype == '2'){
    foxdata(e)
  }
  if (ptype == '3'){
    misdata(e)
  }
  if (ptype == '4'){
    gpdata(e)
  }

}


const ccdata = (e) =>
{
  setIsLoading(true);
  if (e) {
    e.preventDefault()
  }
  
  setActiveContainer('cc');

  setCCBit(true);
  setFoxBit(false);
  setMisBit(false);
  setGPBit(false);
  let formData = new FormData();
        // Adding files to the formdata
        formData.append('weeksbefore',timespan);
        formData.append('director',director);
        formData.append('performance',performance);

  axios({
 
    // Endpoint to send files
    url: "http://127.0.0.1:1234/carecloud/",
    method: "POST",
    headers: {
        // Include the bearer token in the Authorization header
        'Authorization': `Bearer ${bearerToken}`,
    },

    data: formData,
})
.then(response => {


  if (typeof(response.data) == 'string')
  {

    setCCData(JSON.parse(response.data))  
    
  }
  else
  {

    setCCData(response.data)
  }

})
.catch(error => {
  navigatee('/login');
})

.finally(() => {
  setIsLoading(false);
});
}


const foxdata = () => {
  setIsLoading(true);
  setCCBit(false);
  setFoxBit(true);
  setMisBit(false);
  setGPBit(false);

  let formData = new FormData();
  formData.append('weeksbefore', timespan);
  formData.append('director', director);
  formData.append('performance', performance);

  axios({
    url: 'http://127.0.0.1:1234/fox/',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${bearerToken}`,
    },
    data: formData,
  })
    .then((response) => {
      console.log('Raw FOX Data Response:', response.data);
      setFOXData(response.data) })
    //   try {
    //     let data = response.data;
      
    //     if (typeof data === 'string') {
    //       data = data.replace(/NaN/g, 'null'); // Replacing 'NaN' with 'null'
    //     }
    //     let parsedData = JSON.parse(data);

    //     if (Array.isArray(parsedData)) {
    //       console.log('Data inside response:', parsedData);
    //       setFOXData(parsedData); 
    //     } else {
    //       console.error('Parsed data is not an array:', parsedData);
    //       setFOXData([]); 
    //     }
    //   } catch (error) {
    //     console.error('Error parsing FOX data:', error);
    //     setFOXData([]); 
    //   }
    // })
    .catch((error) => {
      console.error('Error fetching FOX data:', error);
      navigatee('/login');
      setFOXData([]); 
    })
    .finally(() => {
      setIsLoading(false);
    });
};

const misdata = (e) =>
{
  setIsLoading(true);
  e.preventDefault()
  setActiveContainer('mis');

  setFoxBit(false)
  setCCBit(false)
  setMisBit(true);
  setGPBit(false);
  let formData = new FormData();
        // Adding files to the formdata
        formData.append('weeksbefore',timespan);
        formData.append('director',director);
        formData.append('performance',performance);

  axios({
 
    // Endpoint to send files
    url: "http://127.0.0.1:1234/mis/",
    method: "POST",
    headers: {
        // Include the bearer token in the Authorization header
        'Authorization': `Bearer ${bearerToken}`,
    },

    data: formData,
})
.then(response => {
  setMISData(response.data);

})
.catch(error => {

  navigatee('/login');
})
.finally(() => {
  setIsLoading(false);
});
}


const gpdata = (e) =>
{
  setIsLoading(true);
  e.preventDefault()
  setActiveContainer('gp');

  setFoxBit(false)
  setCCBit(false)
  setMisBit(false);
  setGPBit(true);
  let formData = new FormData();
        // Adding files to the formdata
        formData.append('weeksbefore',timespan);
        formData.append('director',director);
        formData.append('performance',performance);

  axios({
 
    url: "http://127.0.0.1:1234/globalportal/",
    method: "POST",
    headers: {
        // Include the bearer token in the Authorization header
        'Authorization': `Bearer ${bearerToken}`,
    },

    data: formData,
})
.then(response => {
  if (typeof(response.data) == 'string')
  {
    setGPData(JSON.parse(response.data))
 
  }
  else
  {
    setGPData(response.data)
  }

})
.catch(error => {
  navigatee('/login');

})
.finally(() => {
  setIsLoading(false);
});

}


const CCExport = ({ CCData }) => {
    const exportToExcel = () => {
      const ws = XLSX.utils.json_to_sheet(CCData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'CCData');
      XLSX.writeFile(wb, 'CCData.xlsx');
    };

    return (
      <button className="btn btn-sm btn-success" onClick={exportToExcel}>
        Export
      </button>
    );
};



const FoxExport = ({ FOXData }) => {
    const exportToExcel = () => {
      const ws = XLSX.utils.json_to_sheet(FOXData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'FOXData');
      XLSX.writeFile(wb, 'FOXData.xlsx');
    };

  return (
    <button className="btn btn-sm btn-success" onClick={exportToExcel}>
      Export
    </button>
  );
};

const MIXExport = ({ MISData }) => {
    const exportToExcel = () => {
      const ws = XLSX.utils.json_to_sheet(MISData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'MISData');
      XLSX.writeFile(wb, 'MISData.xlsx');
    };

  return (
    <button className="btn btn-sm btn-success" onClick={exportToExcel}>
      Export
    </button>
);
};


const GPExport = ({ GPData }) => {
    const exportToExcel = () => {
      const ws = XLSX.utils.json_to_sheet(GPData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'GPData');
      XLSX.writeFile(wb, 'GPData.xlsx');
    };

  return (
    <button className="btn btn-sm btn-success" onClick={exportToExcel}>
      Export
    </button>
);
};


const logout = (e) => {
  localStorage.removeItem('bearerToken')
  navigatee('/login')
}
 

    return (

        <div className='div'>

        <MDBRow className='headrow'>
            <MDBCol md='10' className='text-center '>
            <h2 className='head'>
                EMPLOYEE PRODUCTIVITY DASHBOARD
                </h2>
            </MDBCol>
       <MDBCol md='2' className='btn_logout d-flex justify-content-end'>
        <MDBBtn onClick={logout}>Logout</MDBBtn>
       </MDBCol>   
        </MDBRow>
        <div>

        <MDBRow className='row_select'>

          <MDBCol md='3'>
              <label htmlFor="director">Select Portal</label>
              <select className="form-select" id="timespan" aria-label="Default select example" onChange={(e)=>setPtype(e.target.value)}>
                  {/* <option selected>Select Time Span</option> */}
                  <option value="1">CARE CLOUD</option>
                  <option value="2">FOX PORTAL</option>
                  <option value="3">MIS PORTAL</option>
                  <option value="4">GLOBAL PORTAL</option>
              </select>
            </MDBCol>

            <MDBCol md='3'>
                <label htmlFor="director">Select Director</label>
                <select className="form-select" id="director" aria-label="Select Director" onChange={(e)=>setDirector(e.target.value)}>
                  <option value="All">All</option>
                  {directordata.map((director, index) => (
                    <option key={index} value={director.EMPLOYEE_NAME}>
                      {director.EMPLOYEE_NAME}
                    </option>
                    ))}
                  
                </select>
              </MDBCol>

                <MDBCol md='3'>
                <label htmlFor="director">Select Time Span</label>
                <select className="form-select" id="timespan" aria-label="Default select example" onChange={(e)=>setTimespan(e.target.value)}>
                    {/* <option selected>Select Time Span</option> */}
                    <option value="1">Current Week</option>
                    <option value="2">Previous Week</option>
                    <option value="3">Two Weeks Earlier</option>
                </select>
                </MDBCol>

                <MDBCol md='2'>
                <label htmlFor="director">Select Performance</label>
                <select className="form-select" id="perform" aria-label="Default select example" onChange={(e)=>setPerformance(e.target.value)}>
                    {/* <option selected>Select Time Span</option> */}
                    <option value="1">All</option>
                    <option value="2">Top Performer</option>
                    <option value="3">Low Performer</option>
                </select>
                </MDBCol>

          <MDBCol md='1' className='d-flex justify-content-end'>
                    <MDBBtn className='btn btn-success' style={{ height: '40px', marginTop: '25px'}} onClick = {btn_click}>
                      Search
                    </MDBBtn>
          </MDBCol>

            </MDBRow>
        </div>

{ccbit && (
  <div>
    <MDBRow className="pb-0 heading rounded-3">
        <MDBCol md="10" className="pt-2">
          <h5>Care Cloud</h5>
        </MDBCol>
        <MDBCol md="2" className="pt-1 pb-1 d-flex justify-content-end">
          <CCExport CCData={CCData} />
        </MDBCol>
      </MDBRow>
    </div>
    )}

{foxbit && (
  <div>
    <MDBRow className="pb-0 heading rounded-3">
        <MDBCol md="10" className="pt-2">
          <h5>Fox Portal</h5>
        </MDBCol>
        <MDBCol md="2" className="pt-1 pb-1 d-flex justify-content-end">
          <FoxExport FOXData={FOXData} />
        </MDBCol>
      </MDBRow>
    </div>
    )}


{misbit && (
  <div>
    <MDBRow className="pb-0 heading rounded-3">
        <MDBCol md="10" className="pt-2">
          <h5>MIS Portal</h5>
        </MDBCol>
        <MDBCol md="2" className="pt-1 pb-1 d-flex justify-content-end">
          <MIXExport MISData={MISData} />
        </MDBCol>
      </MDBRow>
    </div>
    )}


{gpbit && (
  <div>
    <MDBRow className="pb-0 heading rounded-3">
        <MDBCol md="10" className="pt-2">
          <h5>Global Portal</h5>
        </MDBCol>
        <MDBCol md="2" className="pt-1 pb-1 d-flex justify-content-end">
          <GPExport GPData={GPData} />
        </MDBCol>
      </MDBRow>
    </div>
    )}

      <MDBRow>
       
  <div id = 'tabledisplay' className='scroll card'>


{ ccbit? 
        <table className='tableStyle'>
        <thead className='column'>
          <tr>
          <th>No</th>
           <th>EmpID</th>
           <th>EmpName</th>
           <th>Lead </th>
           <th>ADO </th>
           <th>DO </th>
           <th>DSProd</th>
           <th>GPProd</th>
           <th>OldRVUScore</th>
           <th>CalculatedRVUScore</th>
           <th>Total</th>
           <th>Pending</th>
           <th>Paid</th>
           <th>PreviouslyPaid</th>
           <th>TotalRejections</th>
           <th>TotalDenials</th>
           <th>CorrectPayments</th>
           <th>IncorrectPayments</th>
          </tr>
        </thead>
        <tbody>
         
        {Array.isArray(CCData) && CCData.map((item, index) => (
                              <tr key={index} className={index % 2 === 0 ? 'evenRow' : 'oddRow'}>
                                  <td>{index + 1}</td>
                                  <td>{item.EMPLOYEEID}</td>
                                  <td>{item.Employee_Name}</td>
                                  <td>{item.Lead}</td>
                                  <td>{item.ADO}</td>
                                  <td>{item.DO}</td>
                                  <td>{item.DSProd}</td>
                                  <td>{item.GPProd}</td>
                                  <td>{item.Old_RVU_Score}</td>
                                  {/* <td>{Number(item.Old_RVU_Score).toLocaleString()}</td> */}
                                  <td>{item.Calculated_RVU_Score}</td>
                                  <td>{item.Total}</td>
                                  <td>{item.Pending}</td>
                                  <td>{item.Paid}</td>
                                  <td>{item.Previously_Paid}</td>
                                  <td>{item.Total_Rejections}</td>
                                  <td>{item.Total_Denials}</td>
                                  <td>{item.Correct_Payments}</td>
                                  <td>{item.Incorrect_Payments}</td>
                              </tr>
                          ))}
        </tbody>
      </table>
     :''
    }


{/* Fox Data Table */}
<p>{foxbit}</p>
{ foxbit ? 
        <table className='tableStyle'>
        <thead className='column'>
          <tr>
           <th>No</th>
           <th>EmpID</th>
           <th>EmpName</th>
           <th>Lead</th>
           <th>ADO</th>
           <th>DO</th>
           <th>DSProd</th>
           <th>GPProd</th>
           <th>WorkHoursWeek</th>
           <th>WorkHoursPerDay</th>
           <th>ClaimsSum</th>
           <th>Index</th>
           <th>I.Time(8)</th>
           <th>Invoice</th>
           <th>I.Time(30)</th>
           <th>IVTeam</th>
           <th>I.Time(12)</th>
           <th>OPPHY</th>
           <th>O.Time(10)</th>
           <th>OPAUD</th>
           <th>OP.Time(13)</th>
           <th>Authorization</th>
           <th>A.Time(15)</th>
           <th>POC</th>
           <th>P.Time(5)</th>
           <th>Referral</th>
           <th>R.Time(11)</th>
           <th>O3COI</th>
           <th>O.Time(25)</th>
           <th>Audit</th>
           <th>IA.Time(5)</th>
           <th>Refund</th>
           <th>Rf.Time(15)</th>
           <th>OtherTasks</th>
           <th>OT.Time(5)</th>
           <th>Demo</th>
           <th>D.Time(5)</th>
           <th>Bills</th>
           <th>B.Time(5)</th>
           <th>Payment</th>
           <th>P.Time(2)</th>
           <th>FollowUP</th>
           <th>F.Time(8)</th>
           <th>Denial</th>
           <th>D.Time(7)</th>
           <th>Tickets</th>
           <th>T.Time(5)</th>
           <th>Rejection</th>
           <th>E.Time(3)</th>
           <th>Appeals</th>
           <th>A.Time(5)</th>
           <th>UrgentReferral</th>
           <th>U.Time(15)</th>
           <th>BillCorrect</th>
           <th>B.Time(25)</th>
           <th>F_Ticks</th>
           <th>F.Time(2)</th>
          </tr>
        </thead>
        <tbody>
        {Array.isArray(FOXData) && FOXData.map((item, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'evenRow' : 'oddRow'}>
                      <td>{index + 1}</td>
                      <td>{item.EmpID}</td>
                      <td>{item.EmpName}</td>
                      <td>{item.Lead}</td>
                      <td>{item.ADO}</td>
                      <td>{item.DO}</td>
                      <td>{item.DSProd}</td>
                      <td>{item.GPProd}</td>
                      <td>{item.WorkHoursWeek}</td>
                      <td style={{backgroundColor: item.AdjustedSum >= 10 ? '#2da0bd' : item.AdjustedSum <=6 ? '#f13939' : '#bcc7ac',
                                          color: 'black'}}>{item.AdjustedSum}</td>
                      
                      <td>{item.ClaimsSum}</td>
                      <td>{item.Index}</td>
                      <td className='timecolumn'>{item['I.Time(8)']}</td>
                      <td>{item.Invoice}</td>
                      <td className='timecolumn'>{item['I.Time(30)']}</td>
                      <td>{item.IV_Team}</td>
                      <td className='timecolumn'>{item['I.Time(12)']}</td>
                      <td>{item.OPPHY}</td>
                      <td className='timecolumn'>{item['O.Time(10)']}</td>
                      <td>{item.OPAUD}</td>
                      <td className='timecolumn'>{item['O.Time(13)']}</td>
                      <td>{item.Authorization}</td>
                      <td className='timecolumn'>{item['A.Time(15)']}</td>
                      <td>{item.POC}</td>
                      <td className='timecolumn'>{item['P.Time(5)']}</td>
                      <td>{item.Referral}</td>
                      <td className='timecolumn'>{item['R.Time(11)']}</td>
                      <td>{item.O3COI}</td>
                      <td className='timecolumn'>{item['O.Time(25)']}</td>
                      <td>{item.Audit}</td>
                      <td className='timecolumn'>{item['IA.Time(5)']}</td>
                      <td>{item.Refund}</td>
                      <td className='timecolumn'>{item['Rf.Time(15)']}</td>
                      <td>{item.OtherTasks}</td>
                      <td className='timecolumn'>{item['OT.Time(5)']}</td>
                      <td>{item.Demo}</td>
                      <td className='timecolumn'>{item['D.Time(5)']}</td>
                      <td>{item.Bills}</td>
                      <td className='timecolumn'>{item['B.Time(5)']}</td>
                      <td>{item.Payment}</td>
                      <td className='timecolumn'>{item['P.Time(2)']}</td>
                      <td>{item.FollowUP}</td>
                      <td className='timecolumn'>{item['F.Time(8)']}</td>
                      <td>{item.Denial}</td>
                      <td className='timecolumn'>{item['D.Time(7)']}</td>
                      <td>{item.Ticket}</td>
                      <td className='timecolumn'>{item['T.Time(5)']}</td>

                      <td>{item.Rejection}</td>
                      <td className='timecolumn'>{item['E.Time(3)']}</td>
                      <td>{item.Appeals}</td>
                      <td className='timecolumn'>{item['A.Time(5)']}</td>

                      <td>{item.UrgentReferral}</td>
                      <td className='timecolumn'>{item['U.Time(15)']}</td>
                      <td>{item.BillCorrect}</td>
                      <td className='timecolumn'>{item['B.Time(25)']}</td>
                      <td>{item.F_Ticks}</td>
                      <td className='timecolumn'>{item['F.Time(2)']}</td>
                  </tr>
        ))}
        </tbody>
      </table>
      : ''}


{/* MIS Data Table */}

{ misbit? 
        <table className='tableStyle'>
        <thead className='column'>
          <tr>
            <th>No</th>
           <th>EmpID</th>
           <th>EmpName</th>
           <th>Lead</th>
           <th>ADO</th>
           <th>DO</th>
           <th>DSProd</th>
           <th>GPProd</th>
           <th>RVU</th>
           <th>DeductedRVU</th>
           <th>PaidRVU</th>
           <th>BucketRVU</th>
           <th>Assigned</th>
           <th>Resolve</th>
           <th>RbsRejected</th>
           <th>Rbs%</th>
           <th>KpiRejected</th>
           <th>Kpi%</th>
           <th>Denial</th>
           <th>De%</th>
           <th>Adjusted</th>
           <th>Ad%</th>
           <th>Remaining</th>
           <th>Re%</th>
           <th>PaidNow</th>
           <th>PN%</th>
           <th>ActiveTime</th>
           <th>NormalizedRVU</th>
           
          </tr>
        </thead>
        <tbody>

        {Array.isArray(MISData) && MISData.map((item, index) => (
                                <tr key={index} className={index % 2 === 0 ? 'evenRow' : 'oddRow'}>
                                    <td>{index + 1}</td>
                                    <td>{item.EmpID}</td>
                                    <td>{item.EmpName}</td>
                                    <td>{item.Lead}</td>
                                    <td>{item.ADO}</td>
                                    <td>{item.DO}</td>
                                    <td>{item.DSProd}</td>
                                    <td>{item.GPProd}</td>
                                    <td>{Number(item.RVU).toLocaleString()}</td>
                                    <td>{Number(item.DeductedRVU).toLocaleString()}</td>
                                    <td>{Number(item.PaidRVU).toLocaleString()}</td>
                                    <td>{Number(item.BucketRVU).toLocaleString()}</td>
                                    <td>{Number(item.Assigned).toLocaleString()}</td>
                                    <td>{Number(item.Resolve).toLocaleString()}</td>
                                    <td>{Number(item.RbsRejected).toLocaleString()}</td>
                                    <td>{Number(item.RbsPer).toLocaleString()}</td>
                                    <td>{Number(item.KpiRejected).toLocaleString()}</td>
                                    <td>{Number(item.KpiPer).toLocaleString()}</td>
                                    <td>{Number(item.Denial).toLocaleString()}</td>
                                    <td>{Number(item.DenialPer).toLocaleString()}</td>
                                    <td>{Number(item.Adjusted).toLocaleString()}</td>
                                    <td>{Number(item.AdjustedPer).toLocaleString()}</td>
                                    <td>{Number(item.Remaining).toLocaleString()}</td>
                                    <td>{Number(item.RemainingPer).toLocaleString()}</td>
                                    <td>{Number(item.PaidNow).toLocaleString()}</td>
                                    <td>{Number(item.PaidNowPer).toLocaleString()}</td>
                                    <td>{item.ActiveTime}</td>
                                    <td>{Number(item.NormalizedRVU).toLocaleString()}</td>
                                                
                                            </tr>
                                        ))}
        </tbody>
      </table>
      :''
      }

      {/* Global Portal Data Table */}

{ gpbit? 
        <table className='tableStyle'>
        <thead className='column'>
          <tr>
            <th>No</th>
          <th>EmpID</th>
           <th>EmpName</th>
           <th>Lead</th>
           <th>ADO</th>
           <th>DO</th>
           <th>DSProd</th>
           <th>GPProd</th>
           <th>WorkHoursWeek</th>
           <th>WorkHoursPerDay</th>
           <th>ClaimsSum</th>
           <th>Bills</th>
           <th>B.Time(5)</th>
           <th>Payments</th>
           <th>P.Time(2)</th>
           <th>FollowUP</th>
           <th>F.Time(8)</th>
           <th>OtherTask</th>
           <th>O.Time(5)</th>
           <th>Demo</th>
           <th>D.Time(5)</th>
           <th>Denial</th>
           <th>D.Time(7)</th>
           <th>Tickets</th>
           <th>T.Time(5)</th>
           <th>Rejections</th>
           <th>R.Time(3)</th>
           <th>Appeals</th>
           <th>A.Time(5)</th>
           <th>Index</th>
           <th>I.Time(8)</th>
           <th>Referral</th>
           <th>R.Time(11)</th>
           <th>UrgentReferral</th>
           <th>U.Time(15)</th>
           <th>OPPHY</th>
           <th>O.Time(10)</th>
           <th>OPAUD</th>
           <th>O.Time(13)</th>
           <th>Authorization</th>
           <th>A.Time(15)</th>
           <th>POC</th>
           <th>P.Time(5)</th>
           <th>BillCorrect</th>
           <th>B.Time(25)</th>
          </tr>
        </thead>
        <tbody>

        {Array.isArray(GPData) && GPData.map((item, index) => (
                                <tr key={index} className={index % 2 === 0 ? 'evenRow' : 'oddRow'}>
                                    <td>{index + 1}</td>
                                    <td>{item.EmpID}</td>
                                    <td>{item.EmpName}</td>
                                    <td>{item.Lead}</td>
                                    <td>{item.ADO}</td>
                                    <td>{item.DO}</td>
                                    <td>{item.DSProd}</td>
                                    <td>{item.GPProd}</td>
                                    <td>{item.WorkHoursWeek}</td>
                                    <td style={{backgroundColor: item.AdjustedSum >= 10 ? '#2da0bd' : item.AdjustedSum <=6 ? '#f13939' : '#bcc7ac',
                                          color: 'black'}}>{item.AdjustedSum}</td>
                                    <td>{item.ClaimsSum}</td>
                                    <td>{item.Bills}</td>
                                    <td className='timecolumn'>{item['B.Time(5)']}</td>
                                    <td>{item.Payments}</td>
                                    <td className='timecolumn'>{item['P.Time(2)']}</td>
                                    <td>{item.FollowUP}</td>
                                    <td className='timecolumn'>{item['F.Time(5)']}</td>
                                    <td>{item.OtherTask}</td>
                                    <td className='timecolumn'>{item['O.Time(5)']}</td>
                                    <td>{item.Demo}</td>
                                    <td className='timecolumn'>{item['D.Time(5)']}</td>
                                    <td>{item.Denial}</td>
                                    <td className='timecolumn'>{item['D.Time(7)']}</td>
                                    <td>{item.Tickets}</td>
                                    <td className='timecolumn'>{item['T.Time(5)']}</td>
                                    <td>{item.Rejections}</td>
                                    <td className='timecolumn'>{item['R.Time(3)']}</td>
                                    <td>{item.Appeals}</td>
                                    <td className='timecolumn'>{item['A.Time(5)']}</td>
                                    <td>{item.Index}</td>
                                    <td className='timecolumn'>{item['I.Time(8)']}</td>
                                    <td>{item.Referral}</td>
                                    <td className='timecolumn'>{item['R.Time(10)']}</td>
                                    <td>{item.UrgentReferral}</td>
                                    <td className='timecolumn'>{item['U.Time(15)']}</td>
                                    <td>{item.OPPHY}</td>
                                    <td className='timecolumn'>{item['O.Time(10)']}</td>
                                    <td>{item.OPAUD}</td>
                                    <td className='timecolumn'>{item['O.Time(13)']}</td>
                                    <td>{item.Authorization}</td>
                                    <td className='timecolumn'>{item['A.Time(10)']}</td>
                                    <td>{item.POC}</td>
                                    <td className='timecolumn'>{item['P.Time(5)']}</td>
                                    <td>{item.BillCorrect}</td>
                                    <td className='timecolumn'>{item['B.Time(25)']}</td>
                                </tr>
                            ))}
        </tbody>
      </table>
      :''
      }

        </div>
      </MDBRow>

      <Loader isLoading={isLoading} />

      </div>
      

    );
  }
export default Dashboard;

