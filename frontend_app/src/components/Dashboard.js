import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css'; // Add your CSS for styling

function Dashboard() {
  console.log('Check ');
  const [jobs, setJobs] = useState([]);
  const [jobTitle, setJobTitle] = useState('');
  const [inputData, setInputData] = useState('');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  
  console.log('The username is:', username);

  const navigate = useNavigate();

  useEffect(() => {
    if (!username) {
      navigate('/login'); // Redirect to login if no username is found
    } else {
      fetchJobs();
    }
  }, [username]);


  const fetchJobs = async () => {
    const token = localStorage.getItem('jwtToken');
    console.log('token is:', token);
    const response = await fetch('http://localhost:6302/list_jobs',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token,
        },
    });
    const data = await response.json();
    setJobs(data.jobs);
  };

  const handleJobSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('jwtToken');
    await fetch('http://localhost:6302/job_submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token,
      },
      body: JSON.stringify({ "title": jobTitle, "data": inputData }),
    });

    setJobTitle('');
    setInputData('');
    fetchJobs(); // Refresh the job list
  };

  const handleLogout = () => {
    localStorage.removeItem('username');
    navigate('/login');
  };
  console.log('Jobs:', jobs);
  return (
    <div className="dashboard-container">
      <h1>Hi {username}</h1>
      <button onClick={handleLogout} className="logout-button">Logout</button>
      
      <div className="job-submit-form">
        <h2>Submit a Job</h2>
        <form onSubmit={handleJobSubmit}>
          <div>
            <label>
              Job Title:
              <input 
                type="text" 
                value={jobTitle} 
                onChange={(e) => setJobTitle(e.target.value)} 
                required 
              />
            </label>
          </div>
          <div>
            <label>
              Input Data:
              <input 
                type="text" 
                value={inputData} 
                onChange={(e) => setInputData(e.target.value)} 
                required 
              />
            </label>
          </div>
          <button type="submit">Submit Job</button>
        </form>
      </div>

      <div className="job-list">
        <h2>Submitted Jobs</h2>
        <ul>
          {jobs.map((job, index) => (
            <li key={index}>
              <strong>{job.title}</strong>: {job.status}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
// '''

// "title": job_data["title"],
// "status": "In Progress",
// "created_at": str(datetime.now()),
// "completed_at": None

export default Dashboard;
