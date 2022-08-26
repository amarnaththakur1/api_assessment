import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const [teamName, setTeamName] = useState('');
  const [roleName, setRoleName] = useState('');
  const [message, setMessage] = useState('');

  let handleSubmit = async (e) => {
    e.preventDefault();
    let team = {
      team_name: teamName,
      role_name: roleName,
    };
    console.log(team);
    try {
      let res = await fetch('http://127.0.0.1:5000/teams/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(team),
      });
      let resJson = await res.json();
      console.log(resJson);
      if (res.status === 200) {
        setTeamName('');
        setRoleName('');
        setMessage('Team Created');
      } else {
        setMessage('Some error occured');
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <input type="text" value={teamName} placeholder="Team Name" required onChange={(e) => setTeamName(e.target.value)} />
        <input type="text" value={roleName} placeholder="Roll Name" required onChange={(e) => setRoleName(e.target.value)} />

        <button type="submit">Create</button>

        <div className="message">{message ? <p>{message}</p> : null}</div>
      </form>
    </div>
  );
}

export default App;
