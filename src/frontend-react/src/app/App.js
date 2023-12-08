import React from 'react';
import NavBar from '../components/NavBar';
import Header from '../components/Header';
import DomainForm from '../components/DomainForm';
import FileForm from '../components/FileForm';
import InfoSection from '../components/InfoSection';
import Footer from '../components/Footer';
import './App.css'; // Ensure you have your global styles here
import DataService from '../services/DataService';

function App() {
  // Init Data Service
  DataService.Init();
  return (
    <div className="App">
      <NavBar />
      <Header />
      <DomainForm />
      <FileForm />
      <InfoSection />
      <Footer />
    </div>
  );
}

export default App;
